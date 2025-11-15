#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Routes API Menu/Prodotti"""

from flask import Blueprint, request, jsonify
from .model import MenuModel
from .service import MenuService
from core.exceptions import ValidationError, NotFoundError

menu_bp = Blueprint('menu', __name__, url_prefix='/api')

@menu_bp.route('/menu', methods=['GET'])
def get_menu_completo():
    """GET /api/menu - Menu completo"""
    try:
        menu = MenuService.get_menu_completo()
        return jsonify(menu)
    except Exception as e:
        return jsonify({'error': 'Errore interno'}), 500

@menu_bp.route('/prodotti', methods=['GET'])
def get_prodotti():
    """GET /api/prodotti"""
    try:
        formato = request.args.get('formato')
        prodotti = MenuModel.get_prodotti(formato=formato)
        return jsonify(prodotti)
    except Exception as e:
        return jsonify({'error': 'Errore interno'}), 500

@menu_bp.route('/prodotti/<int:prodotto_id>', methods=['GET'])
def get_prodotto(prodotto_id):
    """GET /api/prodotti/:id"""
    try:
        prodotto = MenuModel.get_prodotto_by_id(prodotto_id)
        if not prodotto:
            return jsonify({'error': 'Prodotto non trovato'}), 404
        return jsonify(prodotto)
    except Exception as e:
        return jsonify({'error': 'Errore interno'}), 500

@menu_bp.route('/prodotti', methods=['POST'])
def crea_prodotto():
    """POST /api/prodotti"""
    try:
        data = request.json
        prodotto_id = MenuService.crea_prodotto(data)
        return jsonify({'success': True, 'id': prodotto_id}), 201
    except ValidationError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': 'Errore interno'}), 500

@menu_bp.route('/prodotti/<int:prodotto_id>', methods=['PUT'])
def aggiorna_prodotto(prodotto_id):
    """PUT /api/prodotti/:id"""
    try:
        data = request.json
        MenuService.aggiorna_prodotto(prodotto_id, data)
        return jsonify({'success': True})
    except NotFoundError as e:
        return jsonify({'success': False, 'error': str(e)}), 404
    except ValidationError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': 'Errore interno'}), 500

@menu_bp.route('/prodotti/<int:prodotto_id>', methods=['DELETE'])
def elimina_prodotto(prodotto_id):
    """DELETE /api/prodotti/:id (soft delete)"""
    try:
        MenuModel.soft_delete_prodotto(prodotto_id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': 'Errore interno'}), 500

@menu_bp.route('/ingredienti', methods=['GET'])
def get_ingredienti():
    """GET /api/ingredienti"""
    try:
        ingredienti = MenuModel.get_ingredienti()
        return jsonify(ingredienti)
    except Exception as e:
        return jsonify({'error': 'Errore interno'}), 500

@menu_bp.route('/impasti', methods=['GET'])
def get_impasti():
    """GET /api/impasti"""
    try:
        impasti = MenuModel.get_impasti()
        return jsonify(impasti)
    except Exception as e:
        return jsonify({'error': 'Errore interno'}), 500

@menu_bp.route('/opzioni', methods=['GET'])
def get_opzioni():
    """GET /api/opzioni"""
    try:
        opzioni = MenuModel.get_opzioni()
        return jsonify(opzioni)
    except Exception as e:
        return jsonify({'error': 'Errore interno'}), 500

@menu_bp.route('/bibite', methods=['GET'])
def get_bibite():
    """GET /api/bibite"""
    try:
        bibite = MenuModel.get_bibite()
        return jsonify(bibite)
    except Exception as e:
        return jsonify({'error': 'Errore interno'}), 500

@menu_bp.route('/metodi-pagamento', methods=['GET'])
def get_metodi_pagamento():
    """GET /api/metodi-pagamento"""
    try:
        metodi = MenuModel.get_metodi_pagamento()
        return jsonify(metodi)
    except Exception as e:
        return jsonify({'error': 'Errore interno'}), 500

@menu_bp.route('/tipi-ordine', methods=['GET'])
def get_tipi_ordine():
    """GET /api/tipi-ordine"""
    try:
        tipi = MenuModel.get_tipi_ordine()
        return jsonify(tipi)
    except Exception as e:
        return jsonify({'error': 'Errore interno'}), 500
