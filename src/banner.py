import pyfiglet
import termcolor

from rich import print as printC
from rich.console import Console
console = Console()


def DisplayBanner():
    ascii_banner = pyfiglet.figlet_format("PassGuard")
    termcolor.cprint(ascii_banner, color="blue")
    printC("[green]PassGuard 2023 v0.1")
