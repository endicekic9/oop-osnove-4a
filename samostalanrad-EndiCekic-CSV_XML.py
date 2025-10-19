import tkinter as tk
import csv
import xml.etree.ElementTree as ET
from xml.dom import minidom
#Definiranje klase učenik
class Ucenik:
    ucenici=[]
    def __init__(self, ime, prezime, razred):
        self.ime=ime
        self.prezime=prezime
        self.razred=razred
    def __str__(self):
        return(f"Učenik {self.prezime}, {self.ime} razreda {self.razred}")
#Definiranje glavne klase
class EvidencijaApp:
    def __init__(self,root):
        self.root=root
        self.root.title("Evidencija učenika")
        self.root.geometry("500x400")
        #Inicijalizacija podataka
        self.ucenici=[]
        self.odabrani_ucenik_index=None
        #Konfig responzivnosti
        self.root.columnconfigure(0,weight=1)
        self.root.rowconfigure(1,weight=1)
        #Okvir za unos
        unos_frame=tk.Frame(self.root,padx=10,pady=10)
        unos_frame.grid(row=0,column=0,sticky="EW")
        #Okvir prikaza
        prikaz_frame=tk.Frame(self.root,padx=10,pady=10)
        prikaz_frame.grid(row=1,column=0,sticky="NSEW")
        #Responzivnost unutar okvira prikaza
        prikaz_frame.columnconfigure(0,weight=1)
        prikaz_frame.rowconfigure(0,weight=1)
        #Widgeti za unos
        #Ime
        tk.Label(unos_frame,text="Ime:").grid(row=0,column=0,padx=5,pady=5,sticky="W")
        self.ime_entry=tk.Entry(unos_frame)
        self.ime_entry.grid(row=0,column=1,padx=5,pady=5,sticky="EW")
        #Prezime
        tk.Label(unos_frame,text="Prezime:").grid(row=1,column=0,padx=5,pady=5,sticky="W")
        self.prezime_entry=tk.Entry(unos_frame)
        self.prezime_entry.grid(row=1,column=1,padx=5,pady=5,sticky="EW")
        #Razred
        tk.Label(unos_frame,text="Razred:").grid(row=2,column=0,padx=5,pady=5,sticky="W")
        self.razred_entry=tk.Entry(unos_frame)
        self.razred_entry.grid(row=2,column=1,padx=5,pady=5,sticky="EW")
        #Gumbi
        self.dodaj_gumb=tk.Button(unos_frame,text="Dodaj učenika",command=self.dodaj_ucenika)
        self.dodaj_gumb.grid(row=3,column=0,padx=5,pady=10)
        self.spremi_gumb=tk.Button(unos_frame,text="Spremi izmjene",command=self.spremi_izmjene)
        self.spremi_gumb.grid(row=3,column=1,padx=5,pady=10,sticky="W")
        #CSV gumbi
        self.spremi_gumb_CSV=tk.Button(unos_frame,text="Spremi CSV",command=lambda:self.spremi_u_CSV())
        self.spremi_gumb_CSV.grid(row=4,column=1,padx=5,pady=10,sticky="W")
        self.učitaj_gumb_CSV=tk.Button(unos_frame,text="Učitaj CSV",command=lambda:self.ucitaj_CSV())
        self.učitaj_gumb_CSV.grid(row=4,column=0,padx=5,pady=10,sticky="W")
        #XML gumbi
        self.spremi_gumb_XML=tk.Button(unos_frame,text="Spremi XML",command=lambda:self.spremi_u_XML())
        self.spremi_gumb_XML.grid(row=5,column=1,padx=5,pady=10,sticky="W")
        self.učitaj_gumb_XML=tk.Button(unos_frame,text="Učitaj XML",command=lambda:self.ucitaj_iz_XML())
        self.učitaj_gumb_XML.grid(row=5,column=0,padx=5,pady=10,sticky="W")
        #Listbox
        self.listbox=tk.Listbox(prikaz_frame)
        self.listbox.grid(row=0,column=0,sticky="NSEW")
        self.listbox.bind("<<ListboxSelect>>", self.odaberi_ucenika)
        #Scrollbar listboxa
        scrollbar=tk.Scrollbar(prikaz_frame,orient="vertical",command=self.listbox.yview)
        scrollbar.grid(row=0,column=1,sticky="NS")
        self.listbox.config(yscrollcommand=scrollbar.set)
    #Dodavanje ucenika
    def dodaj_ucenika(self):
        ime = self.ime_entry.get().strip()
        prezime = self.prezime_entry.get().strip()
        razred = self.razred_entry.get().strip()
        if ime and prezime and razred:
            ucenik=Ucenik(ime, prezime, razred)
            self.ucenici.append(ucenik)
            self.osvjezi_prikaz()
    #Osvjezavanje prikaza
    def osvjezi_prikaz(self):
        self.listbox.delete(0,tk.END)
        for ucenik in self.ucenici:
            self.listbox.insert(tk.END,str(ucenik))
    #Odabir ucenika
    def odaberi_ucenika(self,event):
        index=self.listbox.curselection()
        if index:
            self.odabrani_ucenik_index=index[0]
            ucenik=self.ucenici[self.odabrani_ucenik_index]
            self.ime_entry.delete(0,tk.END)
            self.ime_entry.insert(0,ucenik.ime)
            self.prezime_entry.delete(0,tk.END)
            self.prezime_entry.insert(0,ucenik.prezime)
            self.razred_entry.delete(0,tk.END)
            self.razred_entry.insert(0,ucenik.razred)
    #Spremanje izmjena
    def spremi_izmjene(self):
        if self.odabrani_ucenik_index is not None:
            ucenik=self.ucenici[self.odabrani_ucenik_index]
            ucenik.ime=self.ime_entry.get()
            ucenik.prezime=self.prezime_entry.get()
            ucenik.razred=self.razred_entry.get()
            self.osvjezi_prikaz()
            self.ime_entry.delete(0, tk.END)
            self.prezime_entry.delete(0, tk.END)
            self.razred_entry.delete(0, tk.END)
            self.odabrani_ucenik_index = None
    #Spremanje u CSV
    def spremi_u_CSV(self):
        filename="ucenici.csv"
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Ime", "Prezime", "Razred"])
            for ucenik in self.ucenici:
               writer.writerow([ucenik.ime, ucenik.prezime, ucenik.razred])
        print(f"Lista učenika je spremljena u {filename}")
    #Ucitavanje CSV
    def ucitaj_CSV(self):
        filename="ucenici.csv"
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                ime, prezime, razred=row
                ucenik=Ucenik(ime, prezime, razred)
                self.ucenici.append(ucenik)
            print(f"Lista učenika je učitana iz {filename}")
            self.osvjezi_prikaz()
            return self.ucenici
    #Spremanje u XML
    def spremi_u_XML(self):
        filename="ucenici.xml"
        root = ET.Element("Ucenici")
        for ucenik in self.ucenici:
            ucenik_elem = ET.SubElement(root, "Ucenik")
            ime_elem = ET.SubElement(ucenik_elem, "Ime")
            ime_elem.text = ucenik.ime
            prezime_elem = ET.SubElement(ucenik_elem, "Prezime")
            prezime_elem.text = ucenik.prezime
            razred_elem = ET.SubElement(ucenik_elem, "Razred")
            razred_elem.text = ucenik.razred
        tree = ET.ElementTree(root)
        tree.write("ucenici.xml", encoding='utf-8', xml_declaration=True)
        print("Lista učenika je spremljena u ucenici.xml")
    #Ucitavanje XML
    def ucitaj_iz_XML(self):
        filename="ucenici.xml"
        tree = ET.parse(filename)
        root = tree.getroot()
        for ucenik_elem in root.findall('Ucenik'):
            ime = ucenik_elem.find('Ime').text
            prezime = ucenik_elem.find('Prezime').text
            razred = ucenik_elem.find('Razred').text
            ucenik = Ucenik(ime, prezime, razred)
            self.ucenici.append(ucenik)
        print("Lista učenika je učitana iz ucenici.xml")
        self.osvjezi_prikaz()
        return self.ucenici

#Pokretanje
if __name__=="__main__":
    root=tk.Tk()
    app=EvidencijaApp(root)
    root.mainloop()
