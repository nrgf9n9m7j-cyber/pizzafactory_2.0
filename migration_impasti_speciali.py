#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MIGRATION: Sistema Impasti Speciali
Crea tabelle per gestione impasti con tracciamento movimenti
"""

import sqlite3
import sys
from datetime import datetime

DB_PATH = 'data/pizzeria.db'

def migration_up():
    """Crea tabelle impasti speciali"""
    print("🌾 MIGRATION: Creazione sistema impasti speciali...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # ==========================================
        # TABELLA IMPASTI SPECIALI
        # ==========================================
        print("📦 Creazione tabella Impasti_Speciali...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Impasti_Speciali (
                ID_Impasto INTEGER PRIMARY KEY AUTOINCREMENT,
                Nome TEXT NOT NULL UNIQUE,
                Sovrapprezzo REAL DEFAULT 2.00,
                Quantita_Disponibile INTEGER DEFAULT 0,
                Soglia_Minima INTEGER DEFAULT 0,
                Attivo INTEGER DEFAULT 1,
                Data_Ultimo_Carico TIMESTAMP,
                Note TEXT,
                Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                Updated_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("   ✅ Tabella Impasti_Speciali creata")
        
        # ==========================================
        # TABELLA MOVIMENTI IMPASTI
        # ==========================================
        print("📦 Creazione tabella Movimenti_Impasti...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Movimenti_Impasti (
                ID_Movimento INTEGER PRIMARY KEY AUTOINCREMENT,
                ID_Impasto INTEGER NOT NULL,
                Tipo_Movimento TEXT NOT NULL CHECK(Tipo_Movimento IN ('Carico', 'Scarico', 'Rettifica')),
                Quantita INTEGER NOT NULL,
                Quantita_Precedente INTEGER,
                Quantita_Nuova INTEGER,
                Note TEXT,
                Data_Movimento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (ID_Impasto) REFERENCES Impasti_Speciali(ID_Impasto)
            )
        ''')
        print("   ✅ Tabella Movimenti_Impasti creata")
        
        # ==========================================
        # INDICI PER PERFORMANCE
        # ==========================================
        print("📦 Creazione indici...")
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_impasti_attivo ON Impasti_Speciali(Attivo)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_impasti_qty ON Impasti_Speciali(Quantita_Disponibile)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_movimenti_impasto ON Movimenti_Impasti(ID_Impasto)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_movimenti_data ON Movimenti_Impasti(Data_Movimento)')
        print("   ✅ Indici creati")
        
        # ==========================================
        # TRIGGER AUTO-UPDATE
        # ==========================================
        print("📦 Creazione trigger...")
        cursor.execute('''
            CREATE TRIGGER IF NOT EXISTS update_impasti_timestamp 
            AFTER UPDATE ON Impasti_Speciali
            FOR EACH ROW
            BEGIN
                UPDATE Impasti_Speciali 
                SET Updated_At = CURRENT_TIMESTAMP 
                WHERE ID_Impasto = NEW.ID_Impasto;
            END
        ''')
        print("   ✅ Trigger creato")
        
        # ==========================================
        # COMMIT
        # ==========================================
        conn.commit()
        print("✅ Migration completata con successo!")
        print()
        print("📊 Tabelle create:")
        print("   • Impasti_Speciali (gestione impasti)")
        print("   • Movimenti_Impasti (storico movimenti)")
        print()
        print("🚀 Prossimo step: Esegui popola_impasti.py per inserire dati iniziali")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ ERRORE durante migration: {e}")
        sys.exit(1)
    finally:
        conn.close()

def migration_down():
    """Rollback - rimuove tabelle (solo per sviluppo)"""
    print("⚠️  ROLLBACK: Rimozione tabelle impasti...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute('DROP TABLE IF EXISTS Movimenti_Impasti')
        cursor.execute('DROP TABLE IF EXISTS Impasti_Speciali')
        cursor.execute('DROP TRIGGER IF EXISTS update_impasti_timestamp')
        
        conn.commit()
        print("✅ Rollback completato")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ ERRORE durante rollback: {e}")
        sys.exit(1)
    finally:
        conn.close()

def verifica_db():
    """Verifica che il database esista"""
    import os
    if not os.path.exists(DB_PATH):
        print(f"❌ ERRORE: Database non trovato in {DB_PATH}")
        print("   Assicurati che il database esista prima di eseguire la migration")
        sys.exit(1)

if __name__ == '__main__':
    import sys
    
    verifica_db()
    
    if len(sys.argv) > 1 and sys.argv[1] == 'down':
        migration_down()
    else:
        migration_up()
