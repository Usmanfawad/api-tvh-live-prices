# from App.db.session import get_db, exec_query

import httpx
import asyncio
import base64
import json
import pyodbc


ACCESS_DATABASE_URL = r'C:\NextRevol\NufaersatzteileProject\App\db\NuFa.accdb'
ACCESS_CONN_STRING = f'DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={ACCESS_DATABASE_URL};'

ROUTE_GET = "https://api.tvh.com/availability-codes?language=en"

# f = open('availabilityCodes.json')
# DATA_TVH_AVAILABILITY = json.load(f)


def get_db():

    conn = pyodbc.connect(ACCESS_CONN_STRING)
    try:
        return conn
    except Exception as e:
        print(f"Error: {e}")



def update_tbl_Preis():

    try:
        conn = get_db()
        conn.autocommit = True
        cur = conn.cursor()

        query = """
            SELECT tbl_Bestell_Nr.NuFa_Artikel, tbl_cache.Datum, tbl_cache.price, tbl_cache.listPrice, tbl_cache.Lieferant
            FROM tbl_Bestell_Nr
            LEFT JOIN tbl_cache ON tbl_Bestell_Nr.Bestellnummer = tbl_cache.Bestellnummer
                      AND tbl_Bestell_Nr.Lieferant_Marke = tbl_cache.Lieferant_Marke;
        """
        cur.execute(query)
        rows = cur.fetchall()
        print(len(rows))
        for row in rows:
            insert_query = "INSERT INTO tbl_Preise (NuFa_Art, Datum, EKPreis, lst_Preis, fid_Liefer) VALUES (?, ?, ?, ?, ?)"
            cur.execute(insert_query, row)


    except Exception as e:
        print("Error")
        print(e)


    return



if __name__ == "__main__":
    update_tbl_Preis()