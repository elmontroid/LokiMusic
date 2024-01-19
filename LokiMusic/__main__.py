import sys
import pathlib
import colorama
from os import path
from http.server import HTTPServer
from datetime import datetime

import network
from packages.Logger import logging, LogLevel
from packages.configParser import configurationReader

colors = colorama.Fore

fileDelimiter = path.sep
currentPath = pathlib.Path(__file__).parent.resolve()

logger = logging(LogLevel.info)
network.logger = logger
configurationManager = configurationReader(f'{currentPath}{fileDelimiter}configuration.ini')

if sys.argv.__contains__('--host'):

    HOST = configurationManager.read('publicUrl')
    PORT = configurationManager.read('publicPort')

else:
    HOST = configurationManager.read('privateUrl', 'localhost')
    PORT = configurationManager.read("privatePort", 9000)


print(f"  {colors.LIGHTGREEN_EX}Server v0.1{colors.LIGHTBLACK_EX} stated at {colors.WHITE}{datetime.now().strftime('%X')}{colors.RESET}  \n")
if HOST == 'localhost':
    print(f"{colors.LIGHTGREEN_EX}> {colors.LIGHTBLACK_EX}Local:   {colors.LIGHTBLUE_EX}http://{HOST}:{colors.CYAN}{PORT}{colors.RESET}")
    print(f"{colors.LIGHTGREEN_EX}> {colors.LIGHTBLACK_EX}Network: {colors.LIGHTBLACK_EX}use {colors.LIGHTWHITE_EX}`--host`{colors.LIGHTBLACK_EX} to expose{colors.RESET}\n")

else:
    print(f"{colors.LIGHTGREEN_EX}> {colors.LIGHTBLACK_EX}Local:   {colors.LIGHTBLUE_EX}http://{HOST}:{colors.CYAN}{PORT}{colors.RESET}")
    print(f"{colors.LIGHTGREEN_EX}> {colors.LIGHTBLACK_EX}Network:   {colors.LIGHTBLUE_EX}http://{HOST}:{colors.CYAN}{PORT}{colors.RESET}\n")

try:
    Server = HTTPServer((HOST, PORT), network.handler)
    Server.serve_forever()

except KeyboardInterrupt:
    logger.warn('Server shutting down because user interrupted server task', fileLog=False, force=True)

except BaseException as error:
    logger.error('Unexpected server shutdown because an internal critical error has occurred with the following error message', fileLog=True, force=True)
    logger.error(f'Error: {error}', fileLog=True, force=True)
