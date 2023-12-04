from App.db.session import get_db, exec_query

ACCESS_DATABASE_URL = r'C:\NextRevol\nufaersatzteile\NuFa\TVH_Abgleich.accdb'
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
        INSERT INTO tbl_cache ( Bestellnummer, Lieferant_Marke, aktiv, Lieferant )
        SELECT tbl_Bestell_Nr.Bestellnummer, First(tbl_MakeCodes.code) AS Make_Code, tbl_Bestell_Nr.aktiv, tbl_Bestell_Nr.Lieferant
        FROM tbl_Bestell_Nr INNER JOIN tbl_MakeCodes ON tbl_Bestell_Nr.Lieferant_Marke = tbl_MakeCodes.descr
        GROUP BY tbl_Bestell_Nr.Bestellnummer, tbl_Bestell_Nr.aktiv, tbl_Bestell_Nr.Lieferant
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
        sql_query = "DELETE FROM tbl_cache WHERE (Bestellnummer IS NULL OR Bestellnummer = '') OR (Lieferant_Marke IS NULL OR Lieferant_Marke = '')"
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
        sql_query = "SELECT Lieferant_Marke, Bestellnummer FROM tbl_cache"
        cur.execute(sql_string)
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


if __name__ == "__main__":
    delete_all_table_cache()