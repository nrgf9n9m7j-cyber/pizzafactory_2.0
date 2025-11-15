#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script per aggiornare categorie pizze - OPZIONE A
PizzaFactory 2.0
"""

import sqlite3
import os

DB_PATH = 'data/pizzeria.db'

# ========================================
# CATEGORIE PIZZE - OPZIONE A
# ========================================

# 🍅 ROSSE (con pomodoro/salsa rossa)
ROSSE = [
    'RIVIERA', 'MARGHERITA', 'PROSCIUTTO & FUNGHI', 'VEGETARIANA', 'CAPRICCIOSA',
    '4 FORMAGGI', 'CRUDO & BUFALA', 'SICILIANA', 'GIANNI', 'BOSCAIOLA',
    'GUSTOSA', '4 SALUMI', 'PANCETTA & CIPOLLA', 'SPECK & BRIE', 'GENOVESE',
    'VALE', 'VALDOSTANA', '2 POMODORI', 'PORRO SPECK & NOCI', 'ESTIVA',
    'ARES', 'PERSEO'
]

# 🧀 BIANCHE (senza pomodoro)
BIANCHE = [
    'ANTO', 'IVAAN', 'SALSICCIA & FRIARIELLI', 'STRACCHINO & RUCOLA',
    'FRESCA', 'SOLE', 'DEMETRA'
]

# 🌱 VEGETARIANE (senza carne)
VEGETARIANE = [
    'RIVIERA', 'MARGHERITA', 'VEGETARIANA', '4 FORMAGGI', 'ANTO',
    'VALDOSTANA', 'STRACCHINO & RUCOLA', 'FRESCA', 'SOLE', 'ESTIVA',
    'DEMETRA', 'ARES', 'PERSEO'
]

# ⭐ GOURMET (ingredienti speciali: bufala, speck, stracchino, salmone, formaggi speciali)
GOURMET = [
    'CRUDO & BUFALA', 'IVAAN', '2 POMODORI', 'PORRO SPECK & NOCI',
    'STRACCHINO & RUCOLA', 'SOLE', 'DEMETRA', 'SPECK & BRIE'
]


def main():
    """Aggiorna categorie pizze nel database"""
    
    # Verifica esistenza database
    if not os.path.exists(DB_PATH):
        print(f"❌ ERRORE: Database non trovato in {DB_PATH}")
        return
    
    print("=" * 60)
    print("🏷️  AGGIORNAMENTO CATEGORIE PIZZE - OPZIONE A")
    print("=" * 60)
    print()
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Conta pizze totali
        cursor.execute("SELECT COUNT(*) FROM Prodotti WHERE Formato = 'pizza'")
        totale = cursor.fetchone()[0]
        print(f"📊 Trovate {totale} pizze nel database\n")
        
        aggiornate = 0
        
        # Aggiorna ogni pizza con tutte le categorie applicabili
        # Per ora mettiamo la categoria PRINCIPALE
        
        print("🍅 Categorie ROSSE...")
        for nome in ROSSE:
            cursor.execute('''
                UPDATE Prodotti 
                SET Categoria = 'Rosse'
                WHERE Nome_Prodotto = ? AND Formato = 'pizza'
            ''', (nome,))
            if cursor.rowcount > 0:
                aggiornate += 1
                print(f"   ✅ {nome}")
        
        print("\n🧀 Categorie BIANCHE...")
        for nome in BIANCHE:
            cursor.execute('''
                UPDATE Prodotti 
                SET Categoria = 'Bianche'
                WHERE Nome_Prodotto = ? AND Formato = 'pizza'
            ''', (nome,))
            if cursor.rowcount > 0:
                aggiornate += 1
                print(f"   ✅ {nome}")
        
        # Nota: Vegetariane e Gourmet sono categorie SECONDARIE
        # Le pizze possono essere Rosse O Bianche + Vegetariane + Gourmet
        # Per ora assegniamo solo la categoria base (Rosse/Bianche)
        # Se una pizza è sia Bianca che Gourmet, rimarrà Bianca
        # Se è Rossa e Vegetariana, rimarrà Rossa
        
        # Se vuoi gestire multi-categoria, serve un campo separato nel DB
        
        conn.commit()
        conn.close()
        
        print()
        print("=" * 60)
        print(f"✅ COMPLETATO! Aggiornate {aggiornate} pizze")
        print("=" * 60)
        print()
        print("📝 NOTE:")
        print("   • Rosse: pizze con pomodoro/salsa rossa")
        print("   • Bianche: pizze senza pomodoro")
        print("   • Le categorie Vegetariane e Gourmet sono trasversali")
        print("   • Per filtrare Vegetariane/Gourmet, serve logica JS")
        print()
        print("🧪 Verifica con:")
        print("   SELECT Nome_Prodotto, Categoria FROM Prodotti WHERE Formato = 'pizza';")
        print()
        
    except sqlite3.Error as e:
        print(f"❌ ERRORE DATABASE: {e}")
    except Exception as e:
        print(f"❌ ERRORE: {e}")

if __name__ == '__main__':
    main()
