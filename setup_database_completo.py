#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SETUP DATABASE + IMPORT MENU COMPLETO
PizzaFactory 2.0
"""

import sqlite3
from datetime import datetime

DB_PATH = 'data/pizzeria.db'

# ========================================
# MENU PIZZE (dalla foto)
# ========================================
MENU_PIZZE = [
    # COLONNA SINISTRA
    {"nome": "RIVIERA", "ingredienti": "pomodoro, origano, olive tagg, pom confit, capperi", "prezzo": 9.00},
    {"nome": "MARGHERITA", "ingredienti": "pomodoro, mozzarella", "prezzo": 6.00},
    {"nome": "PROSCIUTTO & FUNGHI", "ingredienti": "pomodoro, mozzarella, prosciutto, funghi", "prezzo": 7.50},
    {"nome": "VEGETARIANA", "ingredienti": "pomodoro, mozzarella, melanz, zucc, peperoni, radicchio", "prezzo": 8.00},
    {"nome": "CAPRICCIOSA", "ingredienti": "pomodoro, mozzarella, pros, funghi, carciofi, olive, salam", "prezzo": 9.00},
    
    # COLONNA CENTRALE (prima metà)
    {"nome": "4 FORMAGGI", "ingredienti": "mozzarella, gorgonzola, fontina, grana, scamorza", "prezzo": 9.00},
    {"nome": "CRUDO & BUFALA", "ingredienti": "pomodoro, bufala fuori cottura, prosciutto crudo", "prezzo": 10.00},
    {"nome": "SICILIANA", "ingredienti": "pomodoro, mozzarella, acciughe, olive, capperi, origano", "prezzo": 8.50},
    {"nome": "GIANNI", "ingredienti": "pomodoro, mozzarella, salamino picc, gorgonzola, cipolla rossa", "prezzo": 8.50},
    {"nome": "BOSCAIOLA", "ingredienti": "pomodoro, mozza, salsiccia, gorgonzola, funghi, noci", "prezzo": 9.00},
    {"nome": "ANTO", "ingredienti": "mozzarella, scamorza, gorgonzola, zucchine, melanzane", "prezzo": 9.00},
    {"nome": "GUSTOSA", "ingredienti": "pomodoro, mozzarella, salsiccia, zucchine, scam aff", "prezzo": 9.00},
    {"nome": "4 SALUMI", "ingredienti": "pomodoro, mozzarella, salsicc, salamino, wurst, prosc", "prezzo": 8.50},
    
    # COLONNA CENTRALE (seconda metà)
    {"nome": "PANCETTA & CIPOLLA", "ingredienti": "pomodoro, mozzarella, scamorza, panc. copp, cipolla rossa", "prezzo": 8.00},
    {"nome": "SPECK & BRIE", "ingredienti": "pomodoro, mozzarella, brie, speck", "prezzo": 9.00},
    {"nome": "GENOVESE", "ingredienti": "mozzarella, pesto, stracchino, patate lesse", "prezzo": 8.50},
    {"nome": "VALE", "ingredienti": "pomodoro, bufala fuori cott, scam aff, salsiccia", "prezzo": 10.50},
    
    # COLONNA DESTRA
    {"nome": "IVAAN", "ingredienti": "mozzarella, sals, gorgonzola, cip rossa, scamorza, olive tagg", "prezzo": 10.00},
    {"nome": "VALDOSTANA", "ingredienti": "pomodoro, mozzarella, prosciutto cotto, fontina", "prezzo": 8.50},
    {"nome": "2 POMODORI", "ingredienti": "bufala fuori cott, pom. giallo, pom. secco, speck", "prezzo": 10.00},
    {"nome": "SALSICCIA & FRIARIELLI", "ingredienti": "mozzarella, salsiccia, friarielli", "prezzo": 9.00},
    {"nome": "PORRO SPECK & NOCI", "ingredienti": "mozzarella, porro, speck, pom. giallo, noci", "prezzo": 10.50},
    {"nome": "STRACCHINO & RUCOLA", "ingredienti": "mozzarella, stracchino, rucola", "prezzo": 7.50},
    {"nome": "FRESCA", "ingredienti": "mozzarella, tonno, cipolla, rucola, olive taggiasche", "prezzo": 9.00},
    {"nome": "SOLE", "ingredienti": "bufala fuori cott, salmone, avocado, pepe", "prezzo": 12.00},
    {"nome": "ESTIVA", "ingredienti": "mozzarella, pomodorino, pesto di rucola, grana", "prezzo": 7.50},
    {"nome": "DEMETRA", "ingredienti": "crema di zucchine, formaggio veg, mopur", "prezzo": 13.00},
    {"nome": "ARES", "ingredienti": "pomodoro, olio basilico, formaggio anacardi", "prezzo": 10.00},
    {"nome": "PERSEO", "ingredienti": "pomodoro, spinaci, tofu alla curcuma", "prezzo": 10.00},
]

# ========================================
# CATEGORIE INGREDIENTI
# ========================================
CATEGORIE_INGREDIENTI = {
    "BASE": ["pomodoro", "mozzarella", "pom", "mozz", "mozza"],
    "LATTICINI": ["bufala", "gorgonzola", "fontina", "grana", "scamorza", "brie", "stracchino", "mozzarella"],
    "CARNI": ["prosciutto", "speck", "salsiccia", "salamino", "wurst", "pancetta", "salam", "salsicc", "pros"],
    "PESCI": ["acciughe", "tonno", "salmone"],
    "VEGETALI": ["funghi", "melanz", "zucc", "peperoni", "radicchio", "carciofi", "olive", "cipolla", "zucchine", "patate", "friarielli", "porro", "rucola", "spinaci"],
    "CREME": ["pesto", "crema di zucchine"],
    "SPEZIE": ["origano", "basilico"],
    "ALTRO": ["capperi", "noci", "avocado", "pepe", "olio"],
    "VEGANI": ["formaggio veg", "mopur", "formaggio anacardi", "tofu"],
}

# ========================================
# FORMATI DISPONIBILI
# ========================================
FORMATI = [
    {"nome": "pizza", "descrizione": "Pizza classica tonda", "fattore_prezzo": 1.0},
    {"nome": "pinsa", "descrizione": "Pinsa romana", "fattore_prezzo": 1.2},
    {"nome": "baby", "descrizione": "Pizza baby (piccola)", "fattore_prezzo": 0.7},
    {"nome": "teglia", "descrizione": "Pizza in teglia (al trancio)", "fattore_prezzo": 0.5},
    {"nome": "maxi", "descrizione": "Pizza maxi (famiglia)", "fattore_prezzo": 1.8},
]

def crea_database():
    """Crea tutte le tabelle necessarie"""
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("🗄️  Creazione database...")
    
    # ========================================
    # TABELLA PRODOTTI
    # ========================================
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Prodotti (
            ID_Prodotto INTEGER PRIMARY KEY AUTOINCREMENT,
            Nome_Prodotto TEXT NOT NULL,
            Formato TEXT DEFAULT 'pizza',
            Prezzo_Base REAL NOT NULL,
            Descrizione TEXT,
            Ingredienti TEXT,
            Allergeni TEXT,
            Disponibile INTEGER DEFAULT 1,
            Preparazione_Minuti INTEGER DEFAULT 5,
            Categoria TEXT,
            Ordinamento INTEGER DEFAULT 0,
            Foto TEXT,
            Data_Creazione TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            Data_Modifica TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # ========================================
    # TABELLA INGREDIENTI
    # ========================================
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Ingredienti (
            ID_Ingrediente INTEGER PRIMARY KEY AUTOINCREMENT,
            Nome_Ingrediente TEXT NOT NULL UNIQUE,
            Categoria TEXT,
            Prezzo_Extra REAL DEFAULT 0,
            Allergeni TEXT,
            Disponibile INTEGER DEFAULT 1,
            Ordinamento INTEGER DEFAULT 0
        )
    ''')
    
    # ========================================
    # TABELLA PRODOTTI_INGREDIENTI (relazione)
    # ========================================
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Prodotti_Ingredienti (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            ID_Prodotto INTEGER NOT NULL,
            ID_Ingrediente INTEGER NOT NULL,
            Quantita REAL DEFAULT 1,
            FOREIGN KEY (ID_Prodotto) REFERENCES Prodotti(ID_Prodotto),
            FOREIGN KEY (ID_Ingrediente) REFERENCES Ingredienti(ID_Ingrediente)
        )
    ''')
    
    # ========================================
    # TABELLA FORMATI
    # ========================================
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Formati (
            ID_Formato INTEGER PRIMARY KEY AUTOINCREMENT,
            Nome_Formato TEXT NOT NULL UNIQUE,
            Descrizione TEXT,
            Fattore_Prezzo REAL DEFAULT 1.0,
            Disponibile INTEGER DEFAULT 1
        )
    ''')
    
    # ========================================
    # TABELLA CLIENTI
    # ========================================
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Clienti (
            ID_Cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            Nome TEXT,
            Cognome TEXT,
            Telefono TEXT UNIQUE NOT NULL,
            Indirizzo TEXT,
            Civico TEXT,
            Citta TEXT DEFAULT 'Chieri',
            CAP TEXT DEFAULT '10023',
            Note TEXT,
            Rating INTEGER DEFAULT 0,
            Totale_Ordini INTEGER DEFAULT 0,
            Data_Creazione TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # ========================================
    # TABELLA ORDINI
    # ========================================
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Ordini (
            ID_Ordine INTEGER PRIMARY KEY AUTOINCREMENT,
            ID_Cliente INTEGER,
            ID_Serata INTEGER,
            Tipo_Ordine INTEGER NOT NULL,
            Numero_Tavolo INTEGER,
            Orario_Ritiro TEXT,
            Totale REAL NOT NULL,
            Sovrapprezzo_Consegna REAL DEFAULT 0,
            Metodo_Pagamento TEXT DEFAULT 'Contanti',
            Note TEXT,
            Stato TEXT DEFAULT 'in_preparazione',
            Data_Ordine TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            Data_Completamento TIMESTAMP,
            FOREIGN KEY (ID_Cliente) REFERENCES Clienti(ID_Cliente)
        )
    ''')
    
    # ========================================
    # TABELLA ORDINI_PRODOTTI
    # ========================================
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Ordini_Prodotti (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            ID_Ordine INTEGER NOT NULL,
            ID_Prodotto INTEGER NOT NULL,
            Quantita INTEGER NOT NULL,
            Prezzo_Unitario REAL NOT NULL,
            Formato TEXT DEFAULT 'pizza',
            Note TEXT,
            FOREIGN KEY (ID_Ordine) REFERENCES Ordini(ID_Ordine),
            FOREIGN KEY (ID_Prodotto) REFERENCES Prodotti(ID_Prodotto)
        )
    ''')
    
    conn.commit()
    print("✅ Tabelle create!")
    return conn

def popola_formati(conn):
    """Popola tabella Formati"""
    
    cursor = conn.cursor()
    
    print("\n📐 Popolamento formati...")
    
    for formato in FORMATI:
        cursor.execute('''
            INSERT OR IGNORE INTO Formati (Nome_Formato, Descrizione, Fattore_Prezzo)
            VALUES (?, ?, ?)
        ''', (formato['nome'], formato['descrizione'], formato['fattore_prezzo']))
    
    conn.commit()
    print(f"✅ {len(FORMATI)} formati inseriti!")

def estrai_e_popola_ingredienti(conn):
    """Estrae tutti gli ingredienti unici dalle pizze e li categorizza"""
    
    cursor = conn.cursor()
    
    print("\n🌿 Estrazione ingredienti...")
    
    # Estrai tutti gli ingredienti unici
    ingredienti_unici = set()
    for pizza in MENU_PIZZE:
        ingredienti = pizza['ingredienti'].split(', ')
        for ing in ingredienti:
            # Pulisci e normalizza
            ing_clean = ing.strip().lower()
            ingredienti_unici.add(ing_clean)
    
    print(f"   Trovati {len(ingredienti_unici)} ingredienti unici")
    
    # Categorizza e inserisci
    for ingrediente in sorted(ingredienti_unici):
        categoria = "ALTRO"  # Default
        
        # Cerca categoria
        for cat, keywords in CATEGORIE_INGREDIENTI.items():
            for keyword in keywords:
                if keyword.lower() in ingrediente:
                    categoria = cat
                    break
            if categoria != "ALTRO":
                break
        
        # Determina allergeni
        allergeni = []
        if any(x in ingrediente for x in ['mozz', 'bufala', 'gorg', 'font', 'scam', 'brie', 'stracc', 'grana', 'formaggio']):
            allergeni.append('Latticini')
        if 'glut' in ingrediente or 'pane' in ingrediente:
            allergeni.append('Glutine')
        
        allergeni_str = ', '.join(allergeni) if allergeni else None
        
        # Prezzo extra (alcuni ingredienti costano di più)
        prezzo_extra = 0.0
        if ingrediente in ['bufala', 'gorgonzola', 'salmone', 'avocado', 'pesto', 'speck']:
            prezzo_extra = 1.5
        elif ingrediente in ['prosciutto', 'salsiccia', 'tonno', 'brie']:
            prezzo_extra = 1.0
        elif ingrediente in ['funghi', 'olive', 'rucola']:
            prezzo_extra = 0.5
        
        cursor.execute('''
            INSERT OR IGNORE INTO Ingredienti (Nome_Ingrediente, Categoria, Prezzo_Extra, Allergeni)
            VALUES (?, ?, ?, ?)
        ''', (ingrediente, categoria, prezzo_extra, allergeni_str))
    
    conn.commit()
    print(f"✅ {len(ingredienti_unici)} ingredienti categorizzati e inseriti!")

def popola_menu_pizze(conn):
    """Popola tabella Prodotti con menu pizze"""
    
    cursor = conn.cursor()
    
    print("\n🍕 Popolamento menu pizze...")
    
    for idx, pizza in enumerate(MENU_PIZZE, start=1):
        # Determina allergeni (tutte le pizze hanno glutine e latticini di base)
        allergeni = "Glutine, Latticini"
        
        # Aggiungi allergeni speciali
        ingredienti_lower = pizza['ingredienti'].lower()
        if any(x in ingredienti_lower for x in ['pesce', 'tonno', 'salmone', 'acciughe']):
            allergeni += ", Pesce"
        if any(x in ingredienti_lower for x in ['noci']):
            allergeni += ", Frutta a guscio"
        
        # Determina categoria
        categoria = "Classiche"
        if any(x in pizza['nome'].upper() for x in ['DEMETRA', 'ARES', 'PERSEO']):
            categoria = "Vegane"
        elif pizza['prezzo'] >= 10.00:
            categoria = "Speciali"
        
        cursor.execute('''
            INSERT INTO Prodotti (
                Nome_Prodotto, Formato, Prezzo_Base, Descrizione, 
                Ingredienti, Allergeni, Categoria, Ordinamento,
                Disponibile, Preparazione_Minuti
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            pizza['nome'],
            'pizza',
            pizza['prezzo'],
            f"Pizza {pizza['nome']}",
            pizza['ingredienti'],
            allergeni,
            categoria,
            idx,
            1,  # Disponibile
            5   # Tempo preparazione
        ))
    
    conn.commit()
    print(f"✅ {len(MENU_PIZZE)} pizze inserite!")

def collega_pizze_ingredienti(conn):
    """Crea relazioni tra pizze e ingredienti"""
    
    cursor = conn.cursor()
    
    print("\n🔗 Collegamento pizze-ingredienti...")
    
    # Per ogni pizza
    cursor.execute('SELECT ID_Prodotto, Nome_Prodotto, Ingredienti FROM Prodotti WHERE Formato = "pizza"')
    pizze = cursor.fetchall()
    
    collegamenti = 0
    
    for id_prodotto, nome, ingredienti_str in pizze:
        ingredienti = [ing.strip().lower() for ing in ingredienti_str.split(',')]
        
        for ingrediente in ingredienti:
            # Trova ID ingrediente
            cursor.execute('SELECT ID_Ingrediente FROM Ingredienti WHERE Nome_Ingrediente = ?', (ingrediente,))
            result = cursor.fetchone()
            
            if result:
                id_ingrediente = result[0]
                
                # Crea collegamento
                cursor.execute('''
                    INSERT INTO Prodotti_Ingredienti (ID_Prodotto, ID_Ingrediente, Quantita)
                    VALUES (?, ?, ?)
                ''', (id_prodotto, id_ingrediente, 1.0))
                
                collegamenti += 1
    
    conn.commit()
    print(f"✅ {collegamenti} collegamenti creati!")

def stampa_statistiche(conn):
    """Stampa statistiche database"""
    
    cursor = conn.cursor()
    
    print("\n" + "="*60)
    print("📊 STATISTICHE DATABASE")
    print("="*60)
    
    cursor.execute('SELECT COUNT(*) FROM Prodotti')
    print(f"🍕 Prodotti: {cursor.fetchone()[0]}")
    
    cursor.execute('SELECT COUNT(*) FROM Ingredienti')
    print(f"🌿 Ingredienti: {cursor.fetchone()[0]}")
    
    cursor.execute('SELECT COUNT(*) FROM Formati')
    print(f"📐 Formati: {cursor.fetchone()[0]}")
    
    cursor.execute('SELECT COUNT(*) FROM Prodotti_Ingredienti')
    print(f"🔗 Collegamenti: {cursor.fetchone()[0]}")
    
    print("\n📋 INGREDIENTI PER CATEGORIA:")
    cursor.execute('SELECT Categoria, COUNT(*) FROM Ingredienti GROUP BY Categoria ORDER BY COUNT(*) DESC')
    for categoria, count in cursor.fetchall():
        print(f"   • {categoria}: {count}")
    
    print("\n🍕 PIZZE PIÙ CARE:")
    cursor.execute('SELECT Nome_Prodotto, Prezzo_Base FROM Prodotti ORDER BY Prezzo_Base DESC LIMIT 5')
    for nome, prezzo in cursor.fetchall():
        print(f"   • {nome}: €{prezzo:.2f}")
    
    print("="*60)

def main():
    """Main function"""
    
    print("="*60)
    print("🍕 PIZZAFACTORY 2.0 - SETUP DATABASE")
    print("="*60)
    print()
    
    try:
        # 1. Crea database e tabelle
        conn = crea_database()
        
        # 2. Popola formati
        popola_formati(conn)
        
        # 3. Estrai e popola ingredienti
        estrai_e_popola_ingredienti(conn)
        
        # 4. Popola menu pizze
        popola_menu_pizze(conn)
        
        # 5. Collega pizze e ingredienti
        collega_pizze_ingredienti(conn)
        
        # 6. Statistiche
        stampa_statistiche(conn)
        
        conn.close()
        
        print("\n✅ DATABASE PRONTO!")
        print(f"📂 Percorso: {DB_PATH}")
        print()
        
    except Exception as e:
        print(f"\n❌ ERRORE: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
