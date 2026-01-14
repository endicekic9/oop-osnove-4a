import sqlite3

def inicijalizacija():
    conn=sqlite3.connect("imenik.db")
    kursor=conn.cursor()
    sql_naredba="""
    CREATE TABLE IF NOT EXISTS kontakti (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ime_prezime TEXT NOT NULL,
    broj_mobitela NUMERIC NOT NULL
    );
    """
    kursor.execute(sql_naredba)
    conn.commit()
    conn.close()
def dodaj_kontakt(ime_prezime, broj_mobitela):
    unos_ime_prezime=input("Unesite ime i prezime: ")
    unos_broj_mobitela=input("Unesite broj mobitela: ")
    conn=sqlite3.connect("imenik.db")
    kursor=conn.cursor()
    sql_naredba="""
    INSERT INTO kontakti (ime_prezime, broj_mobitela)
    VALUES (?, ?);
    """
    podaci=(unos_ime_prezime, unos_broj_mobitela)
    kursor.execute(sql_naredba, podaci)
    conn.commit()
    conn.close()
    print("Kontakt je uspješno dodan.")
def ispisi_kontakte():
    conn=sqlite3.connect("imenik.db")
    kursor=conn.cursor()
    sql_naredba="""
    SELECT * FROM kontakti;
    """
    kursor.execute(sql_naredba)
    rezultati=kursor.fetchall()
    if rezultati:
        for red in rezultati:
            print(f"ID: {red[0]}, Ime i Prezime: {red[1]}, Broj Mobitela: {red[2]}")
    else:
        print("Nema unesenih kontakata.")
    conn.close()
def obrisi_kontakt():
    unos_id=int(input("Unesite ID kontakta koji želite obrisati: "))
    conn=sqlite3.connect("imenik.db")
    kursor=conn.cursor()
    sql_naredba="""
    DELETE FROM kontakti WHERE id = ?;
    """
    podaci=(unos_id,)
    kursor.execute(sql_naredba, podaci)
    if kursor.rowcount > 0:
        print("Kontakt je uspješno obrisan.")
    else:
        print("Kontakt s unesenim ID-om ne postoji.")
    conn.commit()
    conn.close()
while True:
    print("\nIzbornik:")
    print("1. Dodaj kontakt")
    print("2. Ispiši kontakte")
    print("3. Obriši kontakt")
    print("4. Izlaz")
    izbor=input("Odaberite opciju (1-4): ")
    if izbor=="1":
        dodaj_kontakt(ime_prezime="", broj_mobitela=0)
    elif izbor=="2":
        ispisi_kontakte()
    elif izbor=="3":
        obrisi_kontakt()
    elif izbor=="4":
        print("Izlaz iz programa.")
        break
    else:
        print("Nevažeći odabir. Pokušajte ponovno.")
inicijalizacija()