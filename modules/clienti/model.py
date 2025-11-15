#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Model Clienti - solo interazione DB"""

from core.database import get_db_connection
from core.exceptions import DatabaseError, NotFoundError

class ClienteModel:
    
    @staticmethod
    def get_by_id(cliente_id):
        """Recupera cliente per ID"""
        conn = get_db_connection()
        try:
            cliente = conn.execute(
                'SELECT * FROM Clienti WHERE ID_Cliente = ?',
                (cliente_id,)
            ).fetchone()
            return dict(cliente) if cliente else None
        finally:
            conn.close()
    
    @staticmethod
    def cerca(query):
        """Cerca clienti per cognome o telefono"""
        conn = get_db_connection()
        try:
            clienti = conn.execute(
                'SELECT * FROM Clienti WHERE Cognome LIKE ? OR Telefono LIKE ?',
                (f'%{query}%', f'%{query}%')
            ).fetchall()
            return [dict(c) for c in clienti]
        finally:
            conn.close()
    
    @staticmethod
    def create(data):
        """Crea nuovo cliente"""
        conn = get_db_connection()
        try:
            cursor = conn.execute('''
                INSERT INTO Clienti (Nome, Cognome, Indirizzo, Civico, Citta, Telefono, Note_Operatore)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                data.get('nome'),
                data.get('cognome'),
                data.get('indirizzo'),
                data.get('civico'),
                data.get('citta', 'Chieri'),
                data.get('telefono'),
                data.get('note_operatore')
            ))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise DatabaseError(f"Errore creazione cliente: {e}")
        finally:
            conn.close()
    
    @staticmethod
    def update(cliente_id, data):
        """Aggiorna cliente"""
        conn = get_db_connection()
        try:
            conn.execute('''
                UPDATE Clienti 
                SET Nome=?, Cognome=?, Indirizzo=?, Civico=?, Citta=?, Telefono=?, Note_Operatore=?
                WHERE ID_Cliente=?
            ''', (
                data.get('nome'),
                data.get('cognome'),
                data.get('indirizzo'),
                data.get('civico'),
                data.get('citta'),
                data.get('telefono'),
                data.get('note_operatore'),
                cliente_id
            ))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise DatabaseError(f"Errore aggiornamento cliente: {e}")
        finally:
            conn.close()
    
    @staticmethod
    def update_rating(cliente_id, rating, note_staff):
        """Aggiorna rating e note staff"""
        conn = get_db_connection()
        try:
            conn.execute('''
                UPDATE Clienti SET Rating=?, Note_Staff=? WHERE ID_Cliente=?
            ''', (rating, note_staff, cliente_id))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise DatabaseError(f"Errore aggiornamento rating: {e}")
        finally:
            conn.close()
    
    @staticmethod
    def update_coordinates(cliente_id, lat, lon):
        """Aggiorna coordinate"""
        conn = get_db_connection()
        try:
            conn.execute('''
                UPDATE Clienti SET Latitudine=?, Longitudine=? WHERE ID_Cliente=?
            ''', (lat, lon, cliente_id))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise DatabaseError(f"Errore aggiornamento coordinate: {e}")
        finally:
            conn.close()
    
    @staticmethod
    def get_without_coordinates():
        """Recupera clienti senza coordinate"""
        conn = get_db_connection()
        try:
            clienti = conn.execute('''
                SELECT ID_Cliente, Indirizzo, Civico, Citta
                FROM Clienti
                WHERE (Latitudine IS NULL OR Longitudine IS NULL)
                AND Indirizzo IS NOT NULL AND Citta IS NOT NULL
            ''').fetchall()
            return [dict(c) for c in clienti]
        finally:
            conn.close()
    
    @staticmethod
    def get_with_stats():
        """Recupera clienti con statistiche ordini"""
        conn = get_db_connection()
        try:
            clienti = conn.execute('''
                SELECT 
                    c.*,
                    COUNT(DISTINCT o.ID_Ordine) as num_ordini,
                    MAX(o.Data_Ordine) as ultimo_ordine,
                    SUM(o.Totale_Ordine) as totale_speso
                FROM Clienti c
                LEFT JOIN Ordini o ON c.ID_Cliente = o.ID_Cliente
                GROUP BY c.ID_Cliente
            ''').fetchall()
            return [dict(c) for c in clienti]
        finally:
            conn.close()
