import time
import sqlite3
import os
import categorie
import spese
import budget
import menureport


connection = sqlite3.connect("../sql/spese.db")

cursor = connection.cursor()

#tabelle
cursor.execute('''
CREATE TABLE IF NOT EXISTS categorie (
    id INTEGER PRIMARY KEY AUTOINCREMENT,               -- Vincolo PRIMARY KEY
    nomecat TEXT NOT NULL UNIQUE,                       -- Vincoli NOT NULL e UNIQUE
    
    -- Vincolo CHECK: impedisce l'inserimento di nomi vuoti o composti da soli spazi
    CONSTRAINT chk_nome_non_vuoto CHECK (length(trim(nomecat)) > 0)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS spese (
    id INTEGER PRIMARY KEY AUTOINCREMENT,               -- Vincolo PRIMARY KEY
    data TEXT NOT NULL,                                 -- Vincolo NOT NULL (Formato YYYY-MM-DD)
    importo REAL NOT NULL,                              -- Vincolo NOT NULL
    categoria_id INTEGER NOT NULL,                      -- Vincolo NOT NULL
    descrizione TEXT,                                   -- Campo facoltativo (può essere NULL)
    
    -- Vincolo CHECK: l'importo deve essere strettamente maggiore di zero (es. blocca -14)
    CONSTRAINT chk_importo_spesa_positivo CHECK (importo > 0),
    
    -- Vincolo CHECK: garantisce la consistenza formale della data (esattamente 10 caratteri)
    CONSTRAINT chk_formato_data_spesa CHECK (data LIKE '____-__-__'),
    
    -- Vincolo FOREIGN KEY: garantisce l'integrità referenziale verso la tabella categorie
    CONSTRAINT fk_spese_categoria 
        FOREIGN KEY (categoria_id) REFERENCES categorie(id)
        ON DELETE RESTRICT ON UPDATE CASCADE
)
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS budget (
        data TEXT NOT NULL,
        categoria_id INTEGER,
        importo REAL NOT NULL,
        PRIMARY KEY("data","categoria_id","categoria_id"),
        -- Vincolo CHECK: l'importo del budget stanziato deve essere positivo
    CONSTRAINT chk_importo_positivo CHECK (importo > 0),
    
    -- Vincolo CHECK: garantisce la consistenza formale del mese (esattamente 7 caratteri)
    CONSTRAINT chk_formato_data_budget CHECK (data LIKE '____-__'),
    
    -- Vincolo FOREIGN KEY: garantisce l'integrità referenziale verso la tabella categorie
    CONSTRAINT fk_budget_categoria 
        FOREIGN KEY (categoria_id) REFERENCES categorie(id)
        ON DELETE CASCADE ON UPDATE CASCADE,
        
    -- Vincolo UNIQUE composto: impedisce di definire più di un budget per lo stesso mese sulla stessa categoria
    CONSTRAINT uq_mese_categoria UNIQUE (data, categoria_id)
)
''')

connection.commit()

def mostra_menu():
    print("")
    print("-----------------------")
    print("SISTEMA SPESE PERSONALI")
    print("-----------------------")
    print("1. Gestione Categorie")
    print("2. Inserisci Spesa")
    print("3. Definisci Budget Mensile")
    print("4. Visualizza Report")
    print("5. Esci")
    print("-----------------------")
    #print("Inserisci la tua scelta:")

while True:
    os.system('cls||clear')
    mostra_menu()

    scelta = input("Scegli un'opzione (1-5): ")
    match scelta:
        case '1':
            categorie.inserisci_categorie()
        case '2':
            spese.inserisci_spesa()
        case '3':
            budget.inserisci_budget()
        case '4':
            menureport.mostra_menureport()
        case '5':
            print("Uscita dal programma. Arrivederci!")
            time.sleep(1)
            break
        case _:
            print ("scelta non valida. Riprovare\a")
            time.sleep(1)

