import os
import colorama
from datetime import datetime

from . import options

color = colorama.Fore


class logging:

    def __init__(self, logLevel : int = options.LogLevel.info, file : str | None = None, colorSettings = options.ColorSettings()) -> None:

        if file and not os.path.exists(file): raise FileNotFoundError(f'Log file not found at {file}')
        if file and not os.path.isfile(file): raise IsADirectoryError('Log file path is a directory')

        self.logFile = file
        self.level = logLevel
        self.colorSettings = colorSettings


    def debug(self, message : str, fileLog : bool = True, suppressOutput : bool = False, force : bool = False) -> None:
        if not force and self.level > 1: return None

        if fileLog and self.logFile:
            with open(self.logFile, 'a', encoding='utf-8') as file:
                file.write(f'> DEBUG:   {message}  ---[{datetime.now().strftime("%x %X")}]\n')

        if not suppressOutput:
            print(f'{color.LIGHTRED_EX}> {self.colorSettings.debug.heading}Debug: {self.colorSettings.debug.message}{message}{color.RESET}')


    def log(self, message : str, fileLog : bool = True, suppressOutput : bool = False, force : bool = False) -> None:
        if not force and self.level > 2: return None

        if fileLog and self.logFile:
            with open(self.logFile, 'a', encoding='utf-8') as file:
                file.write(f'> LOG:     {message}  ---[{datetime.now().strftime("%x %X")}]\n')

        if not suppressOutput:
            print(f'{color.LIGHTRED_EX}> {self.colorSettings.info.heading}Log:   {self.colorSettings.info.message}{message}{color.RESET}')


    def warn(self, message : str, fileLog : bool = True, suppressOutput : bool = False, force : bool = False) -> None:
        if not force and self.level > 3: return None

        if fileLog and self.logFile:
            with open(self.logFile, 'a', encoding='utf-8') as file:
                file.write(f'> WARNING: {message}  ---[{datetime.now().strftime("%x %X")}]\n')

        if not suppressOutput:
            print(f'{color.LIGHTRED_EX}> {self.colorSettings.warn.heading}Warn:  {self.colorSettings.warn.message}{message}{color.RESET}')


    def error(self, message : str, fileLog : bool = True, suppressOutput : bool = False, force : bool = False) -> None:
        if not force and self.level > 4: return None

        if fileLog and self.logFile:
            with open(self.logFile, 'a', encoding='utf-8') as file:
                file.write(f'> ERROR:   {message}  ---[{datetime.now().strftime("%x %X")}]\n')

        if not suppressOutput:
            print(f'{color.LIGHTRED_EX}> {self.colorSettings.error.heading}Error: {self.colorSettings.error.message}{message}{color.RESET}')

