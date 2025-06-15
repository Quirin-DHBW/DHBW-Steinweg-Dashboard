import sqlite3
import random
import datetime

def gen_random_entries(account_structure, years, min_entries, max_entries):
    """
    This function fills the databank with random data
    """
    for year in years:
        for month in range(1, 13):
            for category, accounts in account_structure.items():
                for account, description in accounts.items():
                    for _ in range(random.randint(min_entries, max_entries)):
                        day = random.randint(1, 28)
                        date = datetime.date(year, month, day)
                        amount = round(random.uniform(100, 3000), 2)

                        cursor.execute("""
                            INSERT INTO buchungssaetze (konto, bezeichnung, kategorie, buchungsdatum, betrag)
                            VALUES (?, ?, ?, ?, ?)
                        """, (account, description, category, date, amount)) 

        abteilungen = ["Controlling", "Finanz", "Geschäftsführung", "Technik", "Buchhaltung", "Facility Management", "Fuhrpark", "Logistik", "Produktion", "Vertrieb", "IT", "HR"]
        for abteilung in abteilungen:
            cursor.execute("""
                INSERT INTO abteilungen (abteilung, budget, year)
                VALUES (?, ?, ?)
            """, (abteilung, random.randint(100000, 500000), year)) 


conn = sqlite3.connect("einzelkonten.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS buchungssaetze (
        buchungs_id INTEGER PRIMARY KEY AUTOINCREMENT,
        konto INTEGER,
        fachbereich INTEGER,
        bezeichnung TEXT,
        kategorie TEXT,
        buchungsdatum DATE,
        betrag REAL,
        FOREIGN KEY(fachbereich) REFERENCES abteilungen(abteilungs_id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS abteilungen (
        abteilungs_id INTEGER PRIMARY KEY AUTOINCREMENT,
        abteilung TEXT,
        budget REAL,
        year INTEGER
    )           
""")


account_structure = {
    "Raumkosten": {
        4210: "Miete (unbewegliche Wirtschaftsgüter)",
        4230: "Heizung",
        4240: "Gas, Strom, Wasser",
        4250: "Reinigung"
    },
    "Nicht abziehbare Vorsteuer": {
        4320: "Gewerbesteuer",
        4340: "Sonstige Betriebssteuern",
        4360: "Versicherungen",
        4366: "Versicherungen für Gebäude"
    },
    "Fahrzeugkosten": {
        4510: "Kfz-Steuer",
        4520: "Fahrzeug-Versicherungen",
        4530: "Laufende Fahrzeug-Betriebskosten",
        4540: "Fahrzeug-Reparaturen"
    },
    "Werbekosten": {
        4660: "Reisekosten Arbeitnehmer",
        4663: "Fahrtkosten",
        4664: "Verpflegungsmehraufwand",
        4666: "Übernachtungsaufwand"
    },
    "Kosten der Warenabgabe": {
        4710: "Verpackungsmaterial",
        4730: "Ausgangsfrachten",
        4750: "Transportversicherungen",
        4760: "Verkaufsprovisionen"
    },
    "Sonstige betriebliche Aufwendungen": {
        4920: "Telefon",
        4925: "Internetkosten",
        4930: "Bürobedarf",
        4945: "Fortbildungskosten"
    },
    "Reparaturen und Instandhaltung": {
        4801: "Reparaturen Bauten",
        4805: "Reparaturen Betriebsausstattung",
        4806: "Wartung Hard-/Software",
        4809: "Sonstige Reparaturen"
    }
}

min_entries = 1
max_entries = 10
years = [2022, 2023, 2024]

gen_random_entries(account_structure, years, min_entries, max_entries)
conn.commit()
conn.close()

print("Databank generation successfull.")