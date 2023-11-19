import colorama
from dataclasses import dataclass

colors = colorama.Fore


@dataclass(init=False)
class LogLevel:
    debug : int = 1
    info : int = 2
    warn : int = 3
    error : int = 4


@dataclass(frozen=True)
class MessageColor:
    heading : str
    message : str


@dataclass
class ColorSettings:
    reset : str = colors.RESET
    debug : MessageColor = MessageColor(colors.LIGHTBLACK_EX, colors.LIGHTWHITE_EX)
    info : MessageColor = MessageColor(colors.LIGHTBLACK_EX, colors.WHITE)
    warn : MessageColor = MessageColor(colors.LIGHTYELLOW_EX, colors.LIGHTCYAN_EX)
    error : MessageColor = MessageColor(colors.LIGHTRED_EX, colors.LIGHTGREEN_EX)
