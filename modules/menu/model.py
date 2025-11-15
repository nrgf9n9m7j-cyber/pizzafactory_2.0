#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Model Menu/Prodotti - solo interazione DB"""

from core.database import get_db_connection
from core.exceptions import DatabaseError

class MenuModel:
    
    @staticmethod
    def get_prodotti(formato=None, disponibili_only=True):
        """Recupera prodotti"""
        conn = get_db_connection()
        try:
            query = 'SELECT * FROM Prodotti'
            params = []
            
            conditions = []
            if disponibili_only:
                conditions.append('Disponibile = 1')
            if formato:
                conditions.append('Formato = ?')
                params.append(formato)
            
            if conditions:
                query += ' WHERE ' + ' AND '.join(conditions)
            
            query += ' ORDER BY Formato, Nome_Prodotto'
            
            prodotti = conn.execute(query, params).fetchall()
            return [dict(p) for p in prodotti]
        finally:
            conn.close()
    
    @staticmethod
    def get_prodotto_by_id(prodotto_id):
        """Recupera prodotto per ID"""
        conn = get_db_connection()
        try:
            prodotto = conn.execute(
                'SELECT * FROM Prodotti WHERE ID_Prodotto = ?',
                (prodotto_id,)
            ).fetchone()
            return dict(prodotto) if prodotto else None
        finally:
            conn.close()
    
    @staticmethod
    def create_prodotto(data):
        """Crea nuovo prodotto"""
        conn = get_db_connection()
        try:
            cursor = conn.execute('''
                INSERT INTO Prodotti 
                (Nome_Prodotto, Formato, Descrizione, Prezzo_Base, Disponibile, Preparazione_Minuti, Allergeni)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                data.get('nome'),
                data.get('formato', 'pizza'),
                data.get('descrizione', ''),
                data.get('prezzo', 0.0),
                data.get('disponibile', 1),
                data.get('preparazione_minuti', 15),
                data.get('allergeni', '')
            ))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise DatabaseError(f"Errore creazione prodotto: {e}")
        finally:
            conn.close()
    
    @staticmethod
    def update_prodotto(prodotto_id, data):
        """Aggiorna prodotto"""
        conn = get_db_connection()
        try:
            conn.execute('''
                UPDATE Prodotti
                SET Nome_Prodotto=?, Formato=?, Descrizione=?, Prezzo_Base=?,
                    Disponibile=?, Preparazione_Minuti=?, Allergeni=?
                WHERE ID_Prodotto=?
            ''', (
                data.get('nome'),
                data.get('formato'),
                data.get('descrizione', ''),
                data.get('prezzo'),
                data.get('disponibile', 1),
                data.get('preparazione_minuti', 15),
                data.get('allergeni', ''),
                prodotto_id
            ))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise DatabaseError(f"Errore aggiornamento prodotto: {e}")
        finally:
            conn.close()
    
    @staticmethod
    def soft_delete_prodotto(prodotto_id):
        """Disabilita prodotto (soft delete)"""
        conn = get_db_connection()
        try:
            conn.execute('UPDATE Prodotti SET Disponibile = 0 WHERE ID_Prodotto = ?', (prodotto_id,))
            conn.commit()
        finally:
            conn.close()
    
    @staticmethod
    def get_ingredienti():
        """Recupera ingredienti disponibili"""
        conn = get_db_connection()
        try:
            ingredienti = conn.execute(
                'SELECT * FROM Ingredienti WHERE Disponibile = 1 ORDER BY Categoria, Nome_Ingrediente'
            ).fetchall()
            return [dict(i) for i in ingredienti]
        finally:
            conn.close()
    
    @staticmethod
    def get_impasti():
        """Recupera impasti speciali disponibili"""
        conn = get_db_connection()
        try:
            impasti = conn.execute(
                'SELECT * FROM Impasti_Speciali WHERE Disponibile = 1'
            ).fetchall()
            return [dict(i) for i in impasti]
        finally:
            conn.close()
    
    @staticmethod
    def get_opzioni():
        """Recupera opzioni preparazione attive"""
        conn = get_db_connection()
        try:
            opzioni = conn.execute(
                'SELECT * FROM Opzioni_Preparazione WHERE Attivo = 1 ORDER BY Categoria'
            ).fetchall()
            return [dict(o) for o in opzioni]
        finally:
            conn.close()
    
    @staticmethod
    def get_bibite():
        """Recupera bibite disponibili"""
        conn = get_db_connection()
        try:
            bibite = conn.execute(
                'SELECT * FROM Bibite WHERE Disponibile = 1 ORDER BY Tipo, Nome_Bibita'
            ).fetchall()
            return [dict(b) for b in bibite]
        finally:
            conn.close()
    
    @staticmethod
    def get_metodi_pagamento():
        """Recupera metodi pagamento attivi"""
        conn = get_db_connection()
        try:
            metodi = conn.execute(
                'SELECT * FROM Metodi_Pagamento WHERE Attivo = 1'
            ).fetchall()
            return [dict(m) for m in metodi]
        finally:
            conn.close()
    
    @staticmethod
    def get_tipi_ordine():
        """Recupera tipi ordine"""
        conn = get_db_connection()
        try:
            tipi = conn.execute('SELECT * FROM Tipi_Ordine').fetchall()
            return [dict(t) for t in tipi]
        finally:
            conn.close()
