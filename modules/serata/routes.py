#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Routes API Serata"""

from flask import Blueprint, request, jsonify
from .model import SerataModel
from .service import SerataService
from core.exceptions import ValidationError

serata_bp = Blueprint('serata', __name__, url_prefix='/api/serata')

@serata_bp.route('/corrente', methods=['GET'])
def get_corrente():
    """GET /api/serata/corrente"""
    try:
        serata = SerataModel.get_corrente()
        return jsonify(serata)
    except Exception as e:
        return jsonify({'error': 'Errore interno'}), 500

@serata_bp.route('/apri', methods=['POST'])
def apri_serata():
    """POST /api/serata/apri"""
    try:
        data = request.json
        serata_id = SerataService.apri_serata(data)
        return jsonify({'success': True, 'id': serata_id}), 201
    except ValidationError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': 'Errore interno'}), 500

@serata_bp.route('/chiudi/<int:serata_id>', methods=['POST'])
def chiudi_serata(serata_id):
    """POST /api/serata/chiudi/:id"""
    try:
        data = request.json
        SerataService.chiudi_serata(serata_id, data)
        return jsonify({'success': True})
    except ValidationError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': 'Errore interno'}), 500

@serata_bp.route('/rimanenze-precedente', methods=['GET'])
def get_rimanenze():
    """GET /api/serata/rimanenze-precedente"""
    try:
        rimanenze = SerataModel.get_rimanenze_precedente()
        return jsonify(rimanenze)
    except Exception as e:
        return jsonify({'error': 'Errore interno'}), 500
