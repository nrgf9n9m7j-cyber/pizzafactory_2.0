#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validators Clienti"""

from core.validators import BaseValidator
from core.exceptions import ValidationError

class ClienteValidator:
    
    @staticmethod
    def valida_dati_cliente(data):
        """Valida dati cliente completi"""
        # Campi obbligatori
        if not data.get('cognome'):
            raise ValidationError("Cognome obbligatorio")
        
        if not data.get('telefono'):
            raise ValidationError("Telefono obbligatorio")
        
        # Valida telefono
        if not BaseValidator.valida_telefono(data['telefono']):
            raise ValidationError("Formato telefono non valido")
        
        # Valida rating se presente
        rating = data.get('rating')
        if rating is not None:
            if not isinstance(rating, int) or rating < 1 or rating > 5:
                raise ValidationError("Rating deve essere tra 1 e 5")
        
        return True
