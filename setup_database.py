#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SETUP DATABASE - PizzaFactory 2.0
Crea tutte le tabelle necessarie (vuote)
"""

import sqlite3
import os

DB_PATH = 'data/pizzeria.db'

def crea_database():
    """Crea database e tutte le tabelle"""
    
    # Crea cartella data se non esiste
    os.makedirs('data', exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("=" * 60)
    print("🗄️  CREAZIONE DATABASE PIZZAFACTORY 2.0")
    print("=" * 60)
    print()
    
    # ========================================
    # TABELLA PRODOTTI
    # ========================================
    print("📋 Creazione tabella Prodotti...")
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
            Data_Creazione TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    print("   ✅ Tabella Prodotti creata")
    
    # ========================================
    # TABELLA INGREDIENTI
    # ========================================
    print("📋 Creazione tabella Ingredienti...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Ingredienti (
            ID_Ingrediente INTEGER PRIMARY KEY AUTOINCREMENT,
            Nome_Ingrediente TEXT NOT NULL UNIQUE,
            Categoria TEXT,
            Prezzo REAL DEFAULT 1.00,
            Disponibile INTEGER DEFAULT 1,
            Allergeni TEXT,
            Ordinamento INTEGER DEFAULT 0
        )
    ''')
    print("   ✅ Tabella Ingredienti creata")
    
    # ========================================
    # TABELLA CLIENTI
    # ========================================
    print("📋 Creazione tabella Clienti...")
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
            Latitudine REAL,
            Longitudine REAL,
            Data_Creazione TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            Data_Ultima_Modifica TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    print("   ✅ Tabella Clienti creata")
    
    # ========================================
    # TABELLA ORDINI
    # ========================================
    print("📋 Creazione tabella Ordini...")
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
    print("   ✅ Tabella Ordini creata")
    
    # ========================================
    # TABELLA ORDINI_PRODOTTI
    # ========================================
    print("📋 Creazione tabella Ordini_Prodotti...")
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
    print("   ✅ Tabella Ordini_Prodotti creata")
    
    # ========================================
    # TABELLA PRODOTTI_INGREDIENTI (relazione N-N)
    # ========================================
    print("📋 Creazione tabella Prodotti_Ingredienti...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Prodotti_Ingredienti (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            ID_Prodotto INTEGER NOT NULL,
            ID_Ingrediente INTEGER NOT NULL,
            Quantita REAL DEFAULT 1.0,
            FOREIGN KEY (ID_Prodotto) REFERENCES Prodotti(ID_Prodotto),
            FOREIGN KEY (ID_Ingrediente) REFERENCES Ingredienti(ID_Ingrediente)
        )
    ''')
    print("   ✅ Tabella Prodotti_Ingredienti creata")
    
    # ========================================
    # TABELLA SERATE
    # ========================================
    print("📋 Creazione tabella Serate...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Serate (
            ID_Serata INTEGER PRIMARY KEY AUTOINCREMENT,
            Data_Apertura TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            Data_Chiusura TIMESTAMP,
            Stato TEXT DEFAULT 'aperta',
            Totale_Incasso REAL DEFAULT 0,
            Totale_Ordini INTEGER DEFAULT 0,
            Note TEXT
        )
    ''')
    print("   ✅ Tabella Serate creata")
    
    # ========================================
    # TABELLA PAGAMENTI
    # ========================================
    print("📋 Creazione tabella Pagamenti...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Pagamenti (
            ID_Pagamento INTEGER PRIMARY KEY AUTOINCREMENT,
            ID_Ordine INTEGER NOT NULL,
            Metodo TEXT NOT NULL,
            Importo REAL NOT NULL,
            Data_Pagamento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            Note TEXT,
            FOREIGN KEY (ID_Ordine) REFERENCES Ordini(ID_Ordine)
        )
    ''')
    print("   ✅ Tabella Pagamenti creata")
    
    # ========================================
    # TABELLA SCARTI (gestione inventario)
    # ========================================
    print("📋 Creazione tabella Scarti...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Scarti (
            ID_Scarto INTEGER PRIMARY KEY AUTOINCREMENT,
            ID_Serata INTEGER NOT NULL,
            ID_Prodotto INTEGER,
            Quantita INTEGER NOT NULL,
            Motivo TEXT,
            Data_Scarto TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (ID_Serata) REFERENCES Serate(ID_Serata),
            FOREIGN KEY (ID_Prodotto) REFERENCES Prodotti(ID_Prodotto)
        )
    ''')
    print("   ✅ Tabella Scarti creata")
    
    # ========================================
    # INDICI PER PERFORMANCE
    # ========================================
    print("\n🔍 Creazione indici per performance...")
    
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_clienti_telefono ON Clienti(Telefono)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_ordini_data ON Ordini(Data_Ordine)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_ordini_cliente ON Ordini(ID_Cliente)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_ordini_stato ON Ordini(Stato)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_prodotti_formato ON Prodotti(Formato)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_prodotti_disponibile ON Prodotti(Disponibile)')
    
    print("   ✅ Indici creati")
    
    conn.commit()
    
    # ========================================
    # STATISTICHE
    # ========================================
    print("\n" + "=" * 60)
    print("📊 STATISTICHE DATABASE")
    print("=" * 60)
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tabelle = cursor.fetchall()
    
    print(f"\n✅ {len(tabelle)} tabelle create:")
    for tabella in tabelle:
        nome_tabella = tabella[0]
        if nome_tabella != 'sqlite_sequence':  # Tabella interna SQLite
            cursor.execute(f'SELECT COUNT(*) FROM {nome_tabella}')
            count = cursor.fetchone()[0]
            print(f"   • {nome_tabella}: {count} record")
    
    print("\n" + "=" * 60)
    print("✅ DATABASE PRONTO!")
    print("=" * 60)
    print(f"📂 Percorso: {DB_PATH}")
    print(f"📏 Dimensione: {os.path.getsize(DB_PATH) / 1024:.2f} KB")
    print()
    print("🚀 PROSSIMI STEP:")
    print("   1. python popola_pizze.py")
    print("   2. python popola_ingredienti.py")
    print("   3. python app.py")
    print("=" * 60)
    print()
    
    conn.close()

def main():
    """Main function"""
    
    # Verifica se database esiste già
    if os.path.exists(DB_PATH):
        print(f"⚠️  Database esistente trovato: {DB_PATH}")
        risposta = input("Vuoi sovrascriverlo? Tutti i dati saranno persi! (s/n): ")
        
        if risposta.lower() != 's':
            print("❌ Operazione annullata")
            return
        
        # Backup del database esistente
        import shutil
        from datetime import datetime
        
        backup_name = f"data/pizzeria_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        shutil.copy(DB_PATH, backup_name)
        print(f"💾 Backup creato: {backup_name}")
        
        # Elimina database esistente
        os.remove(DB_PATH)
        print("🗑️  Database esistente eliminato")
    
    try:
        crea_database()
        
    except Exception as e:
        print(f"\n❌ ERRORE: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
