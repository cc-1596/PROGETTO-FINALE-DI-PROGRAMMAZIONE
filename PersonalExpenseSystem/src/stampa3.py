import sqlite3
import os

def elenco_spese():
    connection = sqlite3.connect("../sql/spese.db")
    cursor = connection.cursor()

    os.system('cls||clear')
    print("--- Elenco Spese ---\n")

    sql_report = '''
        SELECT data, nomecat, importo, descrizione
        FROM spese
        JOIN categorie ON categorie.id = spese.categoria_id
        ORDER BY data DESC, nomecat ASC
    '''
    
    cursor.execute(sql_report)
    rows = cursor.fetchall()

    if not rows:
        print("[Avviso]: Non ci sono dati da stampare.")
        connection.close()
        scelta = input("\npremi invio per continuare")
        return

    # Iteriamo tra i risultati trovati nel database
    for row in rows:
        data = row[0]
        categoria = row[1]
        importo = row[2]
        note = row[3]

        # 3. Visualizzazione dello stato (Output)
        print(f"data: {data}")
        print(f"Categoria: {categoria}")
        print(f"importo: {importo}")
        print(f"descrizione: {note}")
        print("-" * 30)

    connection.close()
    scelta = input("\npremi invio per continuare")