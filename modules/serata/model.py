#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Model Serata"""

from core.database import get_db_connection
from core.exceptions import DatabaseError
from datetime import datetime
import json

class SerataModel:
    
    @staticmethod
    def get_corrente():
        """Recupera serata aperta"""
        conn = get_db_connection()
        try:
            serata = conn.execute('''
                SELECT * FROM Gestione_Serata 
                WHERE Stato = 'Aperta' 
                ORDER BY ID_Serata DESC LIMIT 1
            ''').fetchone()
            return dict(serata) if serata else {'aperta': False}
        finally:
            conn.close()
    
    @staticmethod
    def apri(data, data_serata=None, ora_apertura=None):
        """Apri nuova serata"""
        conn = get_db_connection()
        try:
            if not data_serata:
                data_serata = datetime.now().strftime('%Y-%m-%d')
            if not ora_apertura:
                ora_apertura = datetime.now().strftime('%H:%M:%S')
            
            # Chiudi serate aperte
            conn.execute("UPDATE Gestione_Serata SET Stato='Chiusa', Ora_Chiusura=CURRENT_TIME WHERE Stato='Aperta'")
            
            # Prepara rimanenze
            rimanenze = {
                'palline': {'iniziali': data.get('palline_iniziali', 0), 'finali': None, 'spreco': None},
                'impasti': [{'id': i.get('id'), 'nome': i.get('nome', ''), 'iniziali': i.get('quantita', 0), 'finali': None} for i in data.get('impasti', [])],
                'bufala': {'iniziali': 0, 'finali': None},
                'bibite': [{'id': b.get('id'), 'nome': b.get('nome', ''), 'iniziali': b.get('quantita', 0), 'finali': None} for b in data.get('bibite', [])]
            }
            
            cursor = conn.execute('''
                INSERT INTO Gestione_Serata (Data_Serata, Ora_Apertura, Stato, Note, Rimanenze_JSON, Palline_Iniziali)
                VALUES (?, ?, 'Aperta', ?, ?, ?)
            ''', (data_serata, ora_apertura, data.get('note', ''), json.dumps(rimanenze), data.get('palline_iniziali', 0)))
            
            serata_id = cursor.lastrowid
            
            # Impasti disponibilità
            for imp in data.get('impasti', []):
                conn.execute('''
                    INSERT INTO Disponibilita_Serata (ID_Serata, Tipo_Prodotto, ID_Prodotto, Quantita_Iniziale, Quantita_Utilizzata)
                    VALUES (?, 'impasto', ?, ?, 0)
                ''', (serata_id, imp['id'], imp.get('quantita', 0)))
                
                conn.execute('UPDATE Impasti_Speciali SET Quantita_Disponibile=?, Quantita_Utilizzata=0 WHERE ID_Impasto=?',
                           (imp.get('quantita', 0), imp['id']))
            
            # Bibite disponibilità
            for bib in data.get('bibite', []):
                conn.execute('''
                    INSERT INTO Disponibilita_Serata (ID_Serata, Tipo_Prodotto, ID_Prodotto, Quantita_Iniziale, Quantita_Utilizzata)
                    VALUES (?, 'bibita', ?, ?, 0)
                ''', (serata_id, bib['id'], bib.get('quantita', 0)))
            
            conn.commit()
            return serata_id
        except Exception as e:
            conn.rollback()
            raise DatabaseError(f"Errore apertura serata: {e}")
        finally:
            conn.close()
    
    @staticmethod
    def chiudi(serata_id, rimanenze_finali):
        """Chiudi serata con rimanenze"""
        conn = get_db_connection()
        try:
            # Recupera rimanenze iniziali
            serata = conn.execute('SELECT Rimanenze_JSON FROM Gestione_Serata WHERE ID_Serata=?', (serata_id,)).fetchone()
            if not serata:
                raise DatabaseError("Serata non trovata")
            
            rimanenze = json.loads(serata['Rimanenze_JSON'])
            
            # Aggiorna finali
            rimanenze['palline']['finali'] = rimanenze_finali.get('palline_finali', 0)
            rimanenze['palline']['spreco'] = rimanenze['palline']['iniziali'] - rimanenze['palline']['finali']
            
            conn.execute('''
                UPDATE Gestione_Serata 
                SET Stato='Chiusa', Ora_Chiusura=CURRENT_TIME, Rimanenze_JSON=?, Palline_Finali=?
                WHERE ID_Serata=?
            ''', (json.dumps(rimanenze), rimanenze_finali.get('palline_finali', 0), serata_id))
            
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise DatabaseError(f"Errore chiusura serata: {e}")
        finally:
            conn.close()
    
    @staticmethod
    def get_rimanenze_precedente():
        """Recupera rimanenze ultima serata chiusa"""
        conn = get_db_connection()
        try:
            serata = conn.execute('''
                SELECT Rimanenze_JSON, Data_Serata FROM Gestione_Serata 
                WHERE Stato='Chiusa' AND Rimanenze_JSON IS NOT NULL
                ORDER BY ID_Serata DESC LIMIT 1
            ''').fetchone()
            
            if serata and serata['Rimanenze_JSON']:
                return {'success': True, 'rimanenze': json.loads(serata['Rimanenze_JSON']), 'data_serata': serata['Data_Serata']}
            return {'success': False}
        finally:
            conn.close()
