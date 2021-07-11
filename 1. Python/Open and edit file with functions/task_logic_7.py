
def drukat(fpath):
    f = open(fpath, "r", encoding="utf-8")
    print(f"Studentu saraksts ir: \n{f.read()}")
    f.close()


def pievieno(fpath):
    f = open(fpath, "a", encoding="utf-8")
    x = input("Ievadi studenta vārdu ")
    if not str(x):
        print("Nepareiza vērtība")
        return
    else:
        f.write(f"\n{x}")
    f.close()
    f = open(fpath, "r", encoding="utf-8")
    print(f"Jaunais studentu saraksts ir: \n{f.read()}")
    f.close()



def dzes_pec_indeksa(fpath):
    f = open(fpath, "r", encoding="utf-8")
    file_list = f.readlines()
    f.close()
    x = int(input("Ieraksti studenta kārtas numuru, sākot no 1."))
    if not int(x):
        print("Ievadīta nepreiza vērtība, izvēlies kārtas numuru")
        return
    else:
        file_list.pop(x-1)
    f = open(fpath, "w", encoding="utf-8")
    f.writelines(file_list)
    f.close()
    f = open(fpath, "r", encoding="utf-8")
    print(f"Jaunais studentu saraksts ir: \n{f.read()}")
    f.close()



def dzes_pec_varda(fpath):
    f = open(fpath, "r", encoding="utf-8")
    file_list = []
    for line in f:
        line = line.strip()
        file_list.append(line) #new line noņemšana
    f.close()
    x = input("Ieraksti studenta vārdu ").capitalize()
    if not str(x):
        print("Ievadīta nepreiza vērtība, izvēlies vārdu")
        return
    elif x in file_list:
        file_list.remove(x)
    else:
        print("Nav šāda vārda sarakstā")
    f = open(fpath, "w", encoding="utf-8")
    f.write('\n'.join(file_list))
    f.close()
    f = open(fpath, "r", encoding="utf-8")
    print(f"Jaunais studentu saraksts ir: \n{f.read()}")
    f.close()



def mekle(fpath):
    f = open(fpath, "r", encoding="utf-8")
    file_list = []
    for line in f:
        line = line.strip()
        file_list.append(line) #new line noņemšana
    f.close()
    found = False
    x = input("Ievadi studenta vārdu ").capitalize()
    for i in range(len(file_list)):
        if x == file_list[i]:
            print(f"Indekss ir {i}")
            found = True
    if not found:
        print("Saraksta sadas vertibas nav")
    f.close()