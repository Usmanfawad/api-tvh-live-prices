from App.db.session import get_db, exec_query

import os
from dotenv import load_dotenv

from datetime import datetime

current_date = datetime.now().strftime('%d/%m/%Y')
print(type(current_date))
load_dotenv()
DBNAME = os.getenv("DATABASE_TYPE")

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
        conn.autocommit = True
        cur = conn.cursor()

        # Select from tbl_Bestellnummer
        select_query = "SELECT Bestellnummer, Lieferant, NuFa_Artikel, Lieferant_Marke, aktiv FROM tbl_Bestell_Nr WHERE aktiv='WAHR' AND Lieferant=1"

        # Execute the query
        cur.execute(select_query)

        # Fetch all rows from the result set
        rows = cur.fetchall()

        if DBNAME == "msaccess":
            unique_combinations = set()
            vaLues_to_insert = []

            # Insert data into tbl_cache
            insert_query = "INSERT INTO tbl_cache (Bestellnummer, Lieferant, Lieferant_Marke, aktiv) VALUES (?, ?, ?, ?)"

            # Extract data for unique combinations
            unique_rows = {tuple(row) for row in rows}
            data_to_insert = [(row[0], row[1], row[3], row[4]) for row in unique_rows]

            # Insert data in batches
            cur.executemany(insert_query, data_to_insert)

            cur.close()
            conn.close()
            return True

        else:  
            # Insert data into tbl_cache
            insert_query = "INSERT INTO tbl_cache (Bestellnummer, Lieferant, Lieferant_Marke, aktiv) VALUES (%s, %s, %s, %s)"
            vaLues_to_insert = []
            unique_combinations = set()

            for row in rows:
                combination = (row[0], row[3])

                if combination not in unique_combinations:
                    unique_combinations.add(combination)
                    vaLues_to_insert.append((row[0], row[1], row[3], row[4]))

            cur.executemany(insert_query, vaLues_to_insert)



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
        # for each in rows:
        #     print(each)
        cur.close()
        return rows

    except Exception as e:
        print("Error select_from_table_cache")
        print(f"Error: {e}")
        return False


def update_json_strings_in_cache(updates, price, listPrice, availability_code):
    conn = get_db()
    cur = conn.cursor()

    if DBNAME == 'msaccess':

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
    else:

        for lieferant_marke, bestellnummer, json_string, json_response in updates:
            cur.execute("""UPDATE tbl_cache 
            SET json_string = %s, 
            json_response = %s, 
            price = %s, 
            listPrice = %s,
            availabilityCode = %s,
            Datum = %s
            WHERE Lieferant_Marke = %s AND Bestellnummer = %s""", (json_string, json_response, price, listPrice, availability_code, current_date, lieferant_marke, bestellnummer))
            conn.commit()

    cur.close()
    conn.close()

    return



if __name__ == "__main__":
    delete_all_table_cache()