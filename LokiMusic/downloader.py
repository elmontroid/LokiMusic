import os
import json
import pathlib
from pytube import YouTube
from dataclasses import dataclass

from packages.Logger import logging, LogLevel
from packages.configParser import configurationReader

fileDelimiter = os.path.sep 
currentPath = pathlib.Path(__file__).parent.resolve()
logger = logging(LogLevel.debug)
configurationManager = configurationReader(f'{currentPath}{fileDelimiter}configuration.ini')

@dataclass
class metadata:
    id : str
    fileName : str
    fileFormat : str
    filePath : str

class MaxSize(Exception):
    pass

class AudioNotFound(Exception):
    pass


def resolveCache(id : str) -> metadata | None:
    with open(f'{currentPath}{fileDelimiter}data{fileDelimiter}cache.json', 'r', encoding='utf-8') as file:
        jsonContent = json.load(file)

        if jsonContent['data'].__contains__(id):
            data = jsonContent['data'][id]
            cacheMetadata = metadata(id, data['name'], data['format'], data['path'])

            return cacheMetadata

def updateCache(metadataContent : metadata) -> None:
    with open(f'{currentPath}{fileDelimiter}data{fileDelimiter}cache.json', 'r+', encoding='utf-8') as file:
        jsonContent = json.load(file)

        if jsonContent['data'].__contains__(metadataContent.id): raise KeyError(f'Cache with id[`{metadataContent.id}`] already exist')
        jsonContent['data'][metadataContent.id] = {'name' : metadataContent.fileName, 'format' : metadataContent.fileFormat, 'path' : metadataContent.filePath}
        
        file.seek(0)
        json.dump(jsonContent, file)


def download(url : str, format : str | list[str], logger : logging = logger) -> metadata:
    logger.warn('Starting download process')
    
    logger.debug('initializing YouTube object')
    stream = None
    video = YouTube(url, use_oauth=configurationManager.read('authorizedDownload', False))
    logger.debug(f'video tittle: {video.video_id}, author : {video.author}, views : {video.views}')
    logger.debug('initialized YouTube object')

    logger.log('Searching in cache file for metadata')
    cache = resolveCache(video.video_id)
    if cache:
        logger.warn('Resolving request from cache')
        return cache

    else:
        logger.debug('No cache found')

    logger.log(f'Selecting audio stream with extension as `{format}`')
    if type(format) == str:
        logger.debug(f'Selecting audio stream with extension as `{format}` because no other formats provided')
        stream = video.streams.get_audio_only(format)

    else:
        for fileFormat in format:
            logger.debug(f'Attempting selection with extension as `{fileFormat}`')
            stream = video.streams.get_audio_only(fileFormat)
            if not stream == None:
                logger.debug(F'Selected audio stream with extension as `{fileFormat}`')
                break

    if stream == None: raise AudioNotFound

    logger.warn(f'Audio requires {stream.filesize_mb}mb in disk space')
    maxsize = configurationManager.read('maxDownloadSize', None)
    if maxsize == None or maxsize == 0: maxsize = 999
    
    if stream.filesize_mb > maxsize:
        logger.error('Audio requires more space than maximum defined by admin')
        raise MaxSize

    timeoutsec = configurationManager.read('downloadTimeout', None)
    if timeoutsec == None or timeoutsec == 0: timeoutsec = None

    logger.debug(f'size(MB): {stream.filesize_mb}, file name: {stream.default_filename}')
    logger.warn('Starting audio download')
    filePath = stream.download(f'{currentPath}{fileDelimiter}audios', timeout=timeoutsec)
    logger.warn('Audio download completed')

    logger.debug('Generating metadata')
    videoMetadata = metadata(video.video_id, os.path.splitext(stream.default_filename)[0].encode('latin-1', 'replace').decode('latin-1', 'ignore'), os.path.splitext(filePath)[1][1:], filePath)
    logger.debug('Generated metadata')

    logger.debug('Updating cache')
    updateCache(videoMetadata)
    logger.debug('Successfully updated cache')

    logger.warn('Download process completed')
    return videoMetadata


if __name__ == "__main__":
    download('https://youtu.be/2giYju6OcM0', 'mp4')
