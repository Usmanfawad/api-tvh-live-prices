# from App.db.session import get_db, exec_query

import httpx
import asyncio
import base64
import json

ACCESS_DATABASE_URL = r'C:\NextRevol\NufaersatzteileProject\App\db\NuFa.accdb'
f'DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={ACCESS_DATABASE_URL};'

ROUTE_GET = "https://api.tvh.com/availability-codes?language=en"

f = open('availabilityCodes.json')
DATA_TVH_AVAILABILITY = json.load(f)
print(DATA_TVH_AVAILABILITY[0])



def update_tbl_Preis():

    try:
        conn = get_db()
        cur = conn.cursor()

        query = """
            SELECT tbl_cache.Lieferant_Marke, tbl_Bestell_Nr.NuFa_Artikel , tbl_cache.price, tbl_cache.listPrice
            FROM tbl_Bestell_Nr
            LEFT JOIN tbl_cache ON tbl_Bestell_Nr.Bestellnummer = tbl_cache.Bestellnummer
                      AND tbl_Bestell_Nr.Lieferant_Marke = tbl_cache.Lieferant_Marke;
        """

        # Now updating tbl_Preis


    except Exception as e:
        print(e)


    return



if __name__ == "__main__":
    update_tbl_Preis()