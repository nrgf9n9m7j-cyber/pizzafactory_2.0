#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Import Clienti dal vecchio database
Importa tutti i clienti da pizzeria_OLD.db a pizzeria.db
"""

import sqlite3
import os
from datetime import datetime

DB_VECCHIO = 'data/pizzeria_OLD.db'
DB_NUOVO = 'data/pizzeria.db'

def import_clienti():
    """Importa clienti dal vecchio database al nuovo"""
    
    # Verifica esistenza database
    if not os.path.exists(DB_VECCHIO):
        print(f"❌ Database vecchio '{DB_VECCHIO}' non trovato!")
        print("   Assicurati che il file sia nella stessa directory")
        return
    
    if not os.path.exists(DB_NUOVO):
        print(f"❌ Database nuovo '{DB_NUOVO}' non trovato!")
        print("   Esegui prima 'python3 setup_database.py'")
        return
    
    print("=" * 60)
    print("📥 IMPORT CLIENTI DA VECCHIO DATABASE")
    print("=" * 60)
    
    # Connetti a entrambi i database
    conn_vecchio = sqlite3.connect(DB_VECCHIO)
    conn_nuovo = sqlite3.connect(DB_NUOVO)
    
    cursor_vecchio = conn_vecchio.cursor()
    cursor_nuovo = conn_nuovo.cursor()
    
    try:
        # Conta clienti nel vecchio DB
        count_vecchio = cursor_vecchio.execute("SELECT COUNT(*) FROM Clienti").fetchone()[0]
        print(f"\n📊 Clienti trovati nel vecchio DB: {count_vecchio}")
        
        # Conta clienti nel nuovo DB (per evitare duplicati)
        count_nuovo_prima = cursor_nuovo.execute("SELECT COUNT(*) FROM Clienti").fetchone()[0]
        print(f"📊 Clienti attuali nel nuovo DB: {count_nuovo_prima}")
        
        if count_nuovo_prima > 0:
            risposta = input("\n⚠️  Il nuovo database contiene già clienti. Vuoi sovrascrivere? (s/n): ")
            if risposta.lower() != 's':
                print("❌ Import annullato dall'utente")
                return
            else:
                # Svuota tabella clienti nel nuovo DB
                cursor_nuovo.execute("DELETE FROM Clienti")
                print("🗑️  Tabella Clienti svuotata")
        
        # Leggi tutti i clienti dal vecchio DB
        print("\n🔄 Import in corso...")
        clienti = cursor_vecchio.execute("""
            SELECT 
                Nome, Cognome, Telefono, Indirizzo, Civico, Citta,
                Note_Operatore, Totale_Ordini, Latitudine, Longitudine, Rating_Staff
            FROM Clienti
            ORDER BY ID_Cliente
        """).fetchall()
        
        importati = 0
        errori = 0
        
        for cliente in clienti:
            try:
                # Mappa i campi dal vecchio al nuovo schema
                nome = cliente[0] or ''
                cognome = cliente[1] or 'N/A'
                telefono = cliente[2] or ''
                indirizzo = cliente[3] or ''
                civico = cliente[4] or ''
                citta = cliente[5] or 'Chieri'
                note_vecchio = cliente[6] or ''
                totale_ordini = cliente[7] or 0
                latitudine = cliente[8]
                longitudine = cliente[9]
                rating_vecchio = cliente[10]
                
                # Mappa Rating_Staff (vecchio) -> Rating (nuovo)
                rating = rating_vecchio if rating_vecchio else None
                
                # Inserisci nel nuovo DB (schema semplificato)
                cursor_nuovo.execute("""
                    INSERT INTO Clienti (
                        Nome, Cognome, Telefono, Indirizzo, Civico, Citta,
                        Note, Rating, Totale_Ordini,
                        Latitudine, Longitudine
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    nome, cognome, telefono, indirizzo, civico, citta,
                    note_vecchio, rating, totale_ordini,
                    latitudine, longitudine
                ))
                
                importati += 1
                
                # Progress indicator ogni 5 clienti
                if importati % 5 == 0:
                    print(f"   ✅ Importati {importati}/{count_vecchio} clienti...")
            
            except Exception as e:
                errori += 1
                print(f"   ❌ Errore import cliente: {e}")
        
        conn_nuovo.commit()
        
        # Verifica finale
        count_nuovo_dopo = cursor_nuovo.execute("SELECT COUNT(*) FROM Clienti").fetchone()[0]
        
        print("\n" + "=" * 60)
        print("✅ IMPORT COMPLETATO!")
        print("=" * 60)
        print(f"📊 Riepilogo:")
        print(f"   • Clienti vecchio DB: {count_vecchio}")
        print(f"   • Clienti importati:  {importati}")
        print(f"   • Errori:             {errori}")
        print(f"   • Totale nuovo DB:    {count_nuovo_dopo}")
        
        # Mostra clienti con più ordini
        print("\n📊 Top 5 clienti per numero ordini:")
        top_clienti = cursor_nuovo.execute("""
            SELECT Nome, Cognome, Totale_Ordini
            FROM Clienti
            WHERE Totale_Ordini > 0
            ORDER BY Totale_Ordini DESC
            LIMIT 5
        """).fetchall()
        
        for nome, cognome, ordini in top_clienti:
            print(f"   • {nome} {cognome}: {ordini} ordini")
        
        # Mostra clienti con coordinate
        geocodificati = cursor_nuovo.execute("""
            SELECT COUNT(*) FROM Clienti 
            WHERE Latitudine IS NOT NULL AND Longitudine IS NOT NULL
        """).fetchone()[0]
        print(f"\n🗺️ Clienti geocodificati: {geocodificati}/{count_nuovo_dopo}")
        
    except Exception as e:
        conn_nuovo.rollback()
        print(f"\n❌ ERRORE durante l'import: {e}")
        raise
    
    finally:
        conn_vecchio.close()
        conn_nuovo.close()
    
    print("\n💡 Prossimo passo: Esegui 'python3 popola_bibite.py' per importare le bibite")

if __name__ == '__main__':
    import_clienti()
