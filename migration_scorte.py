#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Migration: Aggiunge sistema gestione scorte
Esegui questo file per aggiornare il database con le nuove colonne
"""

import sqlite3
import os

DB_NAME = 'data/pizzeria.db'

def migration_scorte():
    """Aggiunge colonne per gestione scorte alla tabella Prodotti"""
    
    if not os.path.exists(DB_NAME):
        print(f"❌ Database {DB_NAME} non trovato!")
        print("   Assicurati di essere nella directory corretta")
        return
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    print("=" * 60)
    print("🔄 MIGRATION: Sistema Gestione Scorte")
    print("=" * 60)
    
    try:
        # 1. Aggiungi colonne alla tabella Prodotti
        print("\n📝 Aggiunta colonne alla tabella Prodotti...")
        
        alterazioni = [
            "ALTER TABLE Prodotti ADD COLUMN Gestione_Scorte INTEGER DEFAULT 0",
            "ALTER TABLE Prodotti ADD COLUMN Quantita_Disponibile INTEGER DEFAULT 0",
            "ALTER TABLE Prodotti ADD COLUMN Soglia_Minima INTEGER DEFAULT 5",
            "ALTER TABLE Prodotti ADD COLUMN Unita_Misura TEXT DEFAULT 'pz'",
            "ALTER TABLE Prodotti ADD COLUMN Quantita_Utilizzata INTEGER DEFAULT 0"
        ]
        
        for alter in alterazioni:
            try:
                cursor.execute(alter)
                colonna = alter.split("ADD COLUMN ")[1].split()[0]
                print(f"   ✅ Colonna '{colonna}' aggiunta")
            except sqlite3.OperationalError as e:
                if "duplicate column name" in str(e):
                    colonna = alter.split("ADD COLUMN ")[1].split()[0]
                    print(f"   ⚠️  Colonna '{colonna}' già esistente, skip")
                else:
                    raise
        
        # 2. Crea tabella Movimenti_Scorte
        print("\n📦 Creazione tabella Movimenti_Scorte...")
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Movimenti_Scorte (
                ID_Movimento INTEGER PRIMARY KEY AUTOINCREMENT,
                ID_Prodotto INTEGER NOT NULL,
                Tipo_Movimento TEXT NOT NULL, -- 'Carico', 'Scarico', 'Vendita', 'Inventario', 'Rettifica'
                Quantita INTEGER NOT NULL,
                Quantita_Precedente INTEGER,
                Quantita_Nuova INTEGER,
                Data_Movimento DATETIME DEFAULT CURRENT_TIMESTAMP,
                Note TEXT,
                Utente TEXT DEFAULT 'Sistema',
                FOREIGN KEY (ID_Prodotto) REFERENCES Prodotti(ID_Prodotto)
            )
        ''')
        print("   ✅ Tabella Movimenti_Scorte creata")
        
        # 3. Crea indici per performance
        print("\n⚡ Creazione indici...")
        
        indici = [
            "CREATE INDEX IF NOT EXISTS idx_prodotti_scorte ON Prodotti(Gestione_Scorte)",
            "CREATE INDEX IF NOT EXISTS idx_movimenti_prodotto ON Movimenti_Scorte(ID_Prodotto)",
            "CREATE INDEX IF NOT EXISTS idx_movimenti_data ON Movimenti_Scorte(Data_Movimento)"
        ]
        
        for idx in indici:
            cursor.execute(idx)
            nome_idx = idx.split("idx_")[1].split(" ")[0]
            print(f"   ✅ Indice 'idx_{nome_idx}' creato")
        
        conn.commit()
        
        print("\n" + "=" * 60)
        print("✅ MIGRATION COMPLETATA CON SUCCESSO!")
        print("=" * 60)
        
        # Verifica modifiche
        print("\n📊 Verifica struttura tabella Prodotti:")
        cols = cursor.execute("PRAGMA table_info(Prodotti)").fetchall()
        nuove_colonne = ['Gestione_Scorte', 'Quantita_Disponibile', 'Soglia_Minima', 'Unita_Misura', 'Quantita_Utilizzata']
        for col in cols:
            if col[1] in nuove_colonne:
                print(f"   ✅ {col[1]:<25} {col[2]:<15} DEFAULT {col[4]}")
        
        print("\n📊 Verifica tabella Movimenti_Scorte:")
        count = cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='Movimenti_Scorte'").fetchone()[0]
        if count > 0:
            print("   ✅ Tabella creata correttamente")
        
    except Exception as e:
        conn.rollback()
        print(f"\n❌ ERRORE durante la migration: {e}")
        raise
    
    finally:
        conn.close()
    
    print("\n💡 Prossimi passi:")
    print("   1. Esegui 'python3 import_clienti.py' per importare clienti dal vecchio DB")
    print("   2. Esegui 'python3 popola_bibite.py' per caricare le bibite")
    print("   3. Avvia l'applicazione e gestisci le scorte dalla dashboard")

if __name__ == '__main__':
    migration_scorte()
