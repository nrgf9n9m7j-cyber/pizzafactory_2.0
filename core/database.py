#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gestione connessione database"""

import sqlite3
from config.settings import Config

def get_db_connection():
    """Crea connessione database con row_factory per dict"""
    conn = sqlite3.connect(Config.DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
