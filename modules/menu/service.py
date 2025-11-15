#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Service Menu - logica business"""

from .model import MenuModel
from core.exceptions import ValidationError, NotFoundError

class MenuService:
    
    @staticmethod
    def get_menu_completo():
        """Recupera menu completo con tutte le categorie"""
        return {
            'prodotti': MenuModel.get_prodotti(),
            'ingredienti': MenuModel.get_ingredienti(),
            'impasti': MenuModel.get_impasti(),
            'opzioni': MenuModel.get_opzioni(),
            'bibite': MenuModel.get_bibite(),
            'metodi_pagamento': MenuModel.get_metodi_pagamento(),
            'tipi_ordine': MenuModel.get_tipi_ordine()
        }
    
    @staticmethod
    def crea_prodotto(data):
        """Crea prodotto con validazione"""
        # Valida
        if not data.get('nome'):
            raise ValidationError("Nome prodotto obbligatorio")
        if not data.get('prezzo') or data['prezzo'] <= 0:
            raise ValidationError("Prezzo deve essere maggiore di 0")
        
        # Crea
        return MenuModel.create_prodotto(data)
    
    @staticmethod
    def aggiorna_prodotto(prodotto_id, data):
        """Aggiorna prodotto con validazione"""
        # Verifica esistenza
        prodotto = MenuModel.get_prodotto_by_id(prodotto_id)
        if not prodotto:
            raise NotFoundError(f"Prodotto {prodotto_id} non trovato")
        
        # Valida
        if not data.get('nome'):
            raise ValidationError("Nome prodotto obbligatorio")
        if not data.get('prezzo') or data['prezzo'] <= 0:
            raise ValidationError("Prezzo deve essere maggiore di 0")
        
        # Aggiorna
        MenuModel.update_prodotto(prodotto_id, data)
