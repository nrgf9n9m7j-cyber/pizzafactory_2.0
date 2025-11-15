#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Service Serata"""

from .model import SerataModel
from core.exceptions import ValidationError

class SerataService:
    
    @staticmethod
    def apri_serata(data):
        """Apri serata con validazione"""
        if not data.get('palline_iniziali'):
            raise ValidationError("Palline iniziali obbligatorie")
        
        return SerataModel.apri(data, data.get('data_serata'), data.get('ora_apertura'))
    
    @staticmethod
    def chiudi_serata(serata_id, rimanenze):
        """Chiudi serata con rimanenze"""
        if not rimanenze.get('palline_finali'):
            raise ValidationError("Palline finali obbligatorie")
        
        SerataModel.chiudi(serata_id, rimanenze)
