def saskaita(fails):
    skaitlu_daudzums = 0
    kopa = 0
    list1 = []
    f = open(fails, "r", encoding="utf-8")
    for line in f:
        line = line.strip()
        line = line.split(",")
        list1.append(line) #new line noņemšana   
    print(list1)
    for linija in list1:
        skaitlu_daudzums += len(linija)
        liniju_summa = 0
        for skaitlis in linija:   
            liniju_summa += float(skaitlis)
        print(f"Summa ir {liniju_summa}. Vidējais ir {round(float(liniju_summa) / float(len(linija)),2)}")
        kopa+=liniju_summa
    avg_size = round(float(kopa) / float(skaitlu_daudzums),2)
    print(f"Kopējā summa ir {round(kopa,2)}. Vidējais ir {avg_size}")
  
    f.close()


saskaita("uzd8_2.txt")