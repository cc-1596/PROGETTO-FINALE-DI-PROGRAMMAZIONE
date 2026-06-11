import sqlite3
import os
from datetime import datetime

def inserisci_spesa():
    connection = sqlite3.connect("../sql/spese.db")
    cursor = connection.cursor()

    os.system('cls||clear')
    print("--- Inserimento di una Spesa ---\n")

    cursor.execute("SELECT nomecat FROM categorie ORDER BY nomecat ASC")
    categorie_salvate = cursor.fetchall()
    print("Categorie disponibili nel sistema:")
    if not categorie_salvate:
        print("  [Nessuna categoria presente. Crea prima una categoria nel Modulo 1!]")
        print("-------------------------------------------------------------------")
        connection.close()
        scelta = input("\npremi invio per continuare")
        return
    else:
        nomi_cat = [cat[0] for cat in categorie_salvate]
        print("  > " + ", ".join(nomi_cat))
        print("-------------------------------------------------------------------\n")  

    #Input data
    while True:
        data_input = input("Inserisci la data (YYYY-MM-DD) [Premi INVIO per OGGI]: ").strip()

        if data_input == "":
            data_input = datetime.today().strftime('%Y-%m-%d')
            break

        try:
            # %Y = anno, %m = mese, %d = giorno
            datetime.strptime(data_input, "%Y-%m-%d")
            break  
        except ValueError:
            print("[Errore]: Data non valida. Usa il formato YYYY-MM-DD (es. 2026-06-10).\n")

        
    while True:
        try:
            importo = float(input("Inserisci l'importo (€) o 0 per uscire: ").strip().replace(',', '.'))
        except ValueError:
            print("[Errore]: L'importo inserito non è un numero valido.\n")
            importo = -1
        if importo == 0:
            return
        if importo < 0:
            print("[Errore]: L'importo deve essere maggiore di zero.\n")
        else:
            break
            
    while True:    
        categoria = input("Inserisci il nome della categoria o enter per uscire: ").strip()
        if categoria == "":
            return
        cursor.execute("SELECT id FROM categorie WHERE LOWER(nomecat) = LOWER(?)", (categoria,))
        risultato = cursor.fetchone()
        if not risultato:
            print(f"\n[Errore]: La categoria '{categoria}' non esiste. Creala prima nel Modulo 1.")
        else:
            categoria_id = risultato[0]
            break
        
    descrizione = input("Inserisci una descrizione (facoltativa): ").strip()

    sql_insert = '''
        INSERT INTO spese (data, importo, categoria_id, descrizione) 
        VALUES (?, ?, ?, ?)
    '''

    cursor.execute(sql_insert, (data_input, importo, categoria_id, descrizione))
    connection.commit()

    print(f"\n[Successo]: Spesa di {importo:.2f}€ inserita correttamente in '{categoria}'.")

    connection.close()