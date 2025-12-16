import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import csv
import xml.etree.ElementTree as ET

#V0.1.0
#inicijalni kod za lager vozila, početak grafičkog sučelja, dodavanje i prikaz vozila

#0.2.0
#dodano spremanje i učitavanje iz CSV i XML formata, bug fixes

#0.3.0
#dodani filteri za prikaz vozila

#0.4.0
#personalizacija boja sučelja

#0.5.0
#ispravci kod učitavanja iz CSV datoteke, prilagodba velicina gumba i rasporeda

#0.6.0
#pripreme za završnu verziju, potrebno usavršavanje korisničkog sučelja i testiranje

#1.0.0
#prva potpuna verzija programa ParkPro

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
        # prodano flag: True if vehicle is sold
        self.prodano = False
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
        self.root.title("ParkPro - Lager vozila")
        self.root.geometry("1400x650")
        self.root.resizable(False, False)

        # postavke boja
        # Pri personaliziranju programa, boja odabrati prozorom za odabir boja
        # OBRATITI PAŽNJU NA ČITLJIVOST TEKSTA U ODNOSU NA POZADINU
        self.theme = {
            "bg": "#ff0000",           # pozadina glavnog prozora
            "frame_bg": "#3f3ff9",     # pozadina frame-a
            "entry_bg": "#ffffff",     # pozadina unosa
            "entry_fg": "#000000",
            "btn_bg": "#ffffff",      #boja gumbova
            "btn_fg": "#000000",      #text gumbova
            "listbox_bg": "#ffffff",    #pozadina liste
            "listbox_fg": "#000000",    #text liste
            "label_fg": "#000000",
        }

        self.root.configure(bg=self.theme["bg"])
        style = ttk.Style(self.root)
        try:
            style.theme_use('default')
        except Exception:
            pass
        style.configure('TFrame', background=self.theme["frame_bg"])
        style.configure('TLabel', background=self.theme["frame_bg"], foreground=self.theme["label_fg"])
        style.configure('TEntry', fieldbackground=self.theme["entry_bg"], foreground=self.theme["entry_fg"])
        style.configure('TButton', background=self.theme["btn_bg"], foreground=self.theme["btn_fg"])
        style.configure('TCombobox', fieldbackground=self.theme["entry_bg"], foreground=self.theme["entry_fg"])
        style.configure('Treeview', background=self.theme["listbox_bg"], fieldbackground=self.theme["listbox_bg"], foreground=self.theme["listbox_fg"]) 
        self.root.option_add("*Entry.background", self.theme["entry_bg"])
        self.root.option_add("*Entry.foreground", self.theme["entry_fg"])

        self.automobili = []
        self.motocikli = []
        self.odabrano_vozilo = None

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        unos_frame = ttk.Frame(self.root, padding=10)
        unos_frame.grid(row=0, column=0, sticky="EW")

        prikaz_frame = ttk.Frame(self.root, padding=10)
        prikaz_frame.grid(row=1, column=0, sticky="NSEW")

        prikaz_frame.columnconfigure(0, weight=1)
        prikaz_frame.rowconfigure(0, weight=1)

        # Filter dropdown (Svi / Automobili / Motocikli)
        ttk.Label(unos_frame, text="Filter:").grid(row=0, column=0, padx=5, pady=2, sticky="W")
        self.filter_var = tk.StringVar(value="Svi")
        self.filter_combo = ttk.Combobox(unos_frame, textvariable=self.filter_var, values=("Svi", "Automobili", "Motocikli"), state="readonly", width=10)
        self.filter_combo.grid(row=0, column=1, padx=5, pady=2, sticky="W")
        self.filter_combo.bind('<<ComboboxSelected>>', lambda e: self.osvjezi_prikaz())
        # Additional filters: Novo, Na prodaji, Tip goriva, Tip motocikla
        ttk.Label(unos_frame, text="Novo filter:").grid(row=0, column=2, padx=5, pady=2, sticky="W")
        self.filter_novo_var = tk.StringVar(value="Svi")
        self.filter_novo_combo = ttk.Combobox(unos_frame, textvariable=self.filter_novo_var, values=("Svi","Novo","Rabljeno"), state="readonly", width=10)
        self.filter_novo_combo.grid(row=0, column=3, padx=5, pady=2, sticky="W")
        self.filter_novo_combo.bind('<<ComboboxSelected>>', lambda e: self.osvjezi_prikaz())

        ttk.Label(unos_frame, text="Na prodaji:").grid(row=0, column=4, padx=5, pady=2, sticky="W")
        self.filter_prodaja_var = tk.StringVar(value="Svi")
        self.filter_prodaja_combo = ttk.Combobox(unos_frame, textvariable=self.filter_prodaja_var, values=("Svi","Da","Ne"), state="readonly", width=8)
        self.filter_prodaja_combo.grid(row=0, column=5, padx=5, pady=2, sticky="W")
        self.filter_prodaja_combo.bind('<<ComboboxSelected>>', lambda e: self.osvjezi_prikaz())

        ttk.Label(unos_frame, text="Filter goriva:").grid(row=0, column=6, padx=5, pady=2, sticky="W")
        self.filter_goriva_var = tk.StringVar(value="Svi")
        self.filter_goriva_combo = ttk.Combobox(unos_frame, textvariable=self.filter_goriva_var, values=("Svi","Benzin","Dizel","Hybrid","Električni","Plin"), state="readonly", width=12)
        self.filter_goriva_combo.grid(row=0, column=7, padx=5, pady=2, sticky="W")
        self.filter_goriva_combo.bind('<<ComboboxSelected>>', lambda e: self.osvjezi_prikaz())

        ttk.Label(unos_frame, text="Filter tip motocikla:").grid(row=0, column=8, padx=5, pady=2, sticky="W")
        self.filter_moto_var = tk.StringVar(value="Svi")
        self.filter_moto_combo = ttk.Combobox(unos_frame, textvariable=self.filter_moto_var, values=("Svi","Sportski","Touring","Cruiser","Off-road","Chopper"), state="readonly", width=12)
        self.filter_moto_combo.grid(row=0, column=9, padx=5, pady=2, sticky="W")
        self.filter_moto_combo.bind('<<ComboboxSelected>>', lambda e: self.osvjezi_prikaz())

        ttk.Label(unos_frame, text="Marka:").grid(row=1, column=0, padx=5, pady=5, sticky="W")
        self.marka_entry = ttk.Entry(unos_frame)
        self.marka_entry.grid(row=1, column=1, padx=5, pady=5, sticky="EW")

        ttk.Label(unos_frame, text="Model:").grid(row=1, column=2, padx=5, pady=5, sticky="W")
        self.model_entry = ttk.Entry(unos_frame)
        self.model_entry.grid(row=1, column=3, padx=5, pady=5, sticky="EW")

        ttk.Label(unos_frame, text="Godina proizvodnje:").grid(row=1, column=4, padx=5, pady=5, sticky="W")
        self.godina_entry = ttk.Entry(unos_frame)
        self.godina_entry.grid(row=1, column=5, padx=5, pady=5, sticky="EW")

        ttk.Label(unos_frame, text="Novo:").grid(row=1, column=6, padx=5, pady=5, sticky="W")
        self.novo_var = tk.StringVar(value="Novo")
        self.novo_combo = ttk.Combobox(unos_frame, textvariable=self.novo_var, values=("Novo", "Rabljeno"), state="readonly", width=10)
        self.novo_combo.grid(row=1, column=7, padx=5, pady=5, sticky="EW")

        ttk.Label(unos_frame, text="Boja:").grid(row=2, column=0, padx=5, pady=5, sticky="W")
        self.boja_entry = ttk.Entry(unos_frame)
        self.boja_entry.grid(row=2, column=1, padx=5, pady=5, sticky="EW")

        ttk.Label(unos_frame, text="Snaga motora (KS):").grid(row=2, column=2, padx=5, pady=5, sticky="W")
        self.snaga_entry = ttk.Entry(unos_frame)
        self.snaga_entry.grid(row=2, column=3, padx=5, pady=5, sticky="EW")

        ttk.Label(unos_frame, text="Na prodaji (Da/Ne):").grid(row=2, column=4, padx=5, pady=5, sticky="W")
        self.naprodaji_entry = ttk.Entry(unos_frame)
        self.naprodaji_entry.grid(row=2, column=5, padx=5, pady=5, sticky="EW")

        ttk.Label(unos_frame, text="Cijena (EUR):").grid(row=2, column=6, padx=5, pady=5, sticky="W")
        self.cijena_entry = ttk.Entry(unos_frame)
        self.cijena_entry.grid(row=2, column=7, padx=5, pady=5, sticky="EW")

        ttk.Label(unos_frame, text="Broj vrata (za automobile):").grid(row=3, column=0, padx=5, pady=5, sticky="W")
        self.broj_vrata_entry = ttk.Entry(unos_frame)
        self.broj_vrata_entry.grid(row=3, column=1, padx=5, pady=5, sticky="EW")

        ttk.Label(unos_frame, text="Tip goriva (za automobile):").grid(row=3, column=2, padx=5, pady=5, sticky="W")
        self.tip_goriva_var = tk.StringVar(value="Benzin")
        self.tip_goriva_combo = ttk.Combobox(unos_frame, textvariable=self.tip_goriva_var, values=("Benzin", "Dizel", "Hybrid", "Električni", "Plin"), state="readonly", width=10)
        self.tip_goriva_combo.grid(row=3, column=3, padx=5, pady=5, sticky="EW")
        ttk.Label(unos_frame, text="Tip motocikla (za motocikle):").grid(row=3, column=4, padx=5, pady=5, sticky="W")
        self.tip_motocikla_var = tk.StringVar(value="Sportski")
        self.tip_motocikla_combo = ttk.Combobox(unos_frame, textvariable=self.tip_motocikla_var, values=("Sportski", "Touring", "Cruiser", "Off-road", "Chopper"), state="readonly", width=10)
        self.tip_motocikla_combo.grid(row=3, column=5, padx=5, pady=5, sticky="EW")

        self.dodaj_auto_button = ttk.Button(unos_frame, text="Dodaj automobil", command=self.dodaj_automobil)
        self.dodaj_auto_button.grid(row=4, column=0, columnspan=1, padx=5, pady=5, sticky='EW')

        self.dodaj_moto_button = ttk.Button(unos_frame, text="Dodaj motocikl", command=self.dodaj_motocikl)
        self.dodaj_moto_button.grid(row=4, column=1, columnspan=1, padx=5, pady=5, sticky='EW')

        self.spremi_izmjene_button = ttk.Button(unos_frame, text="Spremi izmjene", command=self.spremi_izmjene)
        self.spremi_izmjene_button.grid(row=4, column=2, columnspan=1, padx=5, pady=5, sticky='EW')

        self.spremi_gumb_csv = ttk.Button(unos_frame, text="Spremi u CSV", command=self.spremi_u_csv)
        self.spremi_gumb_csv.grid(row=4, column=3, columnspan=1, padx=5, pady=5, sticky='EW')
        self.spremi_gumb_xml = ttk.Button(unos_frame, text="Spremi u XML", command=self.spremi_u_xml)
        self.spremi_gumb_xml.grid(row=4, column=4, columnspan=1, padx=5, pady=5, sticky='EW')

        self.učitaj_gumb_csv = ttk.Button(unos_frame, text="Učitaj iz CSV", command=self.učitaj_iz_csv)
        self.učitaj_gumb_csv.grid(row=4, column=5, columnspan=1, padx=5, pady=5, sticky='EW')
        self.učitaj_gumb_xml = ttk.Button(unos_frame, text="Učitaj iz XML", command=self.učitaj_iz_xml)
        self.učitaj_gumb_xml.grid(row=4, column=6, columnspan=1, padx=5, pady=5, sticky='EW')

        ttk.Label(unos_frame, text="🛞 ParkPro", font=("Arial", 12, "bold")).grid(row=3, column=9, padx=5, pady=2)

        # checkbox prodano i about gumb
        self.prodano_var = tk.BooleanVar(value=False)
        self.prodano_check = ttk.Checkbutton(unos_frame, text="Prodano", variable=self.prodano_var, command=self.prodano_toggle)
        self.prodano_check.grid(row=3, column=6, padx=5, pady=5, sticky='W')

        self.mark_sold_button = ttk.Button(unos_frame, text="Označi PRODANO", command=self.mark_selected_sold)
        self.mark_sold_button.grid(row=4, column=7, padx=5, pady=5, sticky='EW')

        self.about_button = ttk.Button(unos_frame, text="About app", command=self.show_about)
        self.about_button.grid(row=4, column=9, padx=5, pady=5, sticky='EW')

        self.columns = ("Tip","Marka","Model","Godina","Novo","Boja","Snaga","NaProdaji","Cijena","BrojVrata","TipGoriva","TipMotocikla")
        self.prikaz_vozila = ttk.Treeview(prikaz_frame, columns=self.columns, show='headings', selectmode='browse')

        for col in self.columns:
            self.prikaz_vozila.heading(col, text=col, command=lambda c=col: self.sort_tree(c))
            width = 80 if col in ("Tip","Godina","Novo","NaProdaji","BrojVrata") else 120
            self.prikaz_vozila.column(col, width=width, anchor='w')
        self.prikaz_vozila.grid(row=0, column=0, sticky="NSEW")
        self.prikaz_vozila.bind('<<TreeviewSelect>>', self.prikaz_odabranog_vozila)

        self.scrollbar = ttk.Scrollbar(prikaz_frame, orient="vertical", command=self.prikaz_vozila.yview)
        self.scrollbar.grid(row=0, column=1, sticky="NS")
        self.prikaz_vozila.configure(yscrollcommand=self.scrollbar.set)
        self.sort_column = None
        self.sort_reverse = False
        # stats frame: total value, total count, available count
        self.stats_frame = ttk.Frame(prikaz_frame)
        self.stats_frame.grid(row=1, column=0, sticky='EW', padx=5, pady=6)
        self.total_label_var = tk.StringVar(value="Ukupna vrijednost: 0.00 EUR")
        self.total_label = ttk.Label(self.stats_frame, textvariable=self.total_label_var)
        self.total_label.grid(row=0, column=0, sticky='W')
        self.total_count_var = tk.StringVar(value="Ukupno vozila: 0")
        self.total_count_label = ttk.Label(self.stats_frame, textvariable=self.total_count_var)
        self.total_count_label.grid(row=0, column=1, sticky='W', padx=10)
        self.available_count_var = tk.StringVar(value="Dostupno: 0")
        self.available_count_label = ttk.Label(self.stats_frame, textvariable=self.available_count_var)
        self.available_count_label.grid(row=0, column=2, sticky='W', padx=10)

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

        # nedovoljan unos
        if not marka or not model or not godina_proizvodnje or not cijena:
            messagebox.showwarning("Prazno polje", "Molimo popunite obavezna polja: Marka, Model, Godina proizvodnje i Cijena.")
            return

        automobil = Automobil(marka, model, godina_proizvodnje, novo, boja, snaga_motora, naprodaji, cijena, broj_vrata, tip_goriva)
        # oznaka prodano
        try:
            automobil.prodano = bool(self.prodano_var.get())
        except Exception:
            automobil.prodano = False
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
        try:
            motocikl.prodano = bool(self.prodano_var.get())
        except Exception:
            motocikl.prodano = False
        self.motocikli.append(motocikl)
        self.osvjezi_prikaz()
        self.ocisti_unos_polja()
    def osvjezi_prikaz(self):
        for item in self.prikaz_vozila.get_children():
            self.prikaz_vozila.delete(item)

        sel = self.filter_var.get() if getattr(self, 'filter_var', None) else "Svi"
        novo_filter = self.filter_novo_var.get() if getattr(self, 'filter_novo_var', None) else "Svi"
        prodaja_filter = self.filter_prodaja_var.get() if getattr(self, 'filter_prodaja_var', None) else "Svi"
        goriva_filter = self.filter_goriva_var.get() if getattr(self, 'filter_goriva_var', None) else "Svi"
        moto_filter = self.filter_moto_var.get() if getattr(self, 'filter_moto_var', None) else "Svi"

        rows = []
        total_value = 0.0
        if sel in ("Svi", "Automobili"):
            for i, auto in enumerate(self.automobili):
                if novo_filter != "Svi":
                    if (novo_filter == "Novo") != bool(getattr(auto, 'novo', False)):
                        continue
                if prodaja_filter != "Svi":
                    if prodaja_filter.lower() != (auto.naprodaji or "").strip().lower():
                        continue
                if goriva_filter != "Svi":
                    if goriva_filter != (auto.tip_goriva or ""):
                        continue
                novo_txt = "Novo" if getattr(auto, 'novo', False) else "Rabljeno"
                marka_display = f"PRODANO - {auto.marka}" if getattr(auto, 'prodano', False) else auto.marka
                vals = ("Automobil", marka_display, auto.model, auto.godina_proizvodnje, novo_txt, auto.boja, f"{auto.snaga_motora} KS", auto.naprodaji, f"{auto.cijena} EUR", auto.broj_vrata, auto.tip_goriva, "")
                if not getattr(auto, 'prodano', False):
                    import re
                    m = re.search(r"([\d,.]+)", str(auto.cijena))
                    if m:
                        try:
                            total_value += float(m.group(1).replace(',', ''))
                        except Exception:
                            pass
                rows.append((f"A-{i}", vals))

        if sel in ("Svi", "Motocikli"):
            for i, moto in enumerate(self.motocikli):
                if novo_filter != "Svi":
                    if (novo_filter == "Novo") != bool(getattr(moto, 'novo', False)):
                        continue
                if prodaja_filter != "Svi":
                    if prodaja_filter.lower() != (moto.naprodaji or "").strip().lower():
                        continue
                if goriva_filter != "Svi":
                    continue
                if moto_filter != "Svi":
                    if moto_filter != (moto.tip_motocikla or ""):
                        continue
                novo_txt = "Novo" if getattr(moto, 'novo', False) else "Rabljeno"
                marka_display = f"PRODANO - {moto.marka}" if getattr(moto, 'prodano', False) else moto.marka
                vals = ("Motocikl", marka_display, moto.model, moto.godina_proizvodnje, novo_txt, moto.boja, f"{moto.snaga_motora} KS", moto.naprodaji, f"{moto.cijena} EUR", "", "", moto.tip_motocikla)
                if not getattr(moto, 'prodano', False):
                    import re
                    m = re.search(r"([\d,.]+)", str(moto.cijena))
                    if m:
                        try:
                            total_value += float(m.group(1).replace(',', ''))
                        except Exception:
                            pass
                rows.append((f"M-{i}", vals))

        if self.sort_column:
            col_idx = self.columns.index(self.sort_column)
            def keyfunc(item):
                val = item[1][col_idx]
                return self._parse_sort_value(val, self.sort_column)
            rows.sort(key=keyfunc, reverse=self.sort_reverse)

        for iid, vals in rows:
            self.prikaz_vozila.insert('', 'end', iid=iid, values=vals)
        try:
            total_count = len(rows)
            available_count = sum(1 for iid, vals in rows if not str(vals[1]).startswith("PRODANO -"))
            self.total_label_var.set(f"Ukupna vrijednost: {total_value:.2f} EUR")
            self.total_count_var.set(f"Ukupno vozila: {total_count}")
            self.available_count_var.set(f"Dostupno: {available_count}")
        except Exception:
            pass

    def _parse_sort_value(self, val, col):
        if val is None:
            return ""
        text = str(val)
        if col == "Godina":
            try:
                return int(text)
            except Exception:
                return -1
        if col == "Snaga":
            import re
            m = re.search(r"(\d+)", text)
            return int(m.group(1)) if m else 0
        if col == "Cijena":
            import re
            m = re.search(r"([\d,.]+)", text)
            if not m:
                return 0.0
            num = m.group(1).replace(',', '')
            try:
                return float(num)
            except Exception:
                return 0.0
        if col == "BrojVrata":
            try:
                return int(text)
            except Exception:
                return 0
        return text.lower()

    def sort_tree(self, col):
        if self.sort_column == col:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = col
            self.sort_reverse = False
        self.osvjezi_prikaz()
    def ocisti_unos_polja(self):
        self.marka_entry.delete(0, tk.END)
        self.model_entry.delete(0, tk.END)
        self.godina_entry.delete(0, tk.END)
        try:
            self.novo_combo.set("Novo")
        except Exception:
            self.novo_var.set("Novo")
        self.boja_entry.delete(0, tk.END)
        self.snaga_entry.delete(0, tk.END)
        self.naprodaji_entry.delete(0, tk.END)
        self.cijena_entry.delete(0, tk.END)
        self.broj_vrata_entry.delete(0, tk.END)
        try:
            self.tip_goriva_combo.set("Benzin")
        except Exception:
            self.tip_goriva_var.set("Benzin")
        try:
            self.tip_motocikla_combo.set("Sportski")
        except Exception:
            self.tip_motocikla_var.set("Sportski")

    def prikaz_odabranog_vozila(self, event):
        selected = self.prikaz_vozila.selection()
        if not selected:
            return
        iid = selected[0]
        if iid.startswith('A-'):
            idx = int(iid.split('-')[1])
            vozilo = self.automobili[idx]
            self.odabrano_vozilo = vozilo
            self.popuni_unos_polja_automobil(vozilo)
        elif iid.startswith('M-'):
            idx = int(iid.split('-')[1])
            vozilo = self.motocikli[idx]
            self.odabrano_vozilo = vozilo
            self.popuni_unos_polja_motocikl(vozilo)
    def popuni_unos_polja_automobil(self, automobil):
        self.marka_entry.delete(0, tk.END)
        self.marka_entry.insert(0, automobil.marka)
        self.model_entry.delete(0, tk.END)
        self.model_entry.insert(0, automobil.model)
        self.godina_entry.delete(0, tk.END)
        self.godina_entry.insert(0, automobil.godina_proizvodnje)
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
        self.tip_goriva_var.set(automobil.tip_goriva)
        try:
            self.prodano_var.set(bool(getattr(automobil, 'prodano', False)))
        except Exception:
            self.prodano_var.set(False)
    def popuni_unos_polja_motocikl(self, motocikl):
        self.marka_entry.delete(0, tk.END)
        self.marka_entry.insert(0, motocikl.marka)
        self.model_entry.delete(0, tk.END)
        self.model_entry.insert(0, motocikl.model)
        self.godina_entry.delete(0, tk.END)
        self.godina_entry.insert(0, motocikl.godina_proizvodnje)
        self.boja_entry.delete(0, tk.END)
        self.novo_var.set("Novo" if motocikl.novo else "Rabljeno")
        self.boja_entry.insert(0, motocikl.boja)
        self.snaga_entry.delete(0, tk.END)
        self.snaga_entry.insert(0, motocikl.snaga_motora)
        self.naprodaji_entry.delete(0, tk.END)
        self.naprodaji_entry.insert(0, motocikl.naprodaji)
        self.cijena_entry.delete(0, tk.END)
        self.cijena_entry.insert(0, motocikl.cijena)
        self.broj_vrata_entry.delete(0, tk.END)
        self.tip_motocikla_var.set(motocikl.tip_motocikla)
        try:
            self.prodano_var.set(bool(getattr(motocikl, 'prodano', False)))
        except Exception:
            self.prodano_var.set(False)
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

            try:
                self.odabrano_vozilo.prodano = bool(self.prodano_var.get())
            except Exception:
                self.odabrano_vozilo.prodano = False

            self.osvjezi_prikaz()
            self.ocisti_unos_polja()
            self.odabrano_vozilo = None
    def prodano_toggle(self):
        if getattr(self, 'odabrano_vozilo', None):
            try:
                self.odabrano_vozilo.prodano = bool(self.prodano_var.get())
            except Exception:
                self.odabrano_vozilo.prodano = False
            self.osvjezi_prikaz()

    def mark_selected_sold(self):
        selected = self.prikaz_vozila.selection()
        if not selected:
            messagebox.showwarning("Nije odabrano", "Molimo odaberite vozilo za označiti kao prodano.")
            return
        iid = selected[0]
        if iid.startswith('A-'):
            idx = int(iid.split('-')[1])
            obj = self.automobili[idx]
        elif iid.startswith('M-'):
            idx = int(iid.split('-')[1])
            obj = self.motocikli[idx]
        else:
            return
        obj.prodano = True
        try:
            self.prodano_var.set(True)
        except Exception:
            pass
        self.osvjezi_prikaz()

    def show_about(self):
        messagebox.showinfo("About ParkPro", "ParkPro v1.0\nAutor: Endi Čekić\nJednostavan alat za vođenje lagera vozila.")
    def spremi_u_csv(self):
        fieldnames = ["Tip", "Marka", "Model", "Godina proizvodnje", "Novo", "Boja", "Snaga motora", "Na prodaji", "Cijena", "Broj vrata", "Tip goriva", "Tip motocikla", "Prodano"]
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
                    "Prodano": "Da" if getattr(auto, 'prodano', False) else "Ne",
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
                    "Prodano": "Da" if getattr(moto, 'prodano', False) else "Ne",
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
                        # parse sold flag
                        prodano_val = (row.get("Prodano") or "").strip()
                        automobil.prodano = True if prodano_val.lower() in ("da", "true", "1", "yes") else False
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
                        prodano_val = (row.get("Prodano") or "").strip()
                        motocikl.prodano = True if prodano_val.lower() in ("da", "true", "1", "yes") else False
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
            prodano_elem=ET.SubElement(auto_elem, "Prodano")
            prodano_elem.text=str(getattr(auto, 'prodano', False))
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
            prodano_elem=ET.SubElement(moto_elem, "Prodano")
            prodano_elem.text=str(getattr(moto, 'prodano', False))
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
            prodano = False
            prod_el = auto_elem.find("Prodano")
            if prod_el is not None and prod_el.text is not None:
                prodano = prod_el.text == "True"
            automobil=Automobil(marka, model, godina_proizvodnje, novo, boja, snaga_motora, naprodaji, cijena, broj_vrata, tip_goriva)
            automobil.prodano = prodano
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
            prodano = False
            prod_el = moto_elem.find("Prodano")
            if prod_el is not None and prod_el.text is not None:
                prodano = prod_el.text == "True"
            motocikl=Motocikl(marka, model, godina_proizvodnje, novo, boja, snaga_motora, naprodaji, cijena, tip_motocikla)
            motocikl.prodano = prodano
            self.motocikli.append(motocikl)
        self.osvjezi_prikaz()
if __name__ == "__main__":
    root = tk.Tk()
    app = Prikaz_lagera(root)
    root.mainloop()