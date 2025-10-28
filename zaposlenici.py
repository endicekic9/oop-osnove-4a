class Zaposlenik:
    def __init__(self, ime, prezime, placa):
        self.ime = ime
        self.prezime = prezime
        self.placa = placa
    def prikaz_info(self):
        print(f"Ime i prezime: {self.ime} {self.prezime}, Plaća: {self.placa} EUR")
class Programer(Zaposlenik):
    def __init__(self, ime, prezime, placa, programski_jezik):
        super().__init__(ime, prezime, placa)
        self.programski_jezik = programski_jezik
    def prikaz_info(self):
        super().prikaz_info()
        print(f'Programski jezik/ci: {", ".join(self.programski_jezik)}')
class Menadzer(Zaposlenik):
    def __init__(self, ime, prezime, placa, tim):
        super().__init__(ime, prezime, placa)
        self.tim = tim
    def prikaz_info(self):
        super().prikaz_info()
        print(f'Tim: {", ".join(self.tim)}')
#Primjer korištenja
z1 = Zaposlenik("Ana", "Anić", 1200)
p1 = Programer("Petar", "Perić", 1800, ["Python", "JavaScript"])
m1 = Menadzer("Iva", "Ivić", 2500, ["Ana Anić", "Petar Perić"])

print("--- Podaci o zaposleniku ---")
z1.prikaz_info()
print("\n--- Podaci o programeru ---")
p1.prikaz_info()
print("\n--- Podaci o menadžeru ---")
m1.prikaz_info()