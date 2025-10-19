import tkinter as tk
from tkinter import messagebox, filedialog
import csv
import os
#Definiranje klase Kontakt
class Kontakt:
    def __init__(self, ime, email, telefon):
        self.ime = ime
        self.email = email
        self.telefon = telefon

    def __str__(self):
        return f"{self.ime} {self.email} {self.telefon}"
#Definiranje glavne klase
class ImenikApp:
    def __init__(self, root):
        self.root = root
        self.kontakti = []
        root.title("Imenik")
        root.geometry("500x400")
        #Konfig responzivnosti
        root.columnconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)
        #Okvir za unos
        unos_frame = tk.Frame(root, padx=10, pady=10)
        unos_frame.grid(row=0, column=0, sticky="EW")
        #Unos imena
        tk.Label(unos_frame, text="Ime:").grid(row=0, column=0, sticky="W")
        self.ime_unos = tk.Entry(unos_frame)
        self.ime_unos.grid(row=0, column=1, padx=10, pady=5, sticky="EW")
        #Unos emaila
        tk.Label(unos_frame, text="Email:").grid(row=1, column=0, sticky="W")
        self.email_unos = tk.Entry(unos_frame)
        self.email_unos.grid(row=1, column=1, padx=10, pady=5, sticky="EW")
        #Unos telefona
        tk.Label(unos_frame, text="Telefon:").grid(row=2, column=0, sticky="W")
        self.telefon_unos = tk.Entry(unos_frame)
        self.telefon_unos.grid(row=2, column=1, padx=10, pady=5, sticky="EW")
        unos_frame.columnconfigure(1, weight=1)
        #Gumb za dodavanje kontakta
        self.dodaj_gumb = tk.Button(unos_frame, text="Dodaj kontakt", command=self.dodaj_kontakt)
        self.dodaj_gumb.grid(row=3, column=0, columnspan=2, pady=10)
        #Okvir za prikaz
        lista_frame = tk.Frame(root, padx=10, pady=10)
        lista_frame.grid(row=1, column=0, sticky="NSEW")
        lista_frame.columnconfigure(0, weight=1)
        lista_frame.rowconfigure(0, weight=1)
        #Lista kontakata
        self.listbox = tk.Listbox(lista_frame)
        self.listbox.grid(row=0, column=0, sticky="NSEW")
        #Scrollbar
        scrollbar = tk.Scrollbar(lista_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="NS")
        self.listbox.config(yscrollcommand=scrollbar.set)
        #Okvir za gumbe
        gumbi_frame = tk.Frame(root, padx=10, pady=10)
        gumbi_frame.grid(row=2, column=0, sticky="EW")
        #Gumb za spremanje kontakta
        self.spremi_gumb = tk.Button(gumbi_frame, text="Spremi kontakte", command=self.spremi_kontakte)
        self.spremi_gumb.grid(row=0, column=0, padx=5, pady=5)
        #Gumb za brisanje kontakta
        self.obrisi_gumb = tk.Button(gumbi_frame, text="Obriši kontakt", command=self.obrisi_kontakt)
        self.obrisi_gumb.grid(row=0, column=1, padx=5, pady=5)

        self.ucitaj_kontakte()
    #Dodavanje kontakta
    def dodaj_kontakt(self):
        ime = self.ime_unos.get().strip()
        email = self.email_unos.get().strip()
        telefon = self.telefon_unos.get().strip()
        if ime and email and telefon:
            novi_kontakt = Kontakt(ime, email, telefon)
            self.kontakti.append(novi_kontakt)
            self.listbox.insert(tk.END, str(novi_kontakt))
            self.ime_unos.delete(0, tk.END)
            self.email_unos.delete(0, tk.END)
            self.telefon_unos.delete(0, tk.END)
        else:
            messagebox.showwarning("???","A sta ti fali? Neka daska u glavi ili prazno polje?")
            return
    def osvjezi_prikaz(self):
        self.listbox.delete(0, tk.END)
        for kontakt in self.kontakti:
            self.listbox.insert(tk.END, str(kontakt))
    #Spremanje kontakta
    def spremi_kontakte(self):
        #if not self.kontakti:
            #messagebox.showwarning("???","Nema sta spremat, samo zrak u tvojoj glavi.")
            #return
        #else:
        #Ako obrišemo jedini/zadnji kontakt->Ne možemo spremiti tu promjenu jer program smatra listbox praznim->pri novom učitavanju se vraća kontakt->funkcionalnost nije potpuna->dopušteno spremanje praznog imenika
        with open("kontakti.csv", "w", newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Ime", "Email", "Telefon"])
            for kontakt in self.kontakti:
                writer.writerow([kontakt.ime, kontakt.email, kontakt.telefon])
            messagebox.showinfo("Ovo kao radi?",f"Valjda spremljeno u: {os.getcwd()}")
    #Učitavanje kontakta
    def ucitaj_kontakte(self):
        if os.path.exists("kontakti.csv"):
            with open("kontakti.csv", "r", newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader) 
                for row in reader:
                    if len(row) == 3:
                        ime, email, telefon = row
                        kontakt = Kontakt(ime, email, telefon)
                        self.kontakti.append(kontakt)
            self.osvjezi_prikaz()
    #Brisanje kontakta
    def obrisi_kontakt(self):
        odabrani_index = self.listbox.curselection()
        if not odabrani_index:
            messagebox.showwarning("???","A sta ti pod treba obrisat? Odaberi nesto.")
            return
        indeks = odabrani_index[0]
        self.kontakti.pop(indeks)
        self.osvjezi_prikaz()
        messagebox.showinfo("Procesiram...","Mora da je uteko.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImenikApp(root)
    root.mainloop()