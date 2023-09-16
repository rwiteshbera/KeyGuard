import pyfiglet
import termcolor

from rich import print as printC
from rich.console import Console
console = Console()


def DisplayBanner():
    ascii_banner = pyfiglet.figlet_format("KeyGuard")
    termcolor.cprint(ascii_banner, color="blue")
    printC("[green]KeyGuard 2023 v0.5")
