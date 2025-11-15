#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Model Dashboard"""

from core.database import get_db_connection
from datetime import datetime

class DashboardModel:
    
    @staticmethod
    def get_statistiche_serata():
        """Statistiche serata corrente"""
        conn = get_db_connection()
        try:
            oggi = datetime.now().strftime('%Y-%m-%d')
            
            # Totali
            totali = conn.execute('''
                SELECT 
                    COUNT(*) as num_ordini,
                    COALESCE(SUM(Totale_Ordine), 0) as totale_incasso,
                    COALESCE(SUM(CASE WHEN Pagato=1 THEN Totale_Ordine ELSE 0 END), 0) as totale_pagato
                FROM Ordini WHERE Data_Ordine=?
            ''', (oggi,)).fetchone()
            
            # Per tipo
            per_tipo = conn.execute('''
                SELECT t.Descrizione, COUNT(*) as num
                FROM Ordini o
                JOIN Tipi_Ordine t ON o.ID_Tipo = t.ID_Tipo
                WHERE o.Data_Ordine=?
                GROUP BY o.ID_Tipo, t.Descrizione
            ''', (oggi,)).fetchall()
            
            # Per ora
            per_ora = conn.execute('''
                SELECT strftime('%H:00', Ora_Ordine) as ora, COUNT(*) as num
                FROM Ordini
                WHERE Data_Ordine=?
                GROUP BY strftime('%H', Ora_Ordine)
                ORDER BY ora
            ''', (oggi,)).fetchall()
            
            return {
                'num_ordini': totali[0],
                'totale_incasso': totali[1],
                'totale_pagato': totali[2],
                'da_incassare': totali[1] - totali[2],
                'ordini_per_tipo': [{'tipo': r[0], 'count': r[1]} for r in per_tipo],
                'ordini_per_ora': [{'ora': r[0], 'count': r[1]} for r in per_ora]
            }
        finally:
            conn.close()
    
    @staticmethod
    def get_top_prodotti(limite=5):
        """Top prodotti venduti"""
        conn = get_db_connection()
        try:
            oggi = datetime.now().strftime('%Y-%m-%d')
            
            rows = conn.execute('''
                SELECT 
                    COALESCE(p.Nome_Prodotto, b.Nome_Bibita) as nome,
                    SUM(d.Quantita) as totale_venduto,
                    SUM(d.Quantita * d.Prezzo_Unitario) as incasso
                FROM Dettagli_Ordine d
                JOIN Ordini o ON d.ID_Ordine = o.ID_Ordine
                LEFT JOIN Prodotti p ON d.ID_Prodotto = p.ID_Prodotto
                LEFT JOIN Bibite b ON d.ID_Bibita = b.ID_Bibita
                WHERE o.Data_Ordine=? AND (d.ID_Prodotto IS NOT NULL OR d.ID_Bibita IS NOT NULL)
                GROUP BY nome
                ORDER BY totale_venduto DESC
                LIMIT ?
            ''', (oggi, limite)).fetchall()
            
            return [{'nome': r[0], 'venduto': r[1], 'incasso': r[2]} for r in rows]
        finally:
            conn.close()
