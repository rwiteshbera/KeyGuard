import sys

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
        printC("[red][!] An error occured while trying to connect with vault.")

    return db


def configDB():
    try:
        db = connectDB()
        if db is not None:
            cursor = db.cursor()

            # Create Database
            cursor.execute("CREATE DATABASE IF NOT EXISTS passguard")
            # Create Table
            query = "CREATE TABLE IF NOT EXISTS passguard.secrets (email VARCHAR(256) UNIQUE PRIMARY KEY, masterPassword_hash TEXT NOT NULL)"
            res = cursor.execute(query)
            query = "CREATE TABLE IF NOT EXISTS passguard.entries (name VARCHAR(256) NOT NULL,token TEXT NOT NULL)"
            res = cursor.execute(query)
    
            db.close()

    except Exception as e:
        printC("[red][!] An error occured while trying to configure vault.")
        sys.exit(0)
