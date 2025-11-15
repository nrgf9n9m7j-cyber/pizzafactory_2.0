#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Service Clienti - logica business"""

from datetime import datetime
import time
import urllib.parse
import urllib.request
import json

from .model import ClienteModel
from .validators import ClienteValidator
from core.exceptions import ValidationError, NotFoundError

class ClienteService:
    
    @staticmethod
    def crea_cliente(data):
        """Crea cliente con validazione"""
        # Valida
        ClienteValidator.valida_dati_cliente(data)
        
        # Crea
        cliente_id = ClienteModel.create(data)
        return cliente_id
    
    @staticmethod
    def aggiorna_cliente(cliente_id, data):
        """Aggiorna cliente con validazione"""
        # Verifica esista
        cliente = ClienteModel.get_by_id(cliente_id)
        if not cliente:
            raise NotFoundError(f"Cliente {cliente_id} non trovato")
        
        # Valida
        ClienteValidator.valida_dati_cliente(data)
        
        # Aggiorna
        ClienteModel.update(cliente_id, data)
    
    @staticmethod
    def get_clienti_per_mappa():
        """Recupera clienti con dati per mappa"""
        clienti = ClienteModel.get_with_stats()
        risultati = []
        oggi = datetime.now().date()
        
        for cliente in clienti:
            # Solo con coordinate
            if not cliente.get('Latitudine') or not cliente.get('Longitudine'):
                continue
            
            # Calcola lifecycle
            lifecycle = ClienteService._calcola_lifecycle(
                cliente['num_ordini'],
                cliente.get('ultimo_ordine'),
                oggi
            )
            
            # Calcola rating
            rating_info = ClienteService._calcola_rating_info(cliente.get('Rating'))
            
            risultati.append({
                'ID_Cliente': cliente['ID_Cliente'],
                'Nome': cliente.get('Nome'),
                'Cognome': cliente.get('Cognome'),
                'Indirizzo': cliente.get('Indirizzo'),
                'Civico': cliente.get('Civico'),
                'Citta': cliente.get('Citta'),
                'Telefono': cliente.get('Telefono'),
                'Latitudine': cliente['Latitudine'],
                'Longitudine': cliente['Longitudine'],
                'Note_Staff': cliente.get('Note_Staff'),
                'totale_speso': cliente.get('totale_speso') or 0.0,
                'lifecycle': lifecycle,
                'rating': rating_info
            })
        
        return risultati
    
    @staticmethod
    def _calcola_lifecycle(num_ordini, ultimo_ordine_str, oggi):
        """Calcola stato lifecycle cliente"""
        if num_ordini == 0:
            return {'status': 'Mai Ordinato', 'emoji': '❓', 'num_ordini': 0, 'ultimo_ordine': None}
        
        if not ultimo_ordine_str:
            return {'status': 'Nuovo', 'emoji': '🆕', 'num_ordini': num_ordini, 'ultimo_ordine': None}
        
        ultimo_ordine = datetime.strptime(ultimo_ordine_str, '%Y-%m-%d').date()
        giorni_inattivo = (oggi - ultimo_ordine).days
        
        if giorni_inattivo > 60:
            status, emoji = 'Dormiente', '😴'
        elif num_ordini == 1:
            status, emoji = 'Nuovo', '🆕'
        elif num_ordini <= 5:
            status, emoji = 'Occasionale', '🙂'
        elif num_ordini <= 15:
            status, emoji = 'Abituale', '😊'
        else:
            status, emoji = 'Fidelizzato', '⭐'
        
        return {
            'status': status,
            'emoji': emoji,
            'num_ordini': num_ordini,
            'ultimo_ordine': ultimo_ordine_str
        }
    
    @staticmethod
    def _calcola_rating_info(rating_val):
        """Calcola info rating cliente"""
        mapping = {
            5: ('🤩', 'Top'),
            4: ('😊', 'Gentile'),
            3: ('😐', 'OK'),
            2: ('😕', 'Poco cordiale'),
            1: ('😠', 'Problematico')
        }
        
        emoji, desc = mapping.get(rating_val, ('❓', 'Non valutato'))
        return {'rating': rating_val, 'emoji': emoji, 'descrizione': desc}
    
    @staticmethod
    def geocode_cliente(cliente_id):
        """Geocodifica singolo cliente"""
        cliente = ClienteModel.get_by_id(cliente_id)
        if not cliente:
            raise NotFoundError(f"Cliente {cliente_id} non trovato")
        
        if not cliente.get('Indirizzo') or not cliente.get('Citta'):
            raise ValidationError("Cliente senza indirizzo completo")
        
        # Geocoding
        indirizzo_completo = f"{cliente['Indirizzo']} {cliente.get('Civico', '')}, {cliente['Citta']}, Italia"
        lat, lon = ClienteService._geocode_address(indirizzo_completo)
        
        # Salva
        ClienteModel.update_coordinates(cliente_id, lat, lon)
        return {'lat': lat, 'lon': lon}
    
    @staticmethod
    def geocode_all():
        """Geocodifica tutti i clienti senza coordinate"""
        clienti = ClienteModel.get_without_coordinates()
        success = 0
        
        for cliente in clienti:
            try:
                indirizzo_completo = f"{cliente['Indirizzo']} {cliente.get('Civico', '')}, {cliente['Citta']}, Italia"
                lat, lon = ClienteService._geocode_address(indirizzo_completo)
                ClienteModel.update_coordinates(cliente['ID_Cliente'], lat, lon)
                success += 1
                time.sleep(1.1)  # Rate limit Nominatim
            except Exception as e:
                print(f"Errore geocoding cliente {cliente['ID_Cliente']}: {e}")
                continue
        
        return {'success': success, 'total': len(clienti)}
    
    @staticmethod
    def _geocode_address(indirizzo):
        """Geocodifica indirizzo con Nominatim"""
        url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(indirizzo)}&format=json&limit=1"
        
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'PizzaFactory/2.0')
        
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
        
        if not data:
            raise ValidationError(f"Indirizzo non trovato: {indirizzo}")
        
        return float(data[0]['lat']), float(data[0]['lon'])
