#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Eccezioni custom"""

class PizzaFactoryException(Exception):
    """Eccezione base"""
    pass

class ValidationError(PizzaFactoryException):
    """Errore validazione"""
    pass

class DatabaseError(PizzaFactoryException):
    """Errore database"""
    pass

class NotFoundError(PizzaFactoryException):
    """Risorsa non trovata"""
    pass
