from App.db.session import get_db, exec_query

ACCESS_DATABASE_URL = r'C:\NextRevol\NufaersatzteileProject\App\db\NuFa.accdb'
f'DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={ACCESS_DATABASE_URL};'



def update_json_strings_in_cache(updates, price, listPrice):

    conn = get_db()
    cur = conn.cursor()
    for lieferant_marke, bestellnummer, json_string, json_response in updates:
        cur.execute("""UPDATE tbl_cache 
        SET json_string = ?, 
        json_response = ?, 
        price = ?, 
        listPrice = ? 
        WHERE Lieferant_Marke = ? AND Bestellnummer = ?""", (json_string, json_response, price, listPrice, lieferant_marke, bestellnummer))
        conn.commit()

    cur.close()
    conn.close()

    return



if __name__ == "__main__":
    delete_all_table_cache()