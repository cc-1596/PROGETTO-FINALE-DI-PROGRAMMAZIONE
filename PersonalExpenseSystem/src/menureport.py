import time
import os
import stampa1
import stampa2
import stampa3

def mostra_menureport():
    while True:
        os.system('cls||clear')

        print("")
        print("-----------------------")
        print("MENU' DEI REPORT")
        print("-----------------------")
        print("1. Totale spese per categoria")
        print("2. Spese mensili vs budget")
        print("3. Elenco completo delle spese ordinate per data")
        print("4. Ritorna al menu principale")
        print("-----------------------")


        scelta = input("Scegli un'opzione (1-4): ")
        match scelta:
            case '1':
                stampa1.stampa_1()
                #categorie.inserisci_categorie()
            case '2':
                stampa2.report_spese_vs_budget()
                #spese.inserisci_spesa()
            case '3':
                stampa3.elenco_spese()
            case '4':
                #print("Uscita dal programma. Arrivederci!")
                #time.sleep(1)
                break
            case _:
                print ("scelta non valida. Riprovare\a")
                time.sleep(1)