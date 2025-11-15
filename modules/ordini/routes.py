#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Routes API Ordini"""

from flask import Blueprint, request, jsonify
from .model import OrdineModel
from .service import OrdineService
from .calcoli import calcola_sovrapprezzo_consegna
from core.exceptions import ValidationError, NotFoundError

ordini_bp = Blueprint('ordini', __name__, url_prefix='/api/ordini')

@ordini_bp.route('/', methods=['GET'])
def get_ordini():
    """GET /api/ordini"""
    try:
        ordini = OrdineModel.get_attivi()
        return jsonify(ordini)
    except Exception as e:
        return jsonify({'error': 'Errore interno'}), 500

@ordini_bp.route('/<int:ordine_id>', methods=['GET'])
def get_dettaglio_ordine(ordine_id):
    """GET /api/ordini/:id"""
    try:
        dettaglio = OrdineModel.get_by_id(ordine_id)
        if not dettaglio:
            return jsonify({'error': 'Ordine non trovato'}), 404
        return jsonify(dettaglio)
    except Exception as e:
        return jsonify({'error': 'Errore interno'}), 500

@ordini_bp.route('/', methods=['POST'])
def crea_ordine():
    """POST /api/ordini"""
    try:
        data = request.json
        
        # Calcola sovrappressi
        sovrapprezzo_consegna = 0.00
        if data.get('id_tipo') == 1:
            totale_prodotti = data.get('totale_ordine', 0)
            sovrapprezzo_consegna = calcola_sovrapprezzo_consegna(totale_prodotti, 1)
        
        sovrapprezzo_citta = data.get('sovrapprezzo_citta', 0.00)
        totale_finale = data.get('totale_ordine', 0) + sovrapprezzo_consegna + sovrapprezzo_citta
        
        ordine_data = {
            'id_cliente': data.get('id_cliente'),
            'id_tipo': data.get('id_tipo'),
            'id_metodo_pagamento': data.get('id_metodo_pagamento'),
            'numero_tavolo': data.get('numero_tavolo'),
            'orario_ritiro': data.get('orario_ritiro'),
            'orario_consegna': data.get('orario_consegna'),
            'indirizzo_consegna': data.get('indirizzo_consegna'),
            'civico_consegna': data.get('civico_consegna'),
            'citta_consegna': data.get('citta_consegna'),
            'telefono_consegna': data.get('telefono_consegna'),
            'note_ordine': data.get('note_ordine'),
            'totale_finale': totale_finale,
            'sovrapprezzo_consegna': sovrapprezzo_consegna,
            'sovrapprezzo_citta': sovrapprezzo_citta,
            'pagato': data.get('pagato', 0),
            'prodotti': data.get('prodotti', [])
        }
        
        result = OrdineService.crea_ordine(ordine_data)
        return jsonify(result), 201
    except ValidationError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': 'Errore interno'}), 500

@ordini_bp.route('/<int:ordine_id>', methods=['PUT'])
def aggiorna_ordine(ordine_id):
    """PUT /api/ordini/:id"""
    try:
        data = request.json
        
        # Calcola sovrappressi
        sovrapprezzo_consegna = 0.00
        if data.get('id_tipo') == 1:
            totale_prodotti = data.get('totale_ordine', 0)
            sovrapprezzo_consegna = calcola_sovrapprezzo_consegna(totale_prodotti, 1)
        
        sovrapprezzo_citta = data.get('sovrapprezzo_citta', 0.00)
        totale_finale = data.get('totale_ordine', 0) + sovrapprezzo_consegna + sovrapprezzo_citta
        
        ordine_data = {
            'id_cliente': data.get('id_cliente'),
            'id_tipo': data.get('id_tipo'),
            'id_metodo_pagamento': data.get('id_metodo_pagamento'),
            'numero_tavolo': data.get('numero_tavolo'),
            'orario_ritiro': data.get('orario_ritiro'),
            'orario_consegna': data.get('orario_consegna'),
            'indirizzo_consegna': data.get('indirizzo_consegna'),
            'civico_consegna': data.get('civico_consegna'),
            'citta_consegna': data.get('citta_consegna'),
            'telefono_consegna': data.get('telefono_consegna'),
            'note_ordine': data.get('note_ordine'),
            'totale_finale': totale_finale,
            'sovrapprezzo_consegna': sovrapprezzo_consegna,
            'sovrapprezzo_citta': sovrapprezzo_citta,
            'pagato': data.get('pagato', 0),
            'prodotti': data.get('prodotti', [])
        }
        
        result = OrdineService.aggiorna_ordine(ordine_id, ordine_data)
        return jsonify(result)
    except NotFoundError as e:
        return jsonify({'success': False, 'error': str(e)}), 404
    except ValidationError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': 'Errore interno'}), 500

@ordini_bp.route('/<int:ordine_id>/pagato', methods=['PUT'])
def aggiorna_pagato(ordine_id):
    """PUT /api/ordini/:id/pagato"""
    try:
        data = request.json
        pagato = data.get('pagato', 0)
        OrdineModel.update_pagato(ordine_id, pagato)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': 'Errore interno'}), 500

@ordini_bp.route('/<int:ordine_id>', methods=['DELETE'])
def elimina_ordine(ordine_id):
    """DELETE /api/ordini/:id"""
    try:
        OrdineModel.delete(ordine_id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': 'Errore interno'}), 500

@ordini_bp.route('/totali', methods=['GET'])
def get_totali():
    """GET /api/ordini/totali"""
    try:
        totali = OrdineModel.get_totali_attivi()
        return jsonify(totali)
    except Exception as e:
        return jsonify({'error': 'Errore interno'}), 500
