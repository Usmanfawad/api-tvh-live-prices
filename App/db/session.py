import pyodbc
import mysql.connector

import os
from dotenv import load_dotenv

from typing import Generator

from App.core.config import settings


database_path = settings.ACCESS_DATABASE_URL
con_string = settings.ACCESS_CONN_STRING

def get_db():
    try:
        # Load environment variables from .env file
        load_dotenv()
        database_type = os.getenv("DATABASE_TYPE")
        if database_type == "msaccess":
            print("The DB path is: " + database_path)
            conn = pyodbc.connect(con_string)
            return conn
        elif database_type == "mysql":
            mysqldb = mysql.connector.connect(
                host="nufa-ersatzteile.de",
                user="d03e7870",
                password="XmvruZzZYSPFtp87T8SP",
                database="d03e7870"
            )
            return mysqldb
        else:
            raise ValueError("Unsupported database type")
    except Exception as e:
        print(f"Error {e}")


def exec_query(str_query):
    if "SELECT" in str_query:
        try:
            print("Select")
            print(str_query)
            conn = get_db()
            cur = conn.cursor()
            cur.execute(str_query)
            rows = cur.fetchall()
            conn.close()
            return rows

        except Exception as e:
            print(f"Error: {e}")
    else:
        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute(str_query)
            conn.commit()
            conn.close()
            print("Committed")
            return True

        except Exception as e:
            print(f"Error: {e}")
