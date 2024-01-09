from App.db.session import get_db, exec_query


from datetime import datetime

current_date = datetime.now().strftime('%d/%m/%Y')
print(type(current_date))

ACCESS_DATABASE_URL = r'C:\NextRevol\NufaersatzteileProject\App\db\TVH_Abgleich.accdb'
f'DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={ACCESS_DATABASE_URL};'


def delete_table_cache():

    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM tbl_cache")
        cur.commit()
        conn.close()
        return True

    except Exception as e:
        print(f"Error: {e}")
        return False

def insert_into_table_cache():

    try:
        conn = get_db()
        cur = conn.cursor()
        sql_string = """
        INSERT INTO tbl_cache ( Bestellnummer, Lieferant_Marke, aktiv, Lieferant, inquiryAmount )
        SELECT tbl_Bestell_Nr.Bestellnummer, First(tbl_MakeCodes.code) AS Make_Code, tbl_Bestell_Nr.aktiv, tbl_Bestell_Nr.Lieferant, tbl_Artikel.TVH_Abfragemenge
        FROM tbl_Artikel INNER JOIN (tbl_Bestell_Nr INNER JOIN tbl_MakeCodes ON tbl_Bestell_Nr.Lieferant_Marke = tbl_MakeCodes.descr) ON tbl_Artikel.Art_Nr_NuFa = tbl_Bestell_Nr.NuFa_Artikel
        GROUP BY tbl_Bestell_Nr.Bestellnummer, tbl_Bestell_Nr.aktiv, tbl_Bestell_Nr.Lieferant, tbl_Artikel.TVH_Abfragemenge
        HAVING (((tbl_Bestell_Nr.aktiv)=True) AND ((tbl_Bestell_Nr.Lieferant)=1));
        """
        cur.execute(sql_string)
        conn.commit()
        cur.close()
        conn.close()
        return True

    except Exception as e:
        print(f"Error: {e}")
        return False


def delete_from_table_cache():

    try:
        conn = get_db()
        cur = conn.cursor()
        sql_string = "DELETE FROM tbl_cache WHERE (Bestellnummer IS NULL OR Bestellnummer = '') OR (Lieferant_Marke IS NULL OR Lieferant_Marke = '')"
        cur.execute(sql_string)
        conn.commit()
        cur.close()
        conn.close()
        return True

    except Exception as e:
        print(f"Error: {e}")
        return False

def select_from_table_cache():

    try:
        conn = get_db()
        cur = conn.cursor()
        sql_query = "SELECT Lieferant_Marke, Bestellnummer, inquiryAmount FROM tbl_cache ORDER BY Bestellnummer ASC"
        cur.execute(sql_query)
        rows = cur.fetchall()
        cur.close()
        return rows

    except Exception as e:
        print(f"Error: {e}")
        return False


def update_json_strings_in_cache(updates, price, listPrice):
    conn = get_db()
    cur = conn.cursor()
    for lieferant_marke, bestellnummer, json_string, json_response in updates:
        cur.execute("""UPDATE tbl_cache 
        SET json_string = ?, 
        json_response = ?, 
        price = ?, 
        listPrice = ?,
        Datum = ?
        WHERE Lieferant_Marke = ? AND Bestellnummer = ?""", (json_string, json_response, price, listPrice, current_date, lieferant_marke, bestellnummer))
        conn.commit()

    cur.close()
    conn.close()

    return



if __name__ == "__main__":
    delete_all_table_cache()