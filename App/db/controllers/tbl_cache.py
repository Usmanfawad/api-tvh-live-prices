from App.db.session import get_db, exec_query


from datetime import datetime

current_date = datetime.now().strftime('%d/%m/%Y')
print(type(current_date))


def delete_table_cache():

    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM tbl_cache")
        conn.commit()
        conn.close()
        return True

    except Exception as e:
        print("Error delete_table_cache")
        print(f"Error: {e}")
        return False

def insert_into_table_cache():

    try:
        conn = get_db()
        cur = conn.cursor()

        # Select from tbl_Bestellnummer
        select_query = "SELECT Bestellnummer, Lieferant, NuFa_Artikel, Lieferant_Marke, aktiv FROM tbl_Bestell_Nr WHERE aktiv='WAHR' AND Lieferant=1"

        # Execute the query
        cur.execute(select_query)

        # Create a set to store unique combinations
        unique_combinations = set()

        # Fetch all rows from the result set
        rows = cur.fetchall()
        print(len(rows))

        # Insert data into tbl_cache
        insert_query = "INSERT INTO tbl_cache (Bestellnummer, Lieferant, Lieferant_Marke, aktiv) VALUES (%s, %s, %s, %s)"

        for row in rows:
            # with open("combinations.txt", "a") as f:
            #     f.write(str(row[0]) + str(row[3]) + "\n")
            combination = (row[0], row[3])  # 0 - Bestellnummer 3 - Lieferank marke
            print(row)
            if combination not in unique_combinations:
                cur.execute(insert_query, (row[0], row[1], row[3], row[4]))
                unique_combinations.add(combination)

        conn.commit()
        # sql_string = """
        # INSERT INTO tbl_cache ( Bestellnummer, Lieferant_Marke, aktiv, Lieferant, inquiryAmount )
        # SELECT tbl_Bestell_Nr.Bestellnummer, First(tbl_MakeCodes.code) AS Make_Code, tbl_Bestell_Nr.aktiv, tbl_Bestell_Nr.Lieferant, tbl_Artikel.TVH_Abfragemenge
        # FROM tbl_Artikel INNER JOIN (tbl_Bestell_Nr INNER JOIN tbl_MakeCodes ON tbl_Bestell_Nr.Lieferant_Marke = tbl_MakeCodes.descr) ON tbl_Artikel.Art_Nr_NuFa = tbl_Bestell_Nr.NuFa_Artikel
        # GROUP BY tbl_Bestell_Nr.Bestellnummer, tbl_Bestell_Nr.aktiv, tbl_Bestell_Nr.Lieferant, tbl_Artikel.TVH_Abfragemenge
        # HAVING (((tbl_Bestell_Nr.aktiv)=True) AND ((tbl_Bestell_Nr.Lieferant)=1));
        # """
        # cur.execute(sql_string)
        # conn.commit()

        cur.close()
        conn.close()
        return True

    except Exception as e:
        print("Error insert_into_table_cache")
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
        print("Error delete_from_table_cache")
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
        print("Error select_from_table_cache")
        print(f"Error: {e}")
        return False


def update_json_strings_in_cache(updates, price, listPrice, availability_code):
    conn = get_db()
    cur = conn.cursor()
    for lieferant_marke, bestellnummer, json_string, json_response in updates:
        cur.execute("""UPDATE tbl_cache 
        SET json_string = ?, 
        json_response = ?, 
        price = ?, 
        listPrice = ?,
        availabilityCode = ?,
        Datum = ?
        WHERE Lieferant_Marke = ? AND Bestellnummer = ?""", (json_string, json_response, price, listPrice, availability_code, current_date, lieferant_marke, bestellnummer))
        conn.commit()

    cur.close()
    conn.close()

    return



if __name__ == "__main__":
    delete_all_table_cache()