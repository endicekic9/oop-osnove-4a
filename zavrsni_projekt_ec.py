import tkinter as tk
from tkinter import messagebox
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
        # fixed window size
        self.root.geometry("1200x650")
        self.root.resizable(False, False)

        # theme / colors (backend settings)
        # You can change these values to recolor the whole app
        self.theme = {
            "bg": "#f0f0f5",           # window background
            "frame_bg": "#2c2cad",     # frames background
            "entry_bg": "#ffffff",     # entry/background color
            "entry_fg": "#000000",
            "btn_bg": "#4a7a8c",      # button background
            "btn_fg": "#ffffff",      # button text
            "listbox_bg": "#ffffff",
            "listbox_fg": "#000000",
            "label_fg": "#000000",
        }

        # apply theme defaults (use option_add so widgets created after this pick them up)
        self.root.configure(bg=self.theme["bg"])
        self.root.option_add("*Frame.background", self.theme["frame_bg"])
        self.root.option_add("*Label.foreground", self.theme["label_fg"])
        self.root.option_add("*Label.background", self.theme["frame_bg"])
        self.root.option_add("*Entry.background", self.theme["entry_bg"])
        self.root.option_add("*Entry.foreground", self.theme["entry_fg"])
        self.root.option_add("*Button.background", self.theme["btn_bg"])
        self.root.option_add("*Button.foreground", self.theme["btn_fg"])
        self.root.option_add("*Listbox.background", self.theme["listbox_bg"])
        self.root.option_add("*Listbox.foreground", self.theme["listbox_fg"])
        self.root.option_add("*Menubutton.background", self.theme["btn_bg"])
        self.root.option_add("*Menu.background", self.theme["btn_bg"])

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

        # Filter dropdown (Svi / Automobili / Motocikli)
        tk.Label(unos_frame, text="Filter:").grid(row=0, column=0, padx=5, pady=2, sticky="W")
        self.filter_var = tk.StringVar(value="Svi")
        self.filter_option = tk.OptionMenu(unos_frame, self.filter_var, "Svi", "Automobili", "Motocikli")
        self.filter_option.grid(row=0, column=1, padx=5, pady=2, sticky="W")
        # refresh when filter changes
        try:
            self.filter_var.trace_add("write", lambda *args: self.osvjezi_prikaz())
        except AttributeError:
            # older Python versions
            self.filter_var.trace("w", lambda *args: self.osvjezi_prikaz())

        tk.Label(unos_frame, text="Marka:").grid(row=1, column=0, padx=5, pady=5, sticky="W")
        self.marka_entry = tk.Entry(unos_frame)
        self.marka_entry.grid(row=1, column=1, padx=5, pady=5, sticky="EW")

        tk.Label(unos_frame, text="Model:").grid(row=1, column=2, padx=5, pady=5, sticky="W")
        self.model_entry = tk.Entry(unos_frame)
        self.model_entry.grid(row=1, column=3, padx=5, pady=5, sticky="EW")

        tk.Label(unos_frame, text="Godina proizvodnje:").grid(row=1, column=4, padx=5, pady=5, sticky="W")
        self.godina_entry = tk.Entry(unos_frame)
        self.godina_entry.grid(row=1, column=5, padx=5, pady=5, sticky="EW")

        tk.Label(unos_frame, text="Novo:").grid(row=1, column=6, padx=5, pady=5, sticky="W")
        self.novo_var = tk.StringVar(value="Novo")
        self.novo_option = tk.OptionMenu(unos_frame, self.novo_var, "Novo", "Rabljeno")
        self.novo_option.grid(row=1, column=7, padx=5, pady=5, sticky="EW")

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
        self.tip_goriva_var = tk.StringVar(value="Benzin")
        self.tip_goriva_option = tk.OptionMenu(unos_frame, self.tip_goriva_var, "Benzin", "Dizel", "Hybrid", "Električni", "Plin")
        self.tip_goriva_option.grid(row=3, column=3, padx=5, pady=5, sticky="EW")
        tk.Label(unos_frame, text="Tip motocikla (za motocikle):").grid(row=3, column=4, padx=5, pady=5, sticky="W")
        self.tip_motocikla_var = tk.StringVar(value="Sportski")
        self.tip_motocikla_option = tk.OptionMenu(unos_frame, self.tip_motocikla_var, "Sportski", "Touring", "Cruiser", "Off-road", "Chopper")
        self.tip_motocikla_option.grid(row=3, column=5, padx=5, pady=5, sticky="EW")

        self.dodaj_auto_button = tk.Button(unos_frame, text="Dodaj automobil", command=self.dodaj_automobil, width=12)
        self.dodaj_auto_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        self.dodaj_moto_button = tk.Button(unos_frame, text="Dodaj motocikl", command=self.dodaj_motocikl, width=12)
        self.dodaj_moto_button.grid(row=4, column=2, columnspan=2, padx=5, pady=5)

        self.spremi_izmjene_button = tk.Button(unos_frame, text="Spremi izmjene", command=self.spremi_izmjene, width=12)
        self.spremi_izmjene_button.grid(row=4, column=4, columnspan=2, padx=5, pady=5)

        self.spremi_gumb_csv = tk.Button(unos_frame, text="Spremi u CSV", command=self.spremi_u_csv, width=12)
        self.spremi_gumb_csv.grid(row=4, column=6, columnspan=2, padx=5, pady=5)
        self.spremi_gumb_xml = tk.Button(unos_frame, text="Spremi u XML", command=self.spremi_u_xml, width=12)
        self.spremi_gumb_xml.grid(row=4, column=8, columnspan=2, padx=5, pady=5)

        self.učitaj_gumb_csv = tk.Button(unos_frame, text="Učitaj iz CSV", command=self.učitaj_iz_csv, width=12)
        self.učitaj_gumb_csv.grid(row=4, column=10, columnspan=2, padx=5, pady=5)
        self.učitaj_gumb_xml = tk.Button(unos_frame, text="Učitaj iz XML", command=self.učitaj_iz_xml, width=12)
        self.učitaj_gumb_xml.grid(row=4, column=12, columnspan=2, padx=5, pady=5)

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
        novo_str = self.novo_var.get()
        novo = True if novo_str == "Novo" else False
        boja = self.boja_entry.get()
        snaga_motora = self.snaga_entry.get()
        naprodaji = self.naprodaji_entry.get()
        cijena = self.cijena_entry.get()
        broj_vrata = self.broj_vrata_entry.get()
        tip_goriva = self.tip_goriva_var.get()

        # simple validation: required fields
        if not marka or not model or not godina_proizvodnje or not cijena:
            messagebox.showwarning("Prazno polje", "Molimo popunite obavezna polja: Marka, Model, Godina proizvodnje i Cijena.")
            return

        automobil = Automobil(marka, model, godina_proizvodnje, novo, boja, snaga_motora, naprodaji, cijena, broj_vrata, tip_goriva)
        self.automobili.append(automobil)
        self.osvjezi_prikaz()
        self.ocisti_unos_polja()
    def dodaj_motocikl(self):
        marka = self.marka_entry.get()
        model = self.model_entry.get()
        godina_proizvodnje = self.godina_entry.get()
        novo_str = self.novo_var.get()
        novo = True if novo_str == "Novo" else False
        boja = self.boja_entry.get()
        snaga_motora = self.snaga_entry.get()
        naprodaji = self.naprodaji_entry.get()
        cijena = self.cijena_entry.get()
        tip_motocikla = self.tip_motocikla_var.get()

        if not marka or not model or not godina_proizvodnje or not cijena:
            messagebox.showwarning("Prazno polje", "Molimo popunite obavezna polja: Marka, Model, Godina proizvodnje i Cijena.")
            return

        motocikl = Motocikl(marka, model, godina_proizvodnje, novo, boja, snaga_motora, naprodaji, cijena, tip_motocikla)
        self.motocikli.append(motocikl)
        self.osvjezi_prikaz()
        self.ocisti_unos_polja()
    def osvjezi_prikaz(self):
        self.prikaz_vozila.delete(0, tk.END)
        # respect filter selection: Svi, Automobili, Motocikli
        filter_val = getattr(self, 'filter_var', None)
        sel = filter_val.get() if filter_val else "Svi"

        if sel in ("Svi", "Automobili"):
            for auto in self.automobili:
                novo_txt = "Novo" if getattr(auto, 'novo', False) else "Rabljeno"
                self.prikaz_vozila.insert(tk.END, f"Automobil | Marka: {auto.marka} | Model: {auto.model} | Godina: {auto.godina_proizvodnje} | {novo_txt} | Boja: {auto.boja} | Snaga: {auto.snaga_motora} KS | Na prodaji: {auto.naprodaji} | Cijena: {auto.cijena} EUR | Broj vrata: {auto.broj_vrata} | Tip goriva: {auto.tip_goriva}")

        if sel in ("Svi", "Motocikli"):
            for moto in self.motocikli:
                novo_txt = "Novo" if getattr(moto, 'novo', False) else "Rabljeno"
                self.prikaz_vozila.insert(tk.END, f"Motocikl | Marka: {moto.marka} | Model: {moto.model} | Godina: {moto.godina_proizvodnje} | {novo_txt} | Boja: {moto.boja} | Snaga: {moto.snaga_motora} KS | Na prodaji: {moto.naprodaji} | Cijena: {moto.cijena} EUR | Tip motocikla: {moto.tip_motocikla}")
    def ocisti_unos_polja(self):
        self.marka_entry.delete(0, tk.END)
        self.model_entry.delete(0, tk.END)
        self.godina_entry.delete(0, tk.END)
        self.novo_var.set("Novo")
        self.boja_entry.delete(0, tk.END)
        self.snaga_entry.delete(0, tk.END)
        self.naprodaji_entry.delete(0, tk.END)
        self.cijena_entry.delete(0, tk.END)
        self.broj_vrata_entry.delete(0, tk.END)
        self.tip_goriva_var.set("Benzin")
        self.tip_motocikla_var.set("Sportski")
    # legacy/unused method removed to avoid references to non-existent attributes
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
        # set novo dropdown
        self.novo_var.set("Novo" if automobil.novo else "Rabljeno")
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
        # set tip goriva dropdown
        self.tip_goriva_var.set(automobil.tip_goriva)
    def popuni_unos_polja_motocikl(self, motocikl):
        self.marka_entry.delete(0, tk.END)
        self.marka_entry.insert(0, motocikl.marka)
        self.model_entry.delete(0, tk.END)
        self.model_entry.insert(0, motocikl.model)
        self.godina_entry.delete(0, tk.END)
        self.godina_entry.insert(0, motocikl.godina_proizvodnje)
        self.boja_entry.delete(0, tk.END)
        # set novo dropdown
        self.novo_var.set("Novo" if motocikl.novo else "Rabljeno")
        self.boja_entry.insert(0, motocikl.boja)
        self.snaga_entry.delete(0, tk.END)
        self.snaga_entry.insert(0, motocikl.snaga_motora)
        self.naprodaji_entry.delete(0, tk.END)
        self.naprodaji_entry.insert(0, motocikl.naprodaji)
        self.cijena_entry.delete(0, tk.END)
        self.cijena_entry.insert(0, motocikl.cijena)
        # clear broj vrata and set tip motocikla dropdown
        self.broj_vrata_entry.delete(0, tk.END)
        self.tip_motocikla_var.set(motocikl.tip_motocikla)
    def spremi_izmjene(self):
        if self.odabrano_vozilo:
            self.odabrano_vozilo.marka = self.marka_entry.get()
            self.odabrano_vozilo.model = self.model_entry.get()
            self.odabrano_vozilo.godina_proizvodnje = self.godina_entry.get()
            novo_str = self.novo_var.get()
            self.odabrano_vozilo.novo = True if novo_str == "Novo" else False
            self.odabrano_vozilo.boja = self.boja_entry.get()
            self.odabrano_vozilo.snaga_motora = self.snaga_entry.get()
            self.odabrano_vozilo.naprodaji = self.naprodaji_entry.get()
            self.odabrano_vozilo.cijena = self.cijena_entry.get()

            if isinstance(self.odabrano_vozilo, Automobil):
                self.odabrano_vozilo.broj_vrata = self.broj_vrata_entry.get()
                self.odabrano_vozilo.tip_goriva = self.tip_goriva_var.get()
            elif isinstance(self.odabrano_vozilo, Motocikl):
                self.odabrano_vozilo.tip_motocikla = self.tip_motocikla_var.get()

            self.osvjezi_prikaz()
            self.ocisti_unos_polja()
            self.odabrano_vozilo = None
    def spremi_u_csv(self):
        fieldnames = ["Tip", "Marka", "Model", "Godina proizvodnje", "Novo", "Boja", "Snaga motora", "Na prodaji", "Cijena", "Broj vrata", "Tip goriva", "Tip motocikla"]
        with open("lager_vozila.csv", mode="w", newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for auto in self.automobili:
                writer.writerow({
                    "Tip": "Automobil",
                    "Marka": auto.marka,
                    "Model": auto.model,
                    "Godina proizvodnje": auto.godina_proizvodnje,
                    "Novo": "Novo" if getattr(auto, 'novo', False) else "Rabljeno",
                    "Boja": auto.boja,
                    "Snaga motora": auto.snaga_motora,
                    "Na prodaji": auto.naprodaji,
                    "Cijena": auto.cijena,
                    "Broj vrata": auto.broj_vrata,
                    "Tip goriva": auto.tip_goriva,
                    "Tip motocikla": "",
                })
            for moto in self.motocikli:
                writer.writerow({
                    "Tip": "Motocikl",
                    "Marka": moto.marka,
                    "Model": moto.model,
                    "Godina proizvodnje": moto.godina_proizvodnje,
                    "Novo": "Novo" if getattr(moto, 'novo', False) else "Rabljeno",
                    "Boja": moto.boja,
                    "Snaga motora": moto.snaga_motora,
                    "Na prodaji": moto.naprodaji,
                    "Cijena": moto.cijena,
                    "Broj vrata": "",
                    "Tip goriva": "",
                    "Tip motocikla": moto.tip_motocikla,
                })
    def učitaj_iz_csv(self):
        self.automobili.clear()
        self.motocikli.clear()
        try:
            with open("lager_vozila.csv", mode="r", newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    tip = (row.get("Tip") or "").strip()
                    if tip == "Automobil":
                        novo_val = (row.get("Novo") or "").strip()
                        novo = True if novo_val.lower() in ("novo", "true", "1", "yes") else False
                        automobil = Automobil(
                            row.get("Marka", ""),
                            row.get("Model", ""),
                            row.get("Godina proizvodnje", ""),
                            novo,
                            row.get("Boja", ""),
                            row.get("Snaga motora", ""),
                            row.get("Na prodaji", ""),
                            row.get("Cijena", ""),
                            row.get("Broj vrata", ""),
                            row.get("Tip goriva", ""),
                        )
                        self.automobili.append(automobil)
                    elif tip == "Motocikl":
                        novo_val = (row.get("Novo") or "").strip()
                        novo = True if novo_val.lower() in ("novo", "true", "1", "yes") else False
                        motocikl = Motocikl(
                            row.get("Marka", ""),
                            row.get("Model", ""),
                            row.get("Godina proizvodnje", ""),
                            novo,
                            row.get("Boja", ""),
                            row.get("Snaga motora", ""),
                            row.get("Na prodaji", ""),
                            row.get("Cijena", ""),
                            row.get("Tip motocikla", ""),
                        )
                        self.motocikli.append(motocikl)
        except FileNotFoundError:
            messagebox.showwarning("Datoteka nije pronađena", "CSV datoteka 'lager_vozila.csv' ne postoji.")
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
    root.mainloop() #prikaz nije cjelovit, izmjene, ako je prazno, motor il auto prikaz fali , odabir vozila, drop down za benzin/dizel, novo staro, itd, msgbox, gui