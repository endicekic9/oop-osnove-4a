class Učenik:
    def __init__(self, ime, prezime, razred):
        self.ime = ime
        self.prezime = prezime
        self.razred = razred
    def dodaj_ocjenu(self, ocjena):
        self.ocjene=[]
        self.ocjene.append(ocjena)
    def prosjek(self):
        if self.ocjene==[]:
            return 0
        return sum(self.ocjene)/len(self.ocjene)
    def info(self):
        return f"{self.ime} {self.prezime}, Razred: {self.razred}, Prosjek ocjena: {self.prosjek():.2f}"
#Primjer1
ucenik1 = Učenik("Ivan", "Ivić", "2a")
ucenik1.dodaj_ocjenu(4)
ucenik1.dodaj_ocjenu(5)
ucenik1.dodaj_ocjenu(2)
#Primjer2
ucenik2 = Učenik("Ana", "Anić", "4a")
ucenik2.dodaj_ocjenu(5)
ucenik2.dodaj_ocjenu(2)
ucenik2.dodaj_ocjenu(4)
print(ucenik1.info())
print(ucenik2.info())