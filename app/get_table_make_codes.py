# from app.db.session import get_db, exec_query
import pyodbc
import os
from dotenv import load_dotenv
import json
from datetime import datetime


ACCESS_DATABASE_URL = r'C:\NextRevol\NufaersatzteileProject\App\db\NuFa.accdb'
ACCESS_CONN_STRING = f'DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={ACCESS_DATABASE_URL};'


def get_make_codes():
    conn = pyodbc.connect(ACCESS_CONN_STRING)
    cur = conn.cursor()

    select_query = "SELECT * from tbl_MakeCodes"
    dict_make_codes = {}
    cur.execute(select_query)
    rows = cur.fetchall()
    for each in rows:
        dict_make_codes[each[1]] = each[0]

    with open("makeCodes.json", "w") as json_file:
        json.dump(dict_make_codes, json_file, indent=4)

if __name__ == "__main__":
    get_make_codes()
