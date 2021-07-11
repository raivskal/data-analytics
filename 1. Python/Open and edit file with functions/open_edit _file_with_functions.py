import task_logic_7 as lo

#izmantoju atrasanas vietu uz diska
filepath = ("C:/Python/example_file_7.txt")
nosacijums = True
while nosacijums:
    izvele = input("Izvēlies darbību ar ciparu:\n1.Izvadīt studentu sarakstu.\n2.Ievadi jaunā studenta vārdu:\n3.Izdzēst studentu no saraksta pēc indeksa.\n4.Izdzēst studentu no saraksta pēc vērtības.\n5.Atrast studenta indeksu pēc studenta vārda\n")
    if izvele == "1":
        lo.drukat(filepath)
    elif izvele == "2":
        lo.pievieno(filepath)
    elif izvele == "3":
        lo.dzes_pec_indeksa(filepath)
    elif izvele == "4":
        lo.dzes_pec_varda(filepath)
    elif izvele == "5":
        lo.mekle(filepath)
    else:
        print("Nav ievadīta pareizā izvēle") 

    mainigais = input ("Turpināt? y/n ")
    if mainigais == "y":
        nosacijums = True
        continue
    elif mainigais == "n":
        nosacijums = False