#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Calcoli prezzi e sovrappressi ordini"""

from datetime import datetime
from config.settings import Config
from core.database import get_db_connection

def calcola_prezzo_baby(prezzo_base):
    """
    Calcola il prezzo formato Baby: prezzo base - €2.00
    
    Args:
        prezzo_base: Prezzo base del prodotto
    
    Returns:
        float: Prezzo baby arrotondato a 2 decimali
    """
    return round(prezzo_base - 2.00, 2)

def calcola_prezzo_maxi(prezzo_base):
    """
    Calcola il prezzo formato Maxi: (prezzo base × 2.5) arrotondato per eccesso a .50 o .00
    
    Args:
        prezzo_base: Prezzo base del prodotto
    
    Returns:
        float: Prezzo maxi arrotondato
    
    Esempi:
        6.00 × 2.5 = 15.00 → 15.00
        7.50 × 2.5 = 18.75 → 19.00
        8.00 × 2.5 = 20.00 → 20.00
        9.00 × 2.5 = 22.50 → 22.50
    """
    import math
    prezzo_calcolato = prezzo_base * 2.5
    # Arrotonda per eccesso al multiplo di 0.50 più vicino
    return math.ceil(prezzo_calcolato * 2) / 2

def calcola_prezzo_tegamino(prezzo_base):
    """
    Calcola il prezzo formato Tegamino: prezzo base + €1.00
    
    Args:
        prezzo_base: Prezzo base del prodotto
    
    Returns:
        float: Prezzo tegamino arrotondato a 2 decimali
    """
    return round(prezzo_base + 1.00, 2)

def calcola_prezzo_con_formato(prezzo_base, formato):
    """
    Calcola il prezzo applicando il formato selezionato.
    
    Args:
        prezzo_base: Prezzo base del prodotto
        formato: Nome del formato (es. 'classica', 'baby', 'maxi', 'tegamino')
    
    Returns:
        float: Prezzo finale arrotondato
    """
    formato = formato.lower()
    
    if formato == 'baby':
        return calcola_prezzo_baby(prezzo_base)
    elif formato == 'maxi':
        return calcola_prezzo_maxi(prezzo_base)
    elif formato == 'tegamino':
        return calcola_prezzo_tegamino(prezzo_base)
    else:  # classica o pizza
        return round(prezzo_base, 2)

def genera_codice_ordine(data_ordine=None):
    """
    Genera codice ordine: [LetteraGiorno][Mese][PF][Progressivo]
    Es: 18 ottobre, 3° ordine → R10PF03
    """
    if data_ordine is None:
        data_ordine = datetime.now().strftime('%Y-%m-%d')
    
    data_obj = datetime.strptime(data_ordine, '%Y-%m-%d')
    giorno = data_obj.day
    mese = data_obj.month
    
    # Giorno → lettera (A=1, B=2, ..., Z=26, AA=27, ...)
    def numero_a_lettera(n):
        result = ""
        while n > 0:
            n -= 1
            result = chr(65 + (n % 26)) + result
            n //= 26
        return result
    
    lettera_giorno = numero_a_lettera(giorno)
    mese_str = f"{mese:02d}"
    
    # Conta ordini del giorno
    conn = get_db_connection()
    try:
        count = conn.execute('''
            SELECT COUNT(*) FROM Ordini 
            WHERE DATE(Data_Ordine) = ?
        ''', (data_ordine,)).fetchone()[0]
    finally:
        conn.close()
    
    numero_progressivo = count + 1
    progressivo_str = f"{numero_progressivo:02d}"
    
    codice = f"{lettera_giorno}{mese_str}PF{progressivo_str}"
    return codice, numero_progressivo

def calcola_sovrapprezzo_consegna(totale_prodotti, tipo_ordine):
    """Calcola sovrapprezzo consegna per ordini sotto €15"""
    if tipo_ordine == 1 and totale_prodotti > 0 and totale_prodotti < Config.SOVRAPPREZZO_CONSEGNA_MINIMO:
        return Config.SOVRAPPREZZO_CONSEGNA_IMPORTO
    return 0.00

def calcola_totale_ordine(subtotale_prodotti, subtotale_bibite, sovrapprezzo_citta, tipo_ordine):
    """Calcola totale finale ordine"""
    subtotale = subtotale_prodotti + subtotale_bibite
    sovrapprezzo_consegna = calcola_sovrapprezzo_consegna(subtotale, tipo_ordine)
    totale = subtotale + sovrapprezzo_consegna + sovrapprezzo_citta
    
    return {
        'subtotale': round(subtotale, 2),
        'sovrapprezzo_consegna': round(sovrapprezzo_consegna, 2),
        'sovrapprezzo_citta': round(sovrapprezzo_citta, 2),
        'totale': round(totale, 2)
    }

def calcola_prezzo_prodotto(prezzo_base, impasto=None, ingredienti_aggiunti=None):
    """Calcola prezzo prodotto con personalizzazioni"""
    totale = prezzo_base
    
    if impasto and 'Sovrapprezzo' in impasto:
        totale += impasto['Sovrapprezzo']
    
    if ingredienti_aggiunti:
        for ing in ingredienti_aggiunti:
            if 'Prezzo' in ing:
                totale += ing['Prezzo']
    
    return round(totale, 2)
