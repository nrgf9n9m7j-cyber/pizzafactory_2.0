#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Popola i 4 prodotti FARINATA con prezzi fissi
PizzaFactory 2.0
"""

import sqlite3

DB_PATH = 'data/pizzeria.db'

# ========================================
# PRODOTTI FARINATA (PREZZI FISSI)
# ========================================
FARINATA = [
    {
        "nome": "Farinata Piccola",
        "prezzo": 4.00,
        "descrizione": "Farinata di ceci piccola (naturale)"
    },
    {
        "nome": "Farinata Piccola Farcita",
        "prezzo": 5.00,
        "descrizione": "Farinata di ceci piccola con farcitura"
    },
    {
        "nome": "Farinata Grande",
        "prezzo": 6.00,
        "descrizione": "Farinata di ceci grande (naturale)"
    },
    {
        "nome": "Farinata Grande Farcita",
        "prezzo": 7.00,
        "descrizione": "Farinata di ceci grande con farcitura"
    }
]

def popola_farinata():
    """Popola tabella Prodotti con farinata"""
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("🌾 Popolamento prodotti Farinata...")
    
    # Verifica se esistono già
    cursor.execute('SELECT COUNT(*) FROM Prodotti WHERE Formato = "farinata"')
    count_esistenti = cursor.fetchone()[0]
    
    if count_esistenti > 0:
        print(f"⚠️  Trovati {count_esistenti} prodotti farinata esistenti")
        risposta = input("Vuoi sovrascrivere? (s/n): ")
        if risposta.lower() != 's':
            print("❌ Operazione annullata")
            conn.close()
            return
        
        # Elimina farinata esistenti
        cursor.execute('DELETE FROM Prodotti WHERE Formato = "farinata"')
        print("🗑️  Prodotti farinata esistenti eliminati")
    
    # Inserisci farinata
    for idx, farinata in enumerate(FARINATA, start=1):
        cursor.execute('''
            INSERT INTO Prodotti (
                Nome_Prodotto, Formato, Prezzo_Base, Descrizione,
                Categoria, Allergeni, Disponibile, Preparazione_Minuti,
                Ordinamento, Gestione_Scorte
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            farinata['nome'],
            'farinata',
            farinata['prezzo'],
            farinata['descrizione'],
            'Farinata',
            'Glutine',  # Farinata di ceci contiene glutine per contaminazione
            1,  # Disponibile
            10,  # Tempo preparazione
            idx,  # Ordinamento
            0  # Non gestisce scorte (fatta al momento)
        ))
    
    conn.commit()
    
    # Statistiche
    cursor.execute('SELECT COUNT(*) FROM Prodotti WHERE Formato = "farinata"')
    count = cursor.fetchone()[0]
    
    print(f"✅ {count} prodotti farinata inseriti!")
    
    # Mostra prodotti inseriti
    print("\n📋 Prodotti Farinata:")
    cursor.execute('''
        SELECT Nome_Prodotto, Prezzo_Base 
        FROM Prodotti 
        WHERE Formato = "farinata" 
        ORDER BY Prezzo_Base
    ''')
    for nome, prezzo in cursor.fetchall():
        print(f"   • {nome}: €{prezzo:.2f}")
    
    conn.close()

def main():
    """Main function"""
    
    print("="*60)
    print("🌾 PIZZAFACTORY 2.0 - POPOLAMENTO FARINATA")
    print("="*60)
    print()
    
    try:
        popola_farinata()
        
        print("\n✅ FARINATA PRONTA!")
        print(f"📂 Database: {DB_PATH}")
        print()
        print("🚀 Prossimi step:")
        print("   1. Avvia Flask: python app.py")
        print("   2. Test: http://localhost:5000/api/prodotti?formato=farinata")
        print()
        
    except Exception as e:
        print(f"\n❌ ERRORE: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
