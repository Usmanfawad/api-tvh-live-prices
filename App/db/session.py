import pyodbc
from typing import Generator
from App.core.config import settings


database_path = settings.ACCESS_DATABASE_URL
con_string = settings.ACCESS_CONN_STRING

def get_db():

    conn = pyodbc.connect(con_string)
    try:
        return conn
    except Exception as e:
        print(f"Error: {e}")


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
