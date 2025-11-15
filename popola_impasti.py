#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
POPOLAMENTO: Impasti Speciali Predefiniti
Inserisce i 7 impasti standard con sovrapprezzo €2.00
"""

import sqlite3
import sys

DB_PATH = 'data/pizzeria.db'

# ==========================================
# IMPASTI PREDEFINITI
# ==========================================
IMPASTI_DEFAULT = [
    {
        'nome': 'Pinsa',
        'sovrapprezzo': 2.00,
        'note': 'Impasto pinsa romana - alta idratazione'
    },
    {
        'nome': 'Farro',
        'sovrapprezzo': 2.00,
        'note': 'Impasto con farina di farro integrale'
    },
    {
        'nome': 'Integrale',
        'sovrapprezzo': 2.00,
        'note': 'Impasto con farina integrale 100%'
    },
    {
        'nome': 'Mais',
        'sovrapprezzo': 2.00,
        'note': 'Impasto con farina di mais'
    },
    {
        'nome': 'Segale',
        'sovrapprezzo': 2.00,
        'note': 'Impasto con farina di segale'
    },
    {
        'nome': 'Basilico',
        'sovrapprezzo': 2.00,
        'note': 'Impasto aromatizzato al basilico'
    },
    {
        'nome': 'Curcuma & Semi',
        'sovrapprezzo': 2.00,
        'note': 'Impasto con curcuma e mix di semi'
    }
]

def popola_impasti():
    """Inserisce impasti predefiniti nel database"""
    print("🌾 POPOLAMENTO: Inserimento impasti speciali...")
    print()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Verifica che la tabella esista
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Impasti_Speciali'")
        if not cursor.fetchone():
            print("❌ ERRORE: Tabella Impasti_Speciali non trovata!")
            print("   Esegui prima: python migration_impasti_speciali.py")
            sys.exit(1)
        
        inseriti = 0
        skippati = 0
        
        for impasto in IMPASTI_DEFAULT:
            # Verifica se esiste già
            cursor.execute('SELECT ID_Impasto FROM Impasti_Speciali WHERE Nome = ?', (impasto['nome'],))
            if cursor.fetchone():
                print(f"⏭️  {impasto['nome']:<20} → già presente, skip")
                skippati += 1
                continue
            
            # Inserisci nuovo impasto
            cursor.execute('''
                INSERT INTO Impasti_Speciali (Nome, Sovrapprezzo, Quantita_Disponibile, Soglia_Minima, Note)
                VALUES (?, ?, 0, 0, ?)
            ''', (impasto['nome'], impasto['sovrapprezzo'], impasto['note']))
            
            print(f"✅ {impasto['nome']:<20} → +{impasto['sovrapprezzo']:.2f}€")
            inseriti += 1
        
        conn.commit()
        
        print()
        print("=" * 60)
        print(f"📊 RIEPILOGO:")
        print(f"   • Impasti inseriti: {inseriti}")
        print(f"   • Impasti skippati: {skippati}")
        print(f"   • Totale impasti:   {inseriti + skippati}")
        print("=" * 60)
        print()
        
        if inseriti > 0:
            print("✅ Popolamento completato con successo!")
            print()
            print("🚀 Prossimi step:")
            print("   1. Aggiungi endpoint API in app.py")
            print("   2. Crea modal carico impasti")
            print("   3. Integra in hamburger menu")
        else:
            print("ℹ️  Nessun nuovo impasto inserito (tutti già presenti)")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ ERRORE durante popolamento: {e}")
        sys.exit(1)
    finally:
        conn.close()

def mostra_impasti():
    """Mostra impasti presenti nel database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT Nome, Sovrapprezzo, Quantita_Disponibile, Soglia_Minima, Attivo
            FROM Impasti_Speciali
            ORDER BY Nome
        ''')
        
        impasti = cursor.fetchall()
        
        if not impasti:
            print("ℹ️  Nessun impasto trovato nel database")
            return
        
        print()
        print("=" * 80)
        print("📋 IMPASTI PRESENTI NEL DATABASE:")
        print("=" * 80)
        print(f"{'Nome':<20} {'Sovrapprezzo':>12} {'Disponibili':>12} {'Soglia':>8} {'Attivo':>8}")
        print("-" * 80)
        
        for nome, sovrapprezzo, qty, soglia, attivo in impasti:
            stato = "✅" if attivo else "❌"
            print(f"{nome:<20} {sovrapprezzo:>11.2f}€ {qty:>12} {soglia:>8} {stato:>8}")
        
        print("=" * 80)
        print()
        
    except Exception as e:
        print(f"❌ ERRORE: {e}")
    finally:
        conn.close()

def verifica_db():
    """Verifica che il database esista"""
    import os
    if not os.path.exists(DB_PATH):
        print(f"❌ ERRORE: Database non trovato in {DB_PATH}")
        sys.exit(1)

if __name__ == '__main__':
    import sys
    
    verifica_db()
    
    if len(sys.argv) > 1 and sys.argv[1] == 'list':
        mostra_impasti()
    else:
        popola_impasti()
        print()
        mostra_impasti()
