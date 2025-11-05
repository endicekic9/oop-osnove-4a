import tkinter as tk
import csv
import xml.etree.ElementTree as ET


class Vozilo:
    def __init__(self, marka, model, godina_proizvodnje, novo, boja, snaga_motora, naprodaji, cijena):
        self.marka = marka
        self.model = model
        self.godina_proizvodnje = godina_proizvodnje
        self.novo =bool(novo)
        self.boja = boja
        self.snaga_motora = snaga_motora
        self.naprodaji = naprodaji
        self.cijena = cijena
class Automobil(Vozilo):
    def __init__(self, marka, model, godina_proizvodnje, novo, boja, snaga_motora, naprodaji, cijena, broj_vrata, tip_goriva):
        super().__init__(marka, model, godina_proizvodnje, novo, boja, snaga_motora, naprodaji, cijena)
        self.broj_vrata = broj_vrata
        self.tip_goriva = tip_goriva
class Motocikl(Vozilo):
    def __init__(self, marka, model, godina_proizvodnje, novo, boja, snaga_motora, naprodaji, cijena, tip_motocikla):
        super().__init__(marka, model, godina_proizvodnje, novo, boja, snaga_motora, naprodaji, cijena)
        self.tip_motocikla = tip_motocikla
class Prikaz_lagera:
    def __init__(self, root):
        self.root = root
        self.root.title("Lager vozila")
        self.root.geometry("1400x600")

        self.automobili = []
        self.motocikli = []
        self.odabrano_vozilo = None

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        unos_frame = tk.Frame(self.root, padx=10, pady=10)
        unos_frame.grid(row=0, column=0, sticky="EW")

        prikaz_frame = tk.Frame(self.root, padx=10, pady=10)
        prikaz_frame.grid(row=1, column=0, sticky="NSEW")

        prikaz_frame.columnconfigure(0, weight=1)
        prikaz_frame.rowconfigure(0, weight=1)

        tk.Label(unos_frame, text="Marka:").grid(row=1, column=0, padx=5, pady=5, sticky="W")
        self.marka_entry = tk.Entry(unos_frame)
        self.marka_entry.grid(row=1, column=1, padx=5, pady=5, sticky="EW")

        tk.Label(unos_frame, text="Model:").grid(row=1, column=2, padx=5, pady=5, sticky="W")
        self.model_entry = tk.Entry(unos_frame)
        self.model_entry.grid(row=1, column=3, padx=5, pady=5, sticky="EW")

        tk.Label(unos_frame, text="Godina proizvodnje:").grid(row=1, column=4, padx=5, pady=5, sticky="W")
        self.godina_entry = tk.Entry(unos_frame)
        self.godina_entry.grid(row=1, column=5, padx=5, pady=5, sticky="EW")

        tk.Label(unos_frame, text="Novo (1/0):").grid(row=1, column=6, padx=5, pady=5, sticky="W")
        self.novo_entry = tk.Entry(unos_frame)
        self.novo_entry.grid(row=1, column=7, padx=5, pady=5, sticky="EW")

        tk.Label(unos_frame, text="Boja:").grid(row=2, column=0, padx=5, pady=5, sticky="W")
        self.boja_entry = tk.Entry(unos_frame)
        self.boja_entry.grid(row=2, column=1, padx=5, pady=5, sticky="EW")

        tk.Label(unos_frame, text="Snaga motora (KS):").grid(row=2, column=2, padx=5, pady=5, sticky="W")
        self.snaga_entry = tk.Entry(unos_frame)
        self.snaga_entry.grid(row=2, column=3, padx=5, pady=5, sticky="EW")

        tk.Label(unos_frame, text="Na prodaji (Da/Ne):").grid(row=2, column=4, padx=5, pady=5, sticky="W")
        self.naprodaji_entry = tk.Entry(unos_frame)
        self.naprodaji_entry.grid(row=2, column=5, padx=5, pady=5, sticky="EW")

        tk.Label(unos_frame, text="Cijena (EUR):").grid(row=2, column=6, padx=5, pady=5, sticky="W")
        self.cijena_entry = tk.Entry(unos_frame)
        self.cijena_entry.grid(row=2, column=7, padx=5, pady=5, sticky="EW")

        tk.Label(unos_frame, text="Broj vrata (za automobile):").grid(row=3, column=0, padx=5, pady=5, sticky="W")
        self.broj_vrata_entry = tk.Entry(unos_frame)
        self.broj_vrata_entry.grid(row=3, column=1, padx=5, pady=5, sticky="EW")

        tk.Label(unos_frame, text="Tip goriva (za automobile):").grid(row=3, column=2, padx=5, pady=5, sticky="W")
        self.tip_goriva_entry = tk.Entry(unos_frame)
        self.tip_goriva_entry.grid(row=3, column=3, padx=5, pady=5, sticky="EW")
        tk.Label(unos_frame, text="Tip motocikla (za motocikle):").grid(row=3, column=4, padx=5, pady=5, sticky="W")
        self.tip_motocikla_entry = tk.Entry(unos_frame)
        self.tip_motocikla_entry.grid(row=3, column=5, padx=5, pady=5, sticky="EW")

        self.dodaj_auto_button = tk.Button(unos_frame, text="Dodaj automobil", command=self.dodaj_automobil)
        self.dodaj_auto_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="EW")

        self.dodaj_moto_button = tk.Button(unos_frame, text="Dodaj motocikl", command=self.dodaj_motocikl)
        self.dodaj_moto_button.grid(row=4, column=2, columnspan=2, padx=5, pady=5, sticky="EW")

        self.spremi_izmjene_button = tk.Button(unos_frame, text="Spremi izmjene", command=self.spremi_izmjene)
        self.spremi_izmjene_button.grid(row=4, column=4, columnspan=2, padx=5, pady=5, sticky="EW")

        self.spremi_gumb_csv = tk.Button(unos_frame, text="Spremi u CSV", command=self.spremi_u_csv)
        self.spremi_gumb_csv.grid(row=4, column=6, columnspan=2, padx=5, pady=5, sticky="EW")
        self.spremi_gumb_xml = tk.Button(unos_frame, text="Spremi u XML", command=self.spremi_u_xml)
        self.spremi_gumb_xml.grid(row=4, column=8, columnspan=2, padx=5, pady=5, sticky="EW")

        self.učitaj_gumb_csv = tk.Button(unos_frame, text="Učitaj iz CSV", command=self.učitaj_iz_csv)
        self.učitaj_gumb_csv.grid(row=4, column=10, columnspan=2, padx=5, pady=5, sticky="EW")
        self.učitaj_gumb_xml = tk.Button(unos_frame, text="Učitaj iz XML", command=self.učitaj_iz_xml)
        self.učitaj_gumb_xml.grid(row=4, column=12, columnspan=2, padx=5, pady=5, sticky="EW")

        self.prikaz_vozila = tk.Listbox(prikaz_frame)
        self.prikaz_vozila.grid(row=0, column=0, sticky="NSEW")
        self.prikaz_vozila.bind("<<ListboxSelect>>", self.prikaz_odabranog_vozila)

        self.scrollbar = tk.Scrollbar(prikaz_frame, orient="vertical", command=self.prikaz_vozila.yview)
        self.scrollbar.grid(row=0, column=1, sticky="NS")
        self.prikaz_vozila.config(yscrollcommand=self.scrollbar.set)

    def dodaj_automobil(self):
        marka = self.marka_entry.get()
        model = self.model_entry.get()
        godina_proizvodnje = self.godina_entry.get()
        novo = self.novo_entry.get()
        boja = self.boja_entry.get()
        snaga_motora = self.snaga_entry.get()
        naprodaji = self.naprodaji_entry.get()
        cijena = self.cijena_entry.get()
        broj_vrata = self.broj_vrata_entry.get()
        tip_goriva = self.tip_goriva_entry.get()

        automobil = Automobil(marka, model, godina_proizvodnje, novo, boja, snaga_motora, naprodaji, cijena, broj_vrata, tip_goriva)
        self.automobili.append(automobil)
        self.osvjezi_prikaz()
        self.ocisti_unos_polja()
    def dodaj_motocikl(self):
        marka = self.marka_entry.get()
        model = self.model_entry.get()
        godina_proizvodnje = self.godina_entry.get()
        novo = self.novo_entry.get()
        boja = self.boja_entry.get()
        snaga_motora = self.snaga_entry.get()
        naprodaji = self.naprodaji_entry.get()
        cijena = self.cijena_entry.get()
        tip_motocikla = self.tip_motocikla_entry.get()

        motocikl = Motocikl(marka, model, godina_proizvodnje, novo, boja, snaga_motora, naprodaji, cijena, tip_motocikla)
        self.motocikli.append(motocikl)
        self.osvjezi_prikaz()
        self.ocisti_unos_polja()
    def osvjezi_prikaz(self):
        self.prikaz_vozila.delete(0, tk.END)
        for auto in self.automobili:
            self.prikaz_vozila.insert(tk.END, f"Auto: {auto.marka} {auto.model} ({auto.godina_proizvodnje}) - {auto.cijena} EUR")
        for moto in self.motocikli:
            self.prikaz_vozila.insert(tk.END, f"Moto: {moto.marka} {moto.model} ({moto.godina_proizvodnje}) - {moto.cijena} EUR")
    def ocisti_unos_polja(self):
        self.marka_entry.delete(0, tk.END)
        self.model_entry.delete(0, tk.END)
        self.godina_entry.delete(0, tk.END)
        self.novo_entry.delete(0, tk.END)
        self.boja_entry.delete(0, tk.END)
        self.snaga_entry.delete(0, tk.END)
        self.naprodaji_entry.delete(0, tk.END)
        self.cijena_entry.delete(0, tk.END)
        self.broj_vrata_entry.delete(0, tk.END)
        self.tip_goriva_entry.delete(0, tk.END)
        self.tip_motocikla_entry.delete(0, tk.END)
    def odaberi_vozilo(self, index):
        index=self.listbox.curselection()[0]
        if index:
            self.odabrano_vozilo_index=index[0]
            vozilo=self.vozilo[self.odabrano_vozilo_index]
            self.marka_entry.delete(0,tk.END)
            self.marka_entry.insert(0,vozilo.marka)
            self.model_entry.delete(0,tk.END)
            self.model_entry.insert(0,vozilo.model)
            self.godina_entry.delete(0,tk.END)
            self.godina_entry.insert(0,vozilo.godina_proizvodnje)
            self.novo_entry.delete(0,tk.END)
            self.novo_entry.insert(0,str(int(vozilo.novo)))
            self.boja_entry.delete(0,tk.END)
            self.boja_entry.insert(0,vozilo.boja)
            self.snaga_entry.delete(0,tk.END)
            self.snaga_entry.insert(0,vozilo.snaga_motora)
            self.naprodaji_entry.delete(0,tk.END)
            self.naprodaji_entry.insert(0,vozilo.naprodaji)
            self.cijena_entry.delete(0,tk.END)
            self.cijena_entry.insert(0,vozilo.cijena)
    def prikaz_odabranog_vozila(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            ukupno_automobila = len(self.automobili)
            if index < ukupno_automobila:
                vozilo = self.automobili[index]
                self.odabrano_vozilo = vozilo
                self.popuni_unos_polja_automobil(vozilo)
            else:
                vozilo = self.motocikli[index - ukupno_automobila]
                self.odabrano_vozilo = vozilo
                self.popuni_unos_polja_motocikl(vozilo)
    def popuni_unos_polja_automobil(self, automobil):
        self.marka_entry.delete(0, tk.END)
        self.marka_entry.insert(0, automobil.marka)
        self.model_entry.delete(0, tk.END)
        self.model_entry.insert(0, automobil.model)
        self.godina_entry.delete(0, tk.END)
        self.godina_entry.insert(0, automobil.godina_proizvodnje)
        self.novo_entry.delete(0, tk.END)
        self.novo_entry.insert(0, str(int(automobil.novo)))
        self.boja_entry.delete(0, tk.END)
        self.boja_entry.insert(0, automobil.boja)
        self.snaga_entry.delete(0, tk.END)
        self.snaga_entry.insert(0, automobil.snaga_motora)
        self.naprodaji_entry.delete(0, tk.END)
        self.naprodaji_entry.insert(0, automobil.naprodaji)
        self.cijena_entry.delete(0, tk.END)
        self.cijena_entry.insert(0, automobil.cijena)
        self.broj_vrata_entry.delete(0, tk.END)
        self.broj_vrata_entry.insert(0, automobil.broj_vrata)
        self.tip_goriva_entry.delete(0, tk.END)
        self.tip_goriva_entry.insert(0, automobil.tip_goriva)
    def popuni_unos_polja_motocikl(self, motocikl):
        self.marka_entry.delete(0, tk.END)
        self.marka_entry.insert(0, motocikl.marka)
        self.model_entry.delete(0, tk.END)
        self.model_entry.insert(0, motocikl.model)
        self.godina_entry.delete(0, tk.END)
        self.godina_entry.insert(0, motocikl.godina_proizvodnje)
        self.novo_entry.delete(0, tk.END)
        self.novo_entry.insert(0, str(int(motocikl.novo)))
        self.boja_entry.delete(0, tk.END)
        self.boja_entry.insert(0, motocikl.boja)
        self.snaga_entry.delete(0, tk.END)
        self.snaga_entry.insert(0, motocikl.snaga_motora)
        self.naprodaji_entry.delete(0, tk.END)
        self.naprodaji_entry.insert(0, motocikl.naprodaji)
        self.cijena_entry.delete(0, tk.END)
        self.cijena_entry.insert(0, motocikl.cijena)
        self.broj_vrata_entry.delete(0, tk.END)
        self.tip_goriva_entry.delete(0, tk.END)
        self.tip_motocikla_entry.delete(0, tk.END)
        self.tip_motocikla_entry.insert(0, motocikl.tip_motocikla)
    def spremi_izmjene(self):
        if self.odabrano_vozilo:
            self.odabrano_vozilo.marka = self.marka_entry.get()
            self.odabrano_vozilo.model = self.model_entry.get()
            self.odabrano_vozilo.godina_proizvodnje = self.godina_entry.get()
            self.odabrano_vozilo.novo = bool(self.novo_entry.get())
            self.odabrano_vozilo.boja = self.boja_entry.get()
            self.odabrano_vozilo.snaga_motora = self.snaga_entry.get()
            self.odabrano_vozilo.naprodaji = self.naprodaji_entry.get()
            self.odabrano_vozilo.cijena = self.cijena_entry.get()

            if isinstance(self.odabrano_vozilo, Automobil):
                self.odabrano_vozilo.broj_vrata = self.broj_vrata_entry.get()
                self.odabrano_vozilo.tip_goriva = self.tip_goriva_entry.get()
            elif isinstance(self.odabrano_vozilo, Motocikl):
                self.odabrano_vozilo.tip_motocikla = self.tip_motocikla_entry.get()

            self.osvjezi_prikaz()
            self.ocisti_unos_polja()
            self.odabrano_vozilo = None
    def spremi_u_csv(self):
        with open("lager_vozila.csv", mode="w", newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Tip", "Marka", "Model", "Godina proizvodnje", "Novo", "Boja", "Snaga motora", "Na prodaji", "Cijena", "Broj vrata", "Tip goriva", "Tip motocikla"])
            for auto in self.automobili:
                writer.writerow(["Automobil", auto.marka, auto.model, auto.godina_proizvodnje, auto.novo, auto.boja, auto.snaga_motora, auto.naprodaji, auto.cijena, auto.broj_vrata, auto.tip_goriva, ""])
            for moto in self.motocikli:
                writer.writerow(["Motocikl", moto.marka, moto.model, moto.godina_proizvodnje, moto.novo, moto.boja, moto.snaga_motora, moto.naprodaji, moto.cijena, "", "", moto.tip_motocikla])
    def učitaj_iz_csv(self):
        self.automobili.clear()
        self.motocikli.clear()
        with open("lager_vozila.csv", mode="r", newline='', encoding='utf-8') as file:
            for row in reader:
                if row["Tip"] == "Automobil":
                    automobil = Automobil(row["Marka"], row["Model"], row["Godina proizvodnje"], row["Novo"], row["Boja"], row["Snaga motora"], row["Na prodaji"], row["Cijena"], row["Broj vrata"], row["Tip goriva"])
                    self.automobili.append(automobil)
                elif row["Tip"] == "Motocikl":
                    motocikl = Motocikl(row["Marka"], row["Model"], row["Godina proizvodnje"], row["Novo"], row["Boja"], row["Snaga motora"], row["Na prodaji"], row["Cijena"], row["Tip motocikla"])
                    self.motocikli.append(motocikl)
        self.osvjezi_prikaz()
    def spremi_u_xml(self):
        filename = "lager_vozila.xml"
        root = ET.Element("Vozila")
        tree=ET.ElementTree(root)
        for auto in self.automobili:
            auto_elem=ET.SubElement(root, "Automobil")
            marka_elem=ET.SubElement(auto_elem, "Marka")
            marka_elem.text=auto.marka
            model_elem=ET.SubElement(auto_elem, "Model")
            model_elem.text=auto.model
            godina_elem=ET.SubElement(auto_elem, "GodinaProizvodnje")
            godina_elem.text=auto.godina_proizvodnje
            novo_elem=ET.SubElement(auto_elem, "Novo")
            novo_elem.text=str(auto.novo)
            boja_elem=ET.SubElement(auto_elem, "Boja")
            boja_elem.text=auto.boja
            snaga_elem=ET.SubElement(auto_elem, "SnagaMotora")
            snaga_elem.text=auto.snaga_motora
            naprodaji_elem=ET.SubElement(auto_elem, "NaProdaji")
            naprodaji_elem.text=auto.naprodaji
            cijena_elem=ET.SubElement(auto_elem, "Cijena")
            cijena_elem.text=auto.cijena
            broj_vrata_elem=ET.SubElement(auto_elem, "BrojVrata")
            broj_vrata_elem.text=auto.broj_vrata
            tip_goriva_elem=ET.SubElement(auto_elem, "TipGoriva")
            tip_goriva_elem.text=auto.tip_goriva
        for moto in self.motocikli:
            moto_elem=ET.SubElement(root, "Motocikl")
            marka_elem=ET.SubElement(moto_elem, "Marka")
            marka_elem.text=moto.marka
            model_elem=ET.SubElement(moto_elem, "Model")
            model_elem.text=moto.model
            godina_elem=ET.SubElement(moto_elem, "GodinaProizvodnje")
            godina_elem.text=moto.godina_proizvodnje
            novo_elem=ET.SubElement(moto_elem, "Novo")
            novo_elem.text=str(moto.novo)
            boja_elem=ET.SubElement(moto_elem, "Boja")
            boja_elem.text=moto.boja
            snaga_elem=ET.SubElement(moto_elem, "SnagaMotora")
            snaga_elem.text=moto.snaga_motora
            naprodaji_elem=ET.SubElement(moto_elem, "NaProdaji")
            naprodaji_elem.text=moto.naprodaji
            cijena_elem=ET.SubElement(moto_elem, "Cijena")
            cijena_elem.text=moto.cijena
            tip_motocikla_elem=ET.SubElement(moto_elem, "TipMotocikla")
            tip_motocikla_elem.text=moto.tip_motocikla
        tree.write(filename, encoding="utf-8", xml_declaration=True)
    def učitaj_iz_xml(self):
        self.automobili.clear()
        self.motocikli.clear()
        tree=ET.parse("lager_vozila.xml")
        root=tree.getroot()
        for auto_elem in root.findall("Automobil"):
            marka=auto_elem.find("Marka").text
            model=auto_elem.find("Model").text
            godina_proizvodnje=auto_elem.find("GodinaProizvodnje").text
            novo=auto_elem.find("Novo").text=="True"
            boja=auto_elem.find("Boja").text
            snaga_motora=auto_elem.find("SnagaMotora").text
            naprodaji=auto_elem.find("NaProdaji").text
            cijena=auto_elem.find("Cijena").text
            broj_vrata=auto_elem.find("BrojVrata").text
            tip_goriva=auto_elem.find("TipGoriva").text
            automobil=Automobil(marka, model, godina_proizvodnje, novo, boja, snaga_motora, naprodaji, cijena, broj_vrata, tip_goriva)
            self.automobili.append(automobil)
        for moto_elem in root.findall("Motocikl"):
            marka=moto_elem.find("Marka").text
            model=moto_elem.find("Model").text
            godina_proizvodnje=moto_elem.find("GodinaProizvodnje").text
            novo=moto_elem.find("Novo").text=="True"
            boja=moto_elem.find("Boja").text
            snaga_motora=moto_elem.find("SnagaMotora").text
            naprodaji=moto_elem.find("NaProdaji").text
            cijena=moto_elem.find("Cijena").text
            tip_motocikla=moto_elem.find("TipMotocikla").text
            motocikl=Motocikl(marka, model, godina_proizvodnje, novo, boja, snaga_motora, naprodaji, cijena, tip_motocikla)
            self.motocikli.append(motocikl)
        self.osvjezi_prikaz()
if __name__ == "__main__":
    root = tk.Tk()
    app = Prikaz_lagera(root)
    root.mainloop() #prikaz nije cjelovit, izmjene, ako je prazno, motor il auto prikaz fali , odabir vozila