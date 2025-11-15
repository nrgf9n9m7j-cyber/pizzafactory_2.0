#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Routes Scorte - Gestione magazzino"""

from flask import Blueprint, request, jsonify, render_template
from core.database import get_db_connection
from datetime import datetime

scorte_bp = Blueprint('scorte', __name__)

@scorte_bp.route('/carico-scorte')
def carico_scorte_page():
    """Pagina carico scorte"""
    return render_template('pages/carico_scorte.html')

@scorte_bp.route('/api/prodotti/bibite')
def get_bibite():
    """Restituisce tutte le bibite disponibili"""
    conn = get_db_connection()
    bibite = conn.execute('''
        SELECT * FROM Prodotti 
        WHERE Formato = 'Bibita' AND Disponibile = 1
        ORDER BY Categoria, Nome_Prodotto
    ''').fetchall()
    conn.close()
    return jsonify([dict(b) for b in bibite])

@scorte_bp.route('/api/prodotti/con-scorte')
def get_prodotti_con_scorte():
    """Restituisce prodotti con gestione scorte attiva"""
    conn = get_db_connection()
    prodotti = conn.execute('''
        SELECT * FROM Prodotti 
        WHERE Gestione_Scorte = 1
        ORDER BY Categoria, Nome_Prodotto
    ''').fetchall()
    conn.close()
    return jsonify([dict(p) for p in prodotti])

@scorte_bp.route('/api/prodotti/aggiorna-soglie', methods=['POST'])
def aggiorna_soglie():
    """Aggiorna soglie minime prodotti"""
    data = request.json
    modifiche = data.get('modifiche', [])
    
    conn = get_db_connection()
    aggiornati = 0
    
    for mod in modifiche:
        id_prodotto = mod['ID_Prodotto']
        updates = []
        params = []
        
        if 'Soglia_Minima' in mod:
            updates.append('Soglia_Minima = ?')
            params.append(mod['Soglia_Minima'])
        
        if 'Unita_Misura' in mod:
            updates.append('Unita_Misura = ?')
            params.append(mod['Unita_Misura'])
        
        if updates:
            query = f"UPDATE Prodotti SET {', '.join(updates)} WHERE ID_Prodotto = ?"
            params.append(id_prodotto)
            conn.execute(query, params)
            aggiornati += 1
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'aggiornati': aggiornati})

@scorte_bp.route('/api/scorte/carico', methods=['POST'])
def carico_scorte():
    """Registra carico scorte - CON DEBUG LOGGING"""
    print("\n" + "="*60)
    print(">>> INIZIO DEBUG CARICO SCORTE <<<")
    print("="*60)
    
    try:
        data = request.json
        movimenti = data.get('movimenti', [])
        
        print(f"[DEBUG] Timestamp: {datetime.now()}")
        print(f"[DEBUG] Movimenti ricevuti: {len(movimenti)}")
        print(f"[DEBUG] Dati completi JSON: {data}")
        print("="*60)
        
        conn = get_db_connection()
        aggiornati = 0
        
        for idx, mov in enumerate(movimenti, 1):
            id_prodotto = mov.get('ID_Prodotto')
            quantita = mov.get('Quantita')
            note = mov.get('Note', '')
            
            print(f"\n--- MOVIMENTO {idx}/{len(movimenti)} ---")
            print(f"ID Prodotto: {id_prodotto}")
            print(f"Quantita da aggiungere: {quantita}")
            print(f"Note: '{note}'")
            
            if not id_prodotto or not quantita:
                print(f"[WARNING] SKIP: Dati mancanti (ID={id_prodotto}, Qta={quantita})")
                continue
            
            # Leggi quantita attuale
            print(f"[QUERY] SELECT Nome_Prodotto, Quantita_Disponibile FROM Prodotti WHERE ID_Prodotto = {id_prodotto}")
            result = conn.execute(
                'SELECT Nome_Prodotto, Quantita_Disponibile FROM Prodotti WHERE ID_Prodotto = ?',
                (id_prodotto,)
            ).fetchone()
            
            if not result:
                print(f"[ERROR] Prodotto {id_prodotto} NON TROVATO nel database!")
                continue
            
            nome_prodotto = result[0]
            qta_attuale = result[1] if result[1] is not None else 0
            
            print(f"[RESULT] Prodotto: {nome_prodotto}")
            print(f"[RESULT] Quantita attuale: {qta_attuale}")
            
            # Calcola nuova quantita
            qta_nuova = qta_attuale + quantita
            print(f"[CALC] Nuova quantita: {qta_attuale} + {quantita} = {qta_nuova}")
            
            # Aggiorna prodotto
            print(f"[UPDATE] UPDATE Prodotti SET Quantita_Disponibile = {qta_nuova} WHERE ID_Prodotto = {id_prodotto}")
            conn.execute('''
                UPDATE Prodotti 
                SET Quantita_Disponibile = ? 
                WHERE ID_Prodotto = ?
            ''', (qta_nuova, id_prodotto))
            
            print(f"[SUCCESS] UPDATE eseguito!")
            
            # Registra movimento
            print(f"[INSERT] Registro movimento in Movimenti_Scorte...")
            conn.execute('''
                INSERT INTO Movimenti_Scorte 
                (ID_Prodotto, Tipo_Movimento, Quantita, Quantita_Precedente, Quantita_Nuova, Note, Data_Movimento)
                VALUES (?, 'Carico', ?, ?, ?, ?, ?)
            ''', (id_prodotto, quantita, qta_attuale, qta_nuova, note, datetime.now()))
            
            print(f"[SUCCESS] Movimento registrato!")
            
            aggiornati += 1
        
        print(f"\n[COMMIT] Eseguo COMMIT del database...")
        conn.commit()
        print(f"[SUCCESS] COMMIT eseguito con successo!")
        print(f"[SUMMARY] Totale prodotti aggiornati: {aggiornati}/{len(movimenti)}")
        
        conn.close()
        
        print("="*60)
        print(">>> FINE DEBUG CARICO SCORTE <<<")
        print("="*60 + "\n")
        
        return jsonify({
            'success': True, 
            'movimenti': aggiornati,
            'ricevuti': len(movimenti)
        }), 201
    
    except Exception as e:
        print("\n" + "!"*60)
        print(">>> ERRORE GRAVE <<<")
        print("!"*60)
        print(f"Tipo errore: {type(e).__name__}")
        print(f"Messaggio: {str(e)}")
        print("\nStack trace completo:")
        import traceback
        traceback.print_exc()
        print("!"*60 + "\n")
        return jsonify({'error': str(e)}), 500

@scorte_bp.route('/api/prodotti/scorte-basse')
def get_scorte_basse():
    """Restituisce prodotti con scorte sotto soglia"""
    conn = get_db_connection()
    prodotti = conn.execute('''
        SELECT * FROM Prodotti 
        WHERE Gestione_Scorte = 1 
        AND Quantita_Disponibile <= Soglia_Minima
        ORDER BY Quantita_Disponibile ASC
    ''').fetchall()
    conn.close()
    return jsonify([dict(p) for p in prodotti])
