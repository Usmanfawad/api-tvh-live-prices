from datetime import datetime
import pyodbc


ACCESS_DATABASE_URL = r'C:\NextRevol\NufaersatzteileProject\App\db\NuFa.accdb'
ACCESS_CONN_STRING = f'DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={ACCESS_DATABASE_URL};'

current_date = datetime.now().strftime('%d-%m-%Y')
print(current_date)


def get_db():

    conn = pyodbc.connect(ACCESS_CONN_STRING)
    try:
        return conn
    except Exception as e:
        print(f"Error: {e}")


def select_from_table_cache():

    try:
        conn = get_db()
        cur = conn.cursor()
        query = """
            SELECT 
                tbl_Preise.NuFa_Art,
                tbl_Preise.lst_Preis,
                tbl_cache.Datum
            FROM table_Preise
            INNER JOIN tbl_cache ON tbl_Preise.NuFa_Art = tbl_cache.Bestellnummer
        """
        cur.execute(query)
        rows = cur.fetchall()
        print(rows)
        cur.close()
        return rows

    except Exception as e:
        print(f"Error: {e}")
        return False

def update_json_strings_in_cache():
    try:
        conn = pyodbc.connect(ACCESS_CONN_STRING)
        cur = conn.cursor()
        conn.autocommit = True


        update_query = """
            UPDATE tbl_Preise
            SET 
                tbl_Preise.EKPreis = tbl_cache.price,
                tbl_Preise.Datum = tbl_cache.Datum,
                tbl_Preise.lst_Preis = tbl_cache.listPrice
            FROM tbl_Preise
            INNER JOIN tbl_cache ON tbl_Preise.NuFa_Art = tbl_cache.Bestellnummer
        """

        query = """
           UPDATE tbl_Preise
           SET 
               EKPreis = (SELECT price FROM tbl_cache WHERE tbl_cache.Bestellnummer = tbl_Bestell_Nr.Bestellnummer),
               lst_Preis = (SELECT listPrice FROM tbl_cache WHERE tbl_cache.Bestellnummer = tbl_Bestell_Nr.Bestellnummer)
           FROM 
               tbl_Preise
           JOIN 
               tbl_Bestell_Nr ON tbl_Preise.NuFa_Art = tbl_Bestell_Nr.NuFa_Artikel;
           """



        cur.execute(query)
        # conn.close()
        print("Updated timestamps")
        return

    except Exception as e:
        print(f"Error: {e}")
        return False


if __name__ == "__main__":
    # select_from_table_cache()
    update_json_strings_in_cache()