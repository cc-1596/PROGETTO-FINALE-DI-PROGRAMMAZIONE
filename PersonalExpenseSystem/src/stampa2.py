import sqlite3
import os

def report_spese_vs_budget():
    connection = sqlite3.connect("../sql/spese.db")
    cursor = connection.cursor()

    os.system('cls||clear')
    print("--- Spese Mensili vs Budget ---\n")

    # 1. Calcolo del totale speso per mese e categoria (SQL)
    # Questa query unisce i Budget alle Spese effettive, raggruppandole per mese e categoria
    sql_report = '''
        SELECT strftime('%Y-%m',spese.data) as mese, nomecat, COALESCE(SUM(spese.importo), 0) AS totale_speso, budget.importo
        FROM spese
        JOIN categorie ON categorie.id = spese.categoria_id
        JOIN budget ON budget.data = strftime('%Y-%m',spese.data) and budget.categoria_id = spese.categoria_id
        GROUP BY strftime('%Y-%m',spese.data), spese.categoria_id
        ORDER BY strftime('%Y-%m',spese.data) DESC, nomecat ASC
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
        mese = row[0]
        categoria = row[1]
        budget = row[3]
        speso = row[2]

        # 2. Confronto con il budget tramite if / else
        if speso > budget:
            stato = "SUPERAMENTO BUDGET"
        elif speso == budget:
            stato = "BUDGET RAGGIUNTO"
        else:
            stato = "ENTRO IL BUDGET"

        # 3. Visualizzazione dello stato (Output)
        print(f"Mese: {mese}")
        print(f"Categoria: {categoria}")
        print(f"Budget: {budget:.2f} €")
        print(f"Speso: {speso:.2f} €")
        print(f"Stato: {stato}")
        print("-" * 30)

    connection.close()
    scelta = input("\npremi invio per continuare")