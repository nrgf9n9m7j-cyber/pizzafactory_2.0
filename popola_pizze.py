#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SETUP SEMPLIFICATO - Solo Pizze e Formati
PizzaFactory 2.0
"""

import sqlite3

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
# FORMATI DISPONIBILI (come menu separati, non moltiplicatori)
# ========================================
FORMATI = [
    "pizza",
    "pinsa", 
    "baby",
    "teglia",
    "maxi"
]

def popola_pizze():
    """Popola solo la tabella Prodotti con le pizze"""
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("🍕 Popolamento menu pizze...")
    
    # Conta pizze esistenti
    cursor.execute('SELECT COUNT(*) FROM Prodotti WHERE Formato = "pizza"')
    count_esistenti = cursor.fetchone()[0]
    
    if count_esistenti > 0:
        print(f"⚠️  Trovate {count_esistenti} pizze esistenti nel database")
        risposta = input("Vuoi sovrascrivere? (s/n): ")
        if risposta.lower() != 's':
            print("❌ Operazione annullata")
            conn.close()
            return
        
        # Elimina pizze esistenti
        cursor.execute('DELETE FROM Prodotti WHERE Formato = "pizza"')
        print("🗑️  Pizze esistenti eliminate")
    
    # Inserisci pizze
    for idx, pizza in enumerate(MENU_PIZZE, start=1):
        # Determina allergeni (tutte hanno glutine e latticini base)
        allergeni = "Glutine, Latticini"
        
        ingredienti_lower = pizza['ingredienti'].lower()
        if any(x in ingredienti_lower for x in ['pesce', 'tonno', 'salmone', 'acciughe']):
            allergeni += ", Pesce"
        if 'noci' in ingredienti_lower:
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
                Ingredienti, Allergeni, Disponibile, Preparazione_Minuti
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            pizza['nome'],
            'pizza',
            pizza['prezzo'],
            f"Pizza {pizza['nome']}",
            pizza['ingredienti'],
            allergeni,
            1,  # Disponibile
            5   # Tempo preparazione
        ))
    
    conn.commit()
    
    # Statistiche
    cursor.execute('SELECT COUNT(*) FROM Prodotti WHERE Formato = "pizza"')
    count = cursor.fetchone()[0]
    
    print(f"✅ {count} pizze inserite!")
    
    # Mostra prime 5 pizze
    print("\n📋 Prime 5 pizze inserite:")
    cursor.execute('SELECT Nome_Prodotto, Prezzo_Base FROM Prodotti WHERE Formato = "pizza" LIMIT 5')
    for nome, prezzo in cursor.fetchall():
        print(f"   • {nome}: €{prezzo:.2f}")
    
    # Pizze più costose
    print("\n💰 Pizze più costose:")
    cursor.execute('SELECT Nome_Prodotto, Prezzo_Base FROM Prodotti WHERE Formato = "pizza" ORDER BY Prezzo_Base DESC LIMIT 3')
    for nome, prezzo in cursor.fetchall():
        print(f"   • {nome}: €{prezzo:.2f}")
    
    conn.close()

def main():
    """Main function"""
    
    print("="*60)
    print("🍕 PIZZAFACTORY 2.0 - POPOLAMENTO MENU")
    print("="*60)
    print()
    
    try:
        popola_pizze()
        
        print("\n✅ MENU PRONTO!")
        print(f"📂 Database: {DB_PATH}")
        print()
        print("🚀 Prossimi step:")
        print("   1. Esegui: python popola_ingredienti.py")
        print("   2. Avvia Flask: python app.py")
        print("   3. Test: http://localhost:5000/api/prodotti?formato=pizza")
        print()
        
    except Exception as e:
        print(f"\n❌ ERRORE: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
