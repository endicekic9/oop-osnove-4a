import tkinter as tk
from tkinter import messagebox, filedialog
import csv
import os

class Kontakt:
    def __init__(self, ime, email, telefon):
        self.ime = ime
        self.email = email
        self.telefon = telefon

    def __str__(self):
        return f"{self.ime} {self.email} {self.telefon}"

class ImenikApp:
    def __init__(self, root):
        self.root = root
        self.kontakti = []

        root.title("Imenik")
        root.geometry("500x400")

        root.columnconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)

        unos_frame = tk.Frame(root, padx=10, pady=10)
        unos_frame.grid(row=0, column=0, sticky="EW")

        tk.Label(unos_frame, text="Ime:").grid(row=0, column=0, sticky="W")
        self.ime_entry = tk.Entry(unos_frame)
        self.ime_entry.grid(row=0, column=1, padx=10, pady=5, sticky="EW")

        tk.Label(unos_frame, text="Email:").grid(row=1, column=0, sticky="W")
        self.email_entry = tk.Entry(unos_frame)
        self.email_entry.grid(row=1, column=1, padx=10, pady=5, sticky="EW")

        tk.Label(unos_frame, text="Telefon:").grid(row=2, column=0, sticky="W")
        self.telefon_entry = tk.Entry(unos_frame)
        self.telefon_entry.grid(row=2, column=1, padx=10, pady=5, sticky="EW")

        unos_frame.columnconfigure(1, weight=1)

        dodaj_btn = tk.Button(unos_frame, text="Dodaj kontakt", command=self.dodaj_kontakt)
        dodaj_btn.grid(row=3, column=0, columnspan=2, pady=10)

        lista_frame = tk.Frame(root, padx=10, pady=10)
        lista_frame.grid(row=1, column=0, sticky="NSEW")

        lista_frame.columnconfigure(0, weight=1)
        lista_frame.rowconfigure(0, weight=1)

        self.listbox = tk.Listbox(lista_frame)
        self.listbox.grid(row=0, column=0, sticky="NSEW")

        scrollbar = tk.Scrollbar(lista_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="NS")
        self.listbox.config(yscrollcommand=scrollbar.set)

        gumbi_frame = tk.Frame(root, padx=10, pady=10)
        gumbi_frame.grid(row=2, column=0, sticky="EW")

        spremi_btn = tk.Button(gumbi_frame, text="Spremi kontakte", command=self.spremi_kontakte)
        spremi_btn.grid(row=0, column=0, padx=5, pady=5)