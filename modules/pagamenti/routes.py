#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Routes API Pagamenti"""

from flask import Blueprint, request, jsonify
from .model import PagamentoModel
from core.exceptions import DatabaseError

pagamenti_bp = Blueprint('pagamenti', __name__, url_prefix='/api/pagamenti')

@pagamenti_bp.route('/parziale', methods=['POST'])
def registra_parziale():
    """POST /api/pagamenti/parziale"""
    try:
        data = request.json
        pagamento_id = PagamentoModel.registra_parziale(
            data['ordine_id'],
            data['importo'],
            data.get('prodotti_ids', []),
            data.get('note', '')
        )
        return jsonify({'success': True, 'id': pagamento_id}), 201
    except DatabaseError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': 'Errore interno'}), 500

@pagamenti_bp.route('/storico/<int:ordine_id>', methods=['GET'])
def get_storico(ordine_id):
    """GET /api/pagamenti/storico/:id"""
    try:
        storico = PagamentoModel.get_storico(ordine_id)
        return jsonify(storico)
    except Exception as e:
        return jsonify({'error': 'Errore interno'}), 500

@pagamenti_bp.route('/prodotti/<int:ordine_id>', methods=['GET'])
def get_prodotti(ordine_id):
    """GET /api/pagamenti/prodotti/:id"""
    try:
        prodotti = PagamentoModel.get_prodotti_ordine(ordine_id)
        return jsonify(prodotti)
    except Exception as e:
        return jsonify({'error': 'Errore interno'}), 500
