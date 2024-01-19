from datetime import datetime
import pyodbc
import json


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

def availability_code_from_json_response():
    try:
        conn = get_db()
        cur = conn.cursor()
        query = "SELECT Bestellnummer, json_response FROM tbl_cache"
        cur.execute(query)
        data = cur.fetchall()
        for rows in data:
            json_obj = json.loads(rows[1])
            availability_code = json_obj[0]["lines"][0]["availabilityCode"]
            cur.execute("UPDATE tbl_cache SET availabilityCode = ? where Bestellnummer = ?", (availability_code, rows[0]))
            conn.commit()

        return rows
    except Exception as e:
        print(f"Error: {e}")
        return False

    cur.close()
    conn.close()


def join_table_update_tbl_preise():
    current_date = datetime.now().strftime('%d/%m/%Y')
    try:
        conn = get_db()
        conn.autocommit = True
        cur = conn.cursor()

        # First creating another table that takes the last prices of dates and duplicates all NuFa_Arts

        query_delete_dups = """
        SELECT T.NuFa_Art, T.Datum, T.EKPreis, T.fid_Liefer
        FROM tbl_Preise AS T INNER JOIN (SELECT [NuFa_Art], Max([Datum]) AS MaxDatum FROM tbl_Preise GROUP BY [NuFa_Art])  AS Q ON (T.[Datum] = Q.MaxDatum) AND (T.[NuFa_Art] = Q.[NuFa_Art])
        WHERE (((T.Datum)<>#12/1/2016 1:0:0#));
        """

        # delete_all_from_tbl_Preise = """
        # DELETE FROM tbl_Preise
        # """

        cur.execute(query_delete_dups)
        rows = cur.fetchall()
        print(rows)

        cur.execute(delete_all_from_tbl_Preise)
        # conn.commit()


        # query = """
        # SELECT tbl_cache.listPrice, tbl_cache.price, tbl_cache.availabilityCode, tbl_cache.Datum, tbl_Bestell_Nr.NuFa_Artikel
        # FROM tbl_Bestell_Nr
        # LEFT JOIN tbl_cache ON tbl_Bestell_Nr.Bestellnummer = tbl_cache.Bestellnummer
        #           AND tbl_Bestell_Nr.Lieferant_Marke = tbl_cache.Lieferant_Marke;
        # """
        #
        # cur.execute(query)
        # rows = cur.fetchall()
        # print(rows)
        #
        # try:
        #     table_Preise = "tbl_Preise"
        #     column_names = ['lst_Preis', 'EKPreis', 'Lieferzeit', 'Datum']
        #     sql_query = f"UPDATE {table_Preise} SET {', '.join([f'{col} = ?' for col in column_names])} WHERE NuFa_Art = ?"
        #     cur.executemany(sql_query, rows)
        # except Exception as e:
        #     print(e)


        # for each_row in rows:
        #     if tuple(each_row).count(None) < 3:
        #         cur.execute("UPDATE tbl_Preise SET lst_Preis = ?, EKPreis = ?, Lieferzeit = ?, Datum = ? where NuFa_Art = ?", (each_row[1], each_row[2], each_row[3], current_date, each_row[0]))
        #         conn.commit()
        #         print(each_row)

        return rows

    except Exception as e:
        print(f"Error: {e}")
        return False

    # conn.commit()
    # cur.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    join_table_update_tbl_preise()

    # this was just used as a test, ran it already, have all availability codes in the DB now.
    # availability_code_from_json_response()