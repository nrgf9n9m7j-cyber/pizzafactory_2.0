#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Popola Bibite dal vecchio database
Importa tutte le bibite con sistema gestione scorte attivato
"""

import sqlite3
import os

DB_VECCHIO = 'data/pizzeria_OLD.db'
DB_NUOVO = 'data/pizzeria.db'

def popola_bibite():
    """Importa bibite dal vecchio database al nuovo con gestione scorte"""
    
    # Verifica esistenza database
    if not os.path.exists(DB_VECCHIO):
        print(f"❌ Database vecchio '{DB_VECCHIO}' non trovato!")
        return
    
    if not os.path.exists(DB_NUOVO):
        print(f"❌ Database nuovo '{DB_NUOVO}' non trovato!")
        return
    
    print("=" * 60)
    print("🍹 IMPORT BIBITE CON GESTIONE SCORTE")
    print("=" * 60)
    
    # Connetti a entrambi i database
    conn_vecchio = sqlite3.connect(DB_VECCHIO)
    conn_nuovo = sqlite3.connect(DB_NUOVO)
    
    cursor_vecchio = conn_vecchio.cursor()
    cursor_nuovo = conn_nuovo.cursor()
    
    try:
        # Verifica che la migration scorte sia stata eseguita
        check_cols = cursor_nuovo.execute("PRAGMA table_info(Prodotti)").fetchall()
        colonne = [col[1] for col in check_cols]
        
        if 'Gestione_Scorte' not in colonne:
            print("❌ Colonne gestione scorte non trovate!")
            print("   Esegui prima 'python3 migration_scorte.py'")
            return
        
        # Leggi bibite dal vecchio DB
        bibite = cursor_vecchio.execute("""
            SELECT 
                Nome_Bibita, Formato, Prezzo, Disponibile, Tipo
            FROM Bibite
            ORDER BY Tipo, Nome_Bibita
        """).fetchall()
        
        count_bibite = len(bibite)
        print(f"\n📊 Bibite trovate nel vecchio DB: {count_bibite}")
        
        # Verifica se ci sono già bibite nel nuovo DB
        count_esistenti = cursor_nuovo.execute("""
            SELECT COUNT(*) FROM Prodotti WHERE Formato = 'Bibita'
        """).fetchone()[0]
        
        if count_esistenti > 0:
            print(f"⚠️  Trovate {count_esistenti} bibite già presenti nel nuovo DB")
            risposta = input("   Vuoi sovrascrivere? (s/n): ")
            if risposta.lower() != 's':
                print("❌ Import annullato")
                return
            else:
                cursor_nuovo.execute("DELETE FROM Prodotti WHERE Formato = 'Bibita'")
                print("🗑️  Bibite esistenti rimosse")
        
        print("\n🔄 Import in corso...")
        
        # Mappa categorie (Tipo nel vecchio DB -> Categoria nel nuovo)
        categoria_map = {
            'Bibite': 'Bibite',
            'Acque': 'Acqua',
            'Birre': 'Birre'
        }
        
        # Soglie minime diverse per categoria
        soglie_map = {
            'Bibite': 10,  # 10 lattine minimo
            'Acqua': 15,   # 15 bottiglie minimo
            'Birre': 6     # 6 birre minimo
        }
        
        importate = 0
        
        for bibita in bibite:
            nome = bibita[0]
            formato = bibita[1] or ''
            prezzo = bibita[2]
            disponibile = bibita[3]
            tipo_vecchio = bibita[4]
            
            # Mappa categoria
            categoria = categoria_map.get(tipo_vecchio, 'Bibite')
            soglia = soglie_map.get(categoria, 10)
            
            # Crea nome completo
            nome_completo = f"{nome} {formato}".strip()
            
            # Inserisci nel nuovo DB come prodotto con scorte
            # Formato = 'Bibita' (tipo generale), Categoria = specifica (Bibite/Acqua/Birre)
            cursor_nuovo.execute("""
                INSERT INTO Prodotti (
                    Nome_Prodotto, Formato, Categoria,
                    Prezzo_Base, Disponibile,
                    Gestione_Scorte, Quantita_Disponibile, Soglia_Minima, Unita_Misura,
                    Preparazione_Minuti
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                nome_completo, 'Bibita', categoria,  # Formato='Bibita', Categoria=specifica
                prezzo, disponibile,
                1,  # Gestione_Scorte attiva
                0,  # Quantita_Disponibile (da caricare poi)
                soglia,  # Soglia_Minima
                'pz',  # Unita_Misura
                0  # Preparazione_Minuti (bibite = 0)
            ))
            
            importate += 1
            print(f"   ✅ {nome_completo:<35} €{prezzo:<5.2f} Cat:{categoria:<10} Soglia:{soglia}")
        
        conn_nuovo.commit()
        
        # Verifica finale
        count_finale = cursor_nuovo.execute("""
            SELECT COUNT(*) FROM Prodotti WHERE Formato = 'Bibita'
        """).fetchone()[0]
        
        print("\n" + "=" * 60)
        print("✅ IMPORT BIBITE COMPLETATO!")
        print("=" * 60)
        print(f"📊 Riepilogo:")
        print(f"   • Bibite vecchio DB:  {count_bibite}")
        print(f"   • Bibite importate:   {importate}")
        print(f"   • Totale nuovo DB:    {count_finale}")
        
        # Mostra distribuzione per categoria
        print("\n📊 Distribuzione per Categoria:")
        categorie = cursor_nuovo.execute("""
            SELECT Categoria, COUNT(*) as Totale, 
                   MIN(Soglia_Minima) as Soglia_Min,
                   MAX(Soglia_Minima) as Soglia_Max
            FROM Prodotti 
            WHERE Formato = 'Bibita'
            GROUP BY Categoria
            ORDER BY Totale DESC
        """).fetchall()
        
        for cat, tot, min_soglia, max_soglia in categorie:
            print(f"   • {cat:<10} {tot} bibite  (soglia minima: {min_soglia}-{max_soglia} pz)")
        
        print("\n💡 Note:")
        print("   • Tutte le bibite hanno Gestione_Scorte ATTIVA")
        print("   • Quantità iniziali = 0 (usa il form 'Carico Scorte' per caricare)")
        print("   • Soglie minime impostate per categoria (modificabili dal modal)")
        
    except Exception as e:
        conn_nuovo.rollback()
        print(f"\n❌ ERRORE durante l'import: {e}")
        raise
    
    finally:
        conn_vecchio.close()
        conn_nuovo.close()
    
    print("\n💡 Prossimo passo: Usa il form 'Carico Scorte' nell'app per caricare le quantità iniziali")

if __name__ == '__main__':
    popola_bibite()
