import sqlite3
import time
import os

def inserisci_categorie():

    connection = sqlite3.connect("../sql/spese.db")

    cursor = connection.cursor()
    os.system('cls||clear')
    #estraggo dal database tutte le categorie ordinate per nome
    cursor.execute("SELECT nomecat FROM categorie ORDER BY nomecat ASC")
    categorie_salvate = cursor.fetchall()
    print("Categorie disponibili nel sistema:")
    if not categorie_salvate:
        print("Nessuna categoria presente\n")
    else:
        # Estraiamo i nomi dalle tuple e li uniamo separati da una virgola
        nomi_cat = [cat[0] for cat in categorie_salvate]
        print("  > " + ", ".join(nomi_cat))
        print("-------------------------------------------------------------------\n")

    scelta = input("Inserisci il nome della categoria: ").strip()

    if scelta == "":
        print("\n[Errore]: Il nome della categoria non può essere vuoto.")
    else:
        sql_select = "SELECT * FROM categorie WHERE LOWER(nomecat) = LOWER(?)"

        cursor.execute(sql_select,(scelta,))
        rows = cursor.fetchall()
        if rows:
            print (f"[Errore]: La categoria '{scelta}' esiste già.")
        else:
            sql_insert = "INSERT INTO categorie (nomecat) VALUES (?)"
            cursor.execute(sql_insert, (scelta,))
            connection.commit()
            print(f"\n[Successo]: Categoria '{scelta}' inserita correttamente.")
    time.sleep(1)

            
    connection.close()
    