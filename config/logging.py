#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Configurazione logging applicazione PizzaFactory 2.0"""

import os
import logging
import logging.config

# Percorso base del progetto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")

# Assicura che la cartella dei log esista
os.makedirs(LOG_DIR, exist_ok=True)

# Configurazione del logging
logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "file_main": {
            "class": "logging.FileHandler",
            "filename": os.path.join(LOG_DIR, "pizzeria.log"),
            "formatter": "default",
        },
        "file_macrodroid": {
            "class": "logging.FileHandler",
            "filename": os.path.join(LOG_DIR, "macrodroid.log"),
            "formatter": "default",
        },
    },
    "loggers": {
        "": {  # root logger
            "handlers": ["console", "file_main"],
            "level": "INFO",
        },
        "macrodroid": {
            "handlers": ["file_macrodroid"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

def setup_logging():
    """Inizializza la configurazione logging"""
    logging.config.dictConfig(logging_config)
