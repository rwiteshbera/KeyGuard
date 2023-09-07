import mysql.connector

from rich import print as printC
from rich.console import Console
console = Console()


def connectDB():
    db = None
    try:
        db = mysql.connector.connect(
            host='localhost',
            user='admin',
            password='admin'
        )

    except Exception as e:
        printC("[red][!] An error occured while trying to connect with vault.[/red]")

    return db