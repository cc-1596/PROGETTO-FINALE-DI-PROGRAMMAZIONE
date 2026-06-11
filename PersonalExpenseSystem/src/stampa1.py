import sqlite3
import time
import os

def stampa_1():

    connection = sqlite3.connect("../sql/spese.db")

    cursor = connection.cursor()
    os.system('cls||clear')
    #estraggo dal database tutte le categorie ordinate per nome
    cursor.execute("select nomecat, sum(importo) as totale from spese inner join categorie on categorie.id=spese.categoria_id group by categoria_id")
    spese = cursor.fetchall()
    print("Totale delle Spese per Categoria\n")
    if not spese:
        print("Nessuna spesa presente\n")
    else:
        # Estraiamo i nomi dalle tuple e li uniamo separati da una virgola
        #nomi_cat = [cat[0] for cat in spese]
        for cat in spese:
            nome = cat[0]
            valore = cat[1]
            
            print(nome.ljust(30,'.') + str(valore).rjust(5))
    scelta = input("\npremi invio per continuare")
    