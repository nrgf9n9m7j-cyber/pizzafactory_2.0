#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Popola la tabella Ingredienti
Da eseguire DOPO setup_database.py
"""

import sqlite3

DB_NAME = 'data/pizzeria.db'

def popola_ingredienti():
    """Inserisce tutti gli ingredienti estratti dal menu pizze"""
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    print("📝 Popolamento tabella Ingredienti...")
    
    # Lista completa ingredienti con categoria e allergeni
    ingredienti = [
        # VERDURE
        ('Pomodoro', 'Verdure', 1.00, 1, None),
        ('Origano', 'Verdure', 1.00, 1, None),
        ('Olive Taggiasche', 'Verdure', 1.00, 1, None),
        ('Olive Nere', 'Verdure', 1.00, 1, None),
        ('Pomodori Confit', 'Verdure', 1.00, 1, None),
        ('Capperi', 'Verdure', 1.00, 1, None),
        ('Melanzane', 'Verdure', 1.00, 1, None),
        ('Zucchine', 'Verdure', 1.00, 1, None),
        ('Peperoni', 'Verdure', 1.00, 1, None),
        ('Radicchio', 'Verdure', 1.00, 1, None),
        ('Carciofi', 'Verdure', 1.00, 1, None),
        ('Cipolla Rossa', 'Verdure', 1.00, 1, None),
        ('Patate Lesse', 'Verdure', 1.00, 1, None),
        ('Friarielli', 'Verdure', 1.00, 1, None),
        ('Porro', 'Verdure', 1.00, 1, None),
        ('Rucola', 'Verdure', 1.00, 1, None),
        ('Pomodorini', 'Verdure', 1.00, 1, None),
        ('Pomodoro Giallo', 'Verdure', 1.00, 1, None),
        ('Pomodoro Secco', 'Verdure', 1.00, 1, None),
        ('Spinaci', 'Verdure', 1.00, 1, None),
        ('Avocado', 'Verdure', 1.00, 1, None),
        ('Funghi', 'Verdure', 1.00, 1, None),
        ('Basilico', 'Verdure', 1.00, 1, None),
        
        # LATTICINI
        ('Mozzarella', 'Latticini', 1.00, 1, 'Latticini'),
        ('Mozzarella di Bufala', 'Latticini', 1.00, 1, 'Latticini'),
        ('Gorgonzola', 'Latticini', 1.00, 1, 'Latticini'),
        ('Fontina', 'Latticini', 1.00, 1, 'Latticini'),
        ('Grana Padano', 'Latticini', 1.00, 1, 'Latticini'),
        ('Scamorza', 'Latticini', 1.00, 1, 'Latticini'),
        ('Scamorza Affumicata', 'Latticini', 1.00, 1, 'Latticini'),
        ('Brie', 'Latticini', 1.00, 1, 'Latticini'),
        ('Stracchino', 'Latticini', 1.00, 1, 'Latticini'),
        ('Formaggio Vegetale', 'Latticini', 1.00, 1, 'Soia'),
        ('Formaggio di Anacardi', 'Latticini', 1.00, 1, 'Frutta a guscio'),
        
        # SALUMI
        ('Prosciutto Cotto', 'Salumi', 1.00, 1, None),
        ('Prosciutto Crudo', 'Salumi', 1.00, 1, None),
        ('Salame', 'Salumi', 1.00, 1, None),
        ('Salame Piccante', 'Salumi', 1.00, 1, None),
        ('Salsiccia', 'Salumi', 1.00, 1, None),
        ('Wurstel', 'Salumi', 1.00, 1, None),
        ('Pancetta Coppata', 'Salumi', 1.00, 1, None),
        ('Speck', 'Salumi', 1.00, 1, None),
        ('Acciughe', 'Salumi', 1.00, 1, 'Pesce'),
        ('Tonno', 'Salumi', 1.00, 1, 'Pesce'),
        ('Salmone', 'Salumi', 1.00, 1, 'Pesce'),
        
        # CREME E CONDIMENTI
        ('Pesto', 'Creme', 1.00, 1, 'Frutta a guscio'),
        ('Pesto di Rucola', 'Creme', 1.00, 1, 'Frutta a guscio'),
        ('Crema di Zucchine', 'Creme', 1.00, 1, None),
        ('Olio al Basilico', 'Creme', 1.00, 1, None),
        
        # ALTRO
        ('Noci', 'Altro', 1.00, 1, 'Frutta a guscio'),
        ('Mopur', 'Altro', 1.00, 1, 'Soia'),
        ('Tofu alla Curcuma', 'Altro', 1.00, 1, 'Soia'),
        ('Pepe', 'Altro', 1.00, 1, None),
    ]
    
    # Inserisci ingredienti
    cursor.executemany('''
        INSERT INTO Ingredienti (Nome_Ingrediente, Categoria, Prezzo, Disponibile, Allergeni)
        VALUES (?, ?, ?, ?, ?)
    ''', ingredienti)
    
    conn.commit()
    
    # Conta ingredienti inseriti
    count = cursor.execute('SELECT COUNT(*) FROM Ingredienti').fetchone()[0]
    
    conn.close()
    
    print(f"✅ Inseriti {count} ingredienti nel database!")
    print("\n📊 Riepilogo per categoria:")
    
    # Mostra riepilogo
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    categorie = cursor.execute('''
        SELECT Categoria, COUNT(*) as Totale
        FROM Ingredienti
        GROUP BY Categoria
        ORDER BY Totale DESC
    ''').fetchall()
    
    for cat, tot in categorie:
        print(f"   • {cat}: {tot} ingredienti")
    
    conn.close()
    
    print("\n💡 Nota: Tutti gli ingredienti hanno prezzo base €1.00")
    print("   Puoi modificarli successivamente dall'interfaccia di gestione")

if __name__ == '__main__':
    popola_ingredienti()