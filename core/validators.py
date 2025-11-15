#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validatori base"""

import re

class BaseValidator:
    @staticmethod
    def valida_telefono(telefono):
        """Valida numero telefono italiano"""
        if not telefono:
            return False
        telefono = re.sub(r'\s+', '', telefono)
        return bool(re.match(r'^(\+39)?3\d{8,9}$', telefono))
    
    @staticmethod
    def valida_email(email):
        """Valida formato email"""
        if not email:
            return False
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def valida_cap(cap):
        """Valida CAP italiano"""
        if not cap:
            return False
        return bool(re.match(r'^\d{5}$', str(cap)))
