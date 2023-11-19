import os
from typing import Any

from . import parser

class configurationReader:

    def __init__(self, filePath : str) -> None:
        
        if not os.path.exists(filePath): raise FileNotFoundError(f'Configuration file not found in "{filePath}"')
        if not os.path.isfile(filePath): raise IsADirectoryError('Configuration file path is a directory')
        if not os.path.splitext(filePath)[1][1:] == 'ini': raise TypeError('Configuration file is not a "ini" file')

        self.path = filePath


    def read(self, key : str, default : Any | None = None) -> Any:

        with open(self.path, 'r', encoding='utf-8') as configurationFile:

            configuration = configurationFile.read()
            lines = configuration.split('\n')

            for line in lines:
                if line.startswith('#') or line.strip() == '': continue

                address = line.split('=', 1)

                if len(address) != 2: raise SyntaxError(f'Syntax error at line:{line}')

                if address[0].strip() == key: return parser.parse(address[1].strip())

        if default: return default

        raise KeyError(f'No key named "{key}" in configuration')

