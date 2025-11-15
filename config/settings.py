#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Configurazione applicazione"""

import os

class Config:
    # Percorsi
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DB_PATH = os.path.join(BASE_DIR, 'data', 'pizzeria.db')
    
    # Flask
    SECRET_KEY = 'pizzeria-secret-key-2024'
    DEBUG = True
    
    # Server
    HOST = '0.0.0.0'
    PORT = 5000
    
     # ðŸ” Chiave per MacroDroid
    MACRODROID_SECRET = "mypass123"
    
    # Logging
    LOG_DIR = os.path.join(BASE_DIR, 'logs')
    LOG_FILE = os.path.join(LOG_DIR, 'pizzeria.log')
    
    # Sovrappressi
    SOVRAPPREZZO_CONSEGNA_MINIMO = 15.00
    SOVRAPPREZZO_CONSEGNA_IMPORTO = 2.00
    
    @staticmethod
    def init_app():
        os.makedirs(Config.LOG_DIR, exist_ok=True)
