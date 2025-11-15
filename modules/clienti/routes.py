#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Routes API Clienti"""

from flask import Blueprint, request, jsonify
from .model import ClienteModel
from .service import ClienteService
from core.exceptions import ValidationError, NotFoundError

clienti_bp = Blueprint('clienti', __name__, url_prefix='/api/clienti')

@clienti_bp.route('/cerca')
def cerca_clienti():
    """GET /api/clienti/cerca?q=query"""
    query = request.args.get('q', '')
    
    if len(query) < 2:
        return jsonify([])
    
    clienti = ClienteModel.cerca(query)
    return jsonify(clienti)

@clienti_bp.route('/<int:cliente_id>')
def get_cliente(cliente_id):
    """GET /api/clienti/:id"""
    cliente = ClienteModel.get_by_id(cliente_id)
    
    if not cliente:
        return jsonify({'error': 'Cliente non trovato'}), 404
    
    return jsonify(cliente)

@clienti_bp.route('/', methods=['POST'])
def crea_cliente():
    """POST /api/clienti"""
    try:
        data = request.json
        cliente_id = ClienteService.crea_cliente(data)
        return jsonify({'id': cliente_id, 'success': True}), 201
    except ValidationError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': 'Errore interno'}), 500

@clienti_bp.route('/<int:cliente_id>', methods=['PUT'])
def aggiorna_cliente(cliente_id):
    """PUT /api/clienti/:id"""
    try:
        data = request.json
        ClienteService.aggiorna_cliente(cliente_id, data)
        return jsonify({'success': True})
    except NotFoundError as e:
        return jsonify({'success': False, 'error': str(e)}), 404
    except ValidationError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': 'Errore interno'}), 500

@clienti_bp.route('/<int:cliente_id>/rating', methods=['PUT'])
def aggiorna_rating(cliente_id):
    """PUT /api/clienti/:id/rating"""
    try:
        data = request.json
        rating = data.get('rating')
        note_staff = data.get('note_staff')
        
        if rating is not None and (rating < 1 or rating > 5):
            raise ValidationError('Rating deve essere tra 1 e 5')
        
        ClienteModel.update_rating(cliente_id, rating, note_staff)
        return jsonify({'success': True})
    except ValidationError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': 'Errore interno'}), 500

@clienti_bp.route('/mappa')
def get_clienti_mappa():
    """GET /api/clienti/mappa"""
    try:
        clienti = ClienteService.get_clienti_per_mappa()
        return jsonify(clienti)
    except Exception as e:
        return jsonify({'error': 'Errore interno'}), 500

@clienti_bp.route('/geocode-all', methods=['POST'])
def geocode_all_clienti():
    """POST /api/clienti/geocode-all"""
    try:
        result = ClienteService.geocode_all()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': 'Errore interno'}), 500
