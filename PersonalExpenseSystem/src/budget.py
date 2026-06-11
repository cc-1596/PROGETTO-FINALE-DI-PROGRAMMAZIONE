import sqlite3
import os
from datetime import datetime

def inserisci_budget():
    connection = sqlite3.connect("../sql/spese.db")
    cursor = connection.cursor()

    os.system('cls||clear')
    print("--- Inserimento di un Budget ---\n")
    #mostra categorie esistenti
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
    #fine mostra categorie esistenti
    while True:
        data_input = input("Inserisci il mese (YYYY-MM) [Premi INVIO per OGGI]: ").strip()

        # Gestione dell'invio a vuoto (Imposta il mese corrente)
        if data_input == "":
            data_input = datetime.today().strftime('%Y-%m')
            break  
            # Data di oggi è sicuramente valida, usciamo dal ciclo

        # Controllo validità del formato e del calendario
        try:
            # %Y = anno a 4 cifre, %m = mese a 2 cifre
            datetime.strptime(data_input, "%Y-%m")
            break  
            # Se non dà errore, la data è valida! Usciamo dal ciclo
        except ValueError:
            print("[Errore]: Formato data non valido o mese inesistente. Usa il formato YYYY-MM (es. 2026-06).\n")
    
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
    
    #Leggo dal database per vedere se già esiste il budget richiesto
    
    cursor.execute("SELECT importo FROM budget WHERE data = ? and categoria_id = ?", (data_input, categoria_id,))
    ris = cursor.fetchone()
    if not ris:
        importo=0
    else:
        importo = ris[0]
        
    #
    
    while True:
        try:
            importo = float(input(f"Inserisci l'importo valore attuale: {importo} 0 per non cambiare ed uscire ").strip().replace(',', '.'))
        except ValueError:
            print("[Errore]: L'importo inserito non è un numero valido.\n")
            importo = -1
        if importo == 0:
            return
        if importo < 0:
            print("[Errore]: L'importo deve essere maggiore di zero.\n")
        else:
            break
            
    if not ris:
        sql = '''
        INSERT INTO budget (data, categoria_id, importo) 
        VALUES (?, ?, ?)
    '''
        cursor.execute(sql, (data_input, categoria_id, importo))
        
    else:
        sql = "UPDATE budget set importo = ? WHERE data = ? and categoria_id = ? "

        cursor.execute(sql, (importo, data_input, categoria_id))
    connection.commit()

    print(f"\n[Successo]: Spesa di {importo:.2f}€ inserita correttamente in '{categoria}'.")
    
    connection.close()    
    scelta = input("\npremi invio per continuare")