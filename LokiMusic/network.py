from os import path
from pytube import exceptions
from functools import cached_property
from urllib.parse import urlparse, parse_qsl
from http.server import BaseHTTPRequestHandler

import downloader
from packages.Logger import logging, LogLevel
from packages.configParser import configurationReader

fileDelimiter = path.sep
logger = logging(LogLevel.debug)
configurationManager = configurationReader(f'.{fileDelimiter}configuration.ini')


class handler(BaseHTTPRequestHandler):
   
    @cached_property
    def url(self):
        return urlparse(self.path)

    @cached_property
    def query_data(self):
        return dict(parse_qsl(self.url.query))

    def log_message(self, format, *args):
        pass


    def do_GET(self):

        if configurationManager.read('accessControl', False) == True:
            if configurationManager.read('blacklist', []).__contains__(self.client_address[0]):
                logger.warn(f'Access denied for client at {self.client_address[0]}')
                logger.debug(f'Access control is active in configuration with blacklist value being `{configurationManager.read("blacklist")}`')
                logger.debug('Sending error HTTP status code[403]')
                self.send_error(403)

                return None

        if self.url.path == '/':
            logger.log(f'New request for `index.html` from client at {self.client_address[0]}')
            logger.debug('Opening `index.html` from `data` directory')
            with open(f'.{fileDelimiter}data{fileDelimiter}index.html', 'r', encoding='utf-8') as file:
                logger.debug('Reading `index.html` file')
                page = file.read()
                logger.debug('Sending HTTP status code to client[200]')
                self.send_response(200)
                logger.debug('Sending MIME type header[text/html]')
                self.send_header('Content-Type', 'text/html')
                logger.debug('Sending end header to client')
                self.end_headers()
                logger.log(f'Sending `index.html` to client at {self.client_address[0]}')
                self.wfile.write(page.encode('utf-8', 'replace'))
                logger.log(f'Successfully transmitted `index.html` to client at {self.client_address[0]}')

            return None


        if self.url.path == '/download':
            logger.log(f'New download request for video from client at {self.client_address[0]}')

            if not self.query_data.__contains__('url'):
                logger.warn(f'Client at {self.client_address[0]} transmitted a corrupted request to server')
                logger.debug("Request doesn't contain `url` parameter")
                logger.debug('Sending error HTTP status code[400]')
                self.send_error(400, 'A query parameter named `url` must be present with a correct YouTube video URL as value', configurationManager.read('requestError'))
                logger.debug('Transmitted error HTTP status code')

                return None

            logger.debug(f'content url : {self.query_data["url"]}, client IP : {self.client_address[0]}')

            try:
                metadata = downloader.download(self.query_data['url'], configurationManager.read('downloadFileFormats', 'mp4'), logger)

                logger.warn(f'Sending audio to client at {self.client_address[0]}')
                logger.debug(f'Sending HTTP status code with file name[200, {metadata.fileName}]')
                self.send_response(200, metadata.fileName)
                logger.debug(f'Sending MIME type header[{metadata.fileFormat}]')
                self.send_header('Content-Type', f'audio/{metadata.fileFormat}')
                logger.debug('Sending end header to client')
                self.end_headers()
                logger.debug('Sending audio data to client')
                with open(metadata.filePath, 'rb') as audioFile:
                    self.wfile.write(audioFile.read())
                logger.log(f'Successfully transmitted audio to client at {self.client_address[0]}')

            except exceptions.RegexMatchError as error:
                logger.error("Can't fulfill download request because client transmitted a corrupted URL for download")
                logger.debug(f'Details: {error}')
                logger.debug('Sending error HTTP status code[404]')
                self.send_error(404, configurationManager.read('userError'), 'download url is not valid')

            except exceptions.VideoUnavailable as error:
                logger.error("Can't extract audio from a unsupported content type")
                logger.debug(f'Details: {error}')
                logger.debug('Sending error HTTP status code[415]')
                self.send_error(404, configurationManager.read('contentError'), 'The url belongs to a unsupported content')

            except exceptions.PytubeError as error:
                logger.error("Extraction system failed to extract audio from url because of an unknown error")
                logger.debug(f'Details: {error}')
                logger.debug('Sending error HTTP status code[500]')
                self.send_error(404, configurationManager.read('extractError'), 'The server failed to extract audio from URL because of an error')

            except BaseException as error:
                logger.error("Can't fulfill download request because of an unknown server error")
                logger.debug(f'Details: {error}')
                logger.debug('Sending error HTTP status code[500]')
                self.send_error(500, configurationManager.read('serverError'))


            return None

        logger.warn(f"Can't serve client at {self.client_address[0]} because got unknown path[{self.url.path}]")
        self.send_error(404)
