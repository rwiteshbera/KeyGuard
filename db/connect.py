import sys

import mysql.connector

from utils.compute import computeMasterKey
from utils.compute import computeMasterPasswordHash

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


def verifyMasterPassword(email, masterPassword) -> bool:
    try:
        db = connectDB()
        if db is not None:
            cursor = db.cursor()

            # Create Database
            cursor.execute("CREATE DATABASE IF NOT EXISTS passguard")
            # Create Table
            query = "SELECT masterPassword_hash FROM passguard.secrets WHERE email = %s"
            value = (email,)
            cursor.execute(query, value)

            # Compute Master Key from Email and MASTER PASSWORD
            masterKey = computeMasterKey(
                salt=email.encode('utf-8'), payload=masterPassword.encode('utf-8'))
            
            # Compute Master Password Hash from Master Key and MASTER PASSWORD
            masterPasswordHash = computeMasterPasswordHash(
                salt=masterPassword.encode('utf-8'), payload=masterKey)
    
            for row in cursor:
                if str(row[0]) != masterPasswordHash:
                    return False

            db.close()

    except Exception as e:
        printC("[red][!] An error occured while trying to verify credentials.")
        console.print_exception()
        sys.exit(0)  
    
    return True