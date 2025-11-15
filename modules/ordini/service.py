#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Service Ordini - logica business"""

from datetime import datetime
from .model import OrdineModel
from .calcoli import genera_codice_ordine, calcola_prezzo_con_formato
from core.exceptions import ValidationError, NotFoundError, DatabaseError

class OrdineService:
    
    @staticmethod
    def crea_ordine(data):
        """Crea ordine completo con codice univoco"""
        # Genera codice
        data_ordine = datetime.now().strftime('%Y-%m-%d')
        codice_ordine, _ = genera_codice_ordine(data_ordine)
        
        # Verifica unicità codice
        codice_ordine = OrdineService._verifica_unicita_codice(codice_ordine)
        
        # Crea ordine
        ordine_id = OrdineModel.create(data, codice_ordine)
        
        # Inserisci prodotti (pizze E bibite, tutto uguale)
        for prodotto in data.get('prodotti', []):
            dettaglio_id = OrdineModel.insert_dettaglio_prodotto(ordine_id, prodotto)
            
            # Solo le pizze hanno extra ingredienti e opzioni
            # Le bibite hanno solo id_prodotto e quantità
            if dettaglio_id and prodotto.get('extra_ingredienti'):
                # Extra ingredienti
                for extra in prodotto.get('extra_ingredienti', []):
                    OrdineModel.insert_extra_ingrediente(dettaglio_id, extra)
            
            if dettaglio_id and prodotto.get('opzioni'):
                # Opzioni
                for opzione_id in prodotto.get('opzioni', []):
                    if opzione_id:
                        OrdineModel.insert_opzione(dettaglio_id, opzione_id)
        
        # Aggiorna statistiche cliente
        if data.get('id_cliente'):
            OrdineModel.update_statistiche_cliente(data['id_cliente'])
        
        return {
            'success': True,
            'id': ordine_id,
            'codice_ordine': codice_ordine,
            'totale_finale': data.get('totale_finale')
        }
    
    @staticmethod
    def aggiorna_ordine(ordine_id, data):
        """Aggiorna ordine esistente"""
        # Verifica esistenza
        ordine = OrdineModel.get_by_id(ordine_id)
        if not ordine:
            raise NotFoundError(f"Ordine {ordine_id} non trovato")
        
        # Aggiorna dati principali
        OrdineModel.update(ordine_id, data)
        
        # Elimina dettagli vecchi
        OrdineModel.delete_dettagli(ordine_id)
        
        # Inserisci nuovi dettagli
        for prodotto in data.get('prodotti', []):
            dettaglio_id = OrdineModel.insert_dettaglio_prodotto(ordine_id, prodotto)
            
            if dettaglio_id and prodotto.get('extra_ingredienti'):
                for extra in prodotto.get('extra_ingredienti', []):
                    OrdineModel.insert_extra_ingrediente(dettaglio_id, extra)
            
            if dettaglio_id and prodotto.get('opzioni'):
                for opzione_id in prodotto.get('opzioni', []):
                    if opzione_id:
                        OrdineModel.insert_opzione(dettaglio_id, opzione_id)
        
        return {
            'success': True,
            'id': ordine_id,
            'totale_finale': data.get('totale_finale')
        }
    
    @staticmethod
    def _verifica_unicita_codice(codice_ordine):
        """Verifica e corregge codice se duplicato"""
        from core.database import get_db_connection
        
        conn = get_db_connection()
        try:
            esistente = conn.execute(
                'SELECT ID_Ordine FROM Ordini WHERE Codice_Ordine = ?',
                (codice_ordine,)
            ).fetchone()
            
            if esistente:
                # Incrementa progressivo
                parts = codice_ordine.split('PF')
                base = parts[0]
                progressivo = int(parts[1]) + 1
                return f"{base}PF{progressivo:02d}"
            
            return codice_ordine
        finally:
            conn.close()
