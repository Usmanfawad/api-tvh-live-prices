from app.db.session import get_db, exec_query

import os
from dotenv import load_dotenv

import httpx
import asyncio
import base64
import json
import pyodbc


# ACCESS_DATABASE_URL = r'C:\NextRevol\NufaersatzteileProject\app\db\NuFa.accdb'
env_path = os.getenv("ENV_PATH")
# ACCESS_DATABASE_URL = os.path.join(env_path, "db", "NuFa.accdb")
# ACCESS_CONN_STRING = f'DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={ACCESS_DATABASE_URL};'
# load_dotenv()
DBNAME = os.getenv("DATABASE_TYPE")

ROUTE_GET = "https://api.tvh.com/availability-codes?language=en"

# f = open('availabilityCodes.json')
# DATA_TVH_AVAILABILITY = json.load(f)


# def get_db():
#
#     conn = pyodbc.connect(ACCESS_CONN_STRING)
#     try:
#         return conn
#     except Exception as e:
#         print(f"Error: {e}")



def update_tbl_Preis():
    try:
        if DBNAME == "msaccess":
            print("Post processing msaccess")
            conn = get_db()
            conn.autocommit = True
            cur = conn.cursor()

            query = """
                        SELECT tbl_Bestell_Nr.NuFa_Artikel, tbl_cache.Datum, tbl_cache.price, tbl_cache.listPrice, tbl_cache.Lieferant
                        FROM tbl_Bestell_Nr
                        INNER JOIN tbl_cache ON tbl_Bestell_Nr.Bestellnummer = tbl_cache.Bestellnummer
                                  AND tbl_Bestell_Nr.Lieferant_Marke = tbl_cache.Lieferant_Marke;
                    """
            cur.execute(query)
            rows = cur.fetchall()
            print(len(rows))
            insert_query = "INSERT INTO tbl_Preise (NuFa_Art, Datum, EKPreis, lst_Preis, fid_Liefer) VALUES (?, ?, ?, ?, ?)"
            insert_data = [(row[0], row[1], row[2], row[3], row[4]) for row in rows]
            # Execute the insert operation using executemany
            cur.executemany(insert_query, insert_data)

        else:
            print("Post processing mysql")
            conn = get_db()
            conn.autocommit = True
            cur = conn.cursor()

            query = """
                        SELECT tbl_Bestell_Nr.NuFa_Artikel, tbl_cache.Datum, tbl_cache.price, tbl_cache.listPrice, tbl_cache.Lieferant
                        FROM tbl_Bestell_Nr
                        INNER JOIN tbl_cache ON tbl_Bestell_Nr.Bestellnummer = tbl_cache.Bestellnummer
                                  AND tbl_Bestell_Nr.Lieferant_Marke = tbl_cache.Lieferant_Marke;
                    """
            cur.execute(query)
            rows = cur.fetchall()
            print(len(rows))
            for row in rows:
                insert_query = "INSERT INTO tbl_Preise (NuFa_Art, Datum, EKPreis, lst_Preis, fid_Liefer) VALUES (%s, %s, %s, %s, %s)"
                cur.execute(insert_query, row)



    except Exception as e:
        print("Error")
        print(e)


    return



if __name__ == "__main__":
    update_tbl_Preis()