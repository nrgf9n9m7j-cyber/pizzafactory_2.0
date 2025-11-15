#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Model Pagamenti"""

from core.database import get_db_connection
from core.exceptions import DatabaseError
import json

class PagamentoModel:
    
    @staticmethod
    def registra_parziale(ordine_id, importo, prodotti_ids, note=''):
        """Registra pagamento parziale"""
        conn = get_db_connection()
        try:
            # Inserisci pagamento
            cursor = conn.execute('''
                INSERT INTO Pagamenti_Parziali (ID_Ordine, Importo, Prodotti_Pagati, Note)
                VALUES (?, ?, ?, ?)
            ''', (ordine_id, importo, json.dumps(prodotti_ids), note))
            
            # Segna prodotti pagati
            if prodotti_ids:
                placeholders = ','.join(['?' for _ in prodotti_ids])
                conn.execute(f'UPDATE Dettagli_Ordine SET Pagato=1 WHERE ID_Dettaglio IN ({placeholders})', prodotti_ids)
            
            # Aggiorna totale pagato
            conn.execute('UPDATE Ordini SET Totale_Pagato = Totale_Pagato + ? WHERE ID_Ordine = ?', (importo, ordine_id))
            
            # Aggiorna stato
            totale, pagato = conn.execute('SELECT Totale_Ordine, Totale_Pagato FROM Ordini WHERE ID_Ordine=?', (ordine_id,)).fetchone()
            
            if pagato >= totale:
                stato = 'Completato'
            elif pagato > 0:
                stato = 'Parziale'
            else:
                stato = 'Non Pagato'
            
            conn.execute('UPDATE Ordini SET Stato_Pagamento=?, Pagato=? WHERE ID_Ordine=?',
                       (stato, 1 if stato == 'Completato' else 0, ordine_id))
            
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise DatabaseError(f"Errore pagamento: {e}")
        finally:
            conn.close()
    
    @staticmethod
    def get_storico(ordine_id):
        """Storico pagamenti ordine"""
        conn = get_db_connection()
        try:
            rows = conn.execute('''
                SELECT ID_Pagamento, Data_Pagamento, Ora_Pagamento, Importo, Prodotti_Pagati, Note
                FROM Pagamenti_Parziali
                WHERE ID_Ordine=?
                ORDER BY Data_Pagamento, Ora_Pagamento
            ''', (ordine_id,)).fetchall()
            
            return [{
                'id': r[0],
                'data': r[1],
                'ora': r[2],
                'importo': r[3],
                'prodotti_ids': json.loads(r[4]) if r[4] else [],
                'note': r[5]
            } for r in rows]
        finally:
            conn.close()
    
    @staticmethod
    def get_prodotti_ordine(ordine_id):
        """Prodotti ordine con stato pagamento"""
        conn = get_db_connection()
        try:
            rows = conn.execute('''
                SELECT 
                    d.ID_Dettaglio,
                    CASE 
                        WHEN d.ID_Prodotto IS NOT NULL THEN p.Nome_Prodotto
                        WHEN d.ID_Bibita IS NOT NULL THEN b.Nome_Bibita
                        ELSE 'Prodotto Sconosciuto'
                    END as Nome,
                    d.Quantita,
                    d.Prezzo_Unitario,
                    (d.Quantita * d.Prezzo_Unitario) as Totale,
                    d.Note_Prodotto,
                    d.Pagato
                FROM Dettagli_Ordine d
                LEFT JOIN Prodotti p ON d.ID_Prodotto = p.ID_Prodotto
                LEFT JOIN Bibite b ON d.ID_Bibita = b.ID_Bibita
                WHERE d.ID_Ordine=?
                AND (d.ID_Prodotto IS NOT NULL OR d.ID_Bibita IS NOT NULL)
                ORDER BY d.ID_Dettaglio
            ''', (ordine_id,)).fetchall()
            
            return [{
                'id_dettaglio': r[0],
                'nome': r[1],
                'quantita': r[2],
                'prezzo_unitario': r[3],
                'totale': r[4],
                'note': r[5],
                'pagato': r[6] == 1
            } for r in rows]
        finally:
            conn.close()
