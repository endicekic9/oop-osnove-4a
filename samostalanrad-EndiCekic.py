import tkinter as tk

class Ucenik:
    def __init__(self, ime, prezime, razred):
        self.ime=ime
        self.prezime=prezime
        self.razred=razred
    def __str__(self):
        return(f"Učenik {self.prezime}, {self.ime} razreda {self.razred}")
#print(Ucenik("Pero","Perić","4.a"))
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
        #Listbox
        listbox=tk.Listbox(prikaz_frame)
        listbox.grid(row=0,column=0,sticky="NSEW")
        #Scrollbar listboxa
        scrollbar = tk.Scrollbar(prikaz_frame,orient="vertical",command=listbox.yview)
        scrollbar.grid(row=0,column=1,sticky="NS")
        listbox.config(yscrollcommand=scrollbar.set)
    #Dodavanje ucenika
    def dodaj_ucenika(self):
        ime=self.ime_entry.get()
        prezime=self.prezime_entry.get()
        razred=self.razred_entry.get()
    #Osvjezavanje prikaza
    def osvjezi_prikaz(self):
        self.listbox.delete(0,tk.END)
        for ucenik in self.ucenici:
            self.listbox.insert(tk.END,str(ucenik))
    #Odabir ucenika
    def odaberi_ucenika(self,event):
        index=self.listbox.curselection()[0]
        self.odabrani_ucenik_index=index
        ucenik=self.ucenici[index]
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

#Pokretanje
if __name__=="__main__":
    root=tk.Tk()
    app=EvidencijaApp(root)
    root.mainloop()