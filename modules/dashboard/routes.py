#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Routes API Dashboard"""

from flask import Blueprint, jsonify, request
from .model import DashboardModel

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

@dashboard_bp.route('/statistiche', methods=['GET'])
def get_statistiche():
    """GET /api/dashboard/statistiche"""
    try:
        stats = DashboardModel.get_statistiche_serata()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': 'Errore interno'}), 500

@dashboard_bp.route('/top-prodotti', methods=['GET'])
def get_top_prodotti():
    """GET /api/dashboard/top-prodotti"""
    try:
        limite = request.args.get('limite', 5, type=int)
        prodotti = DashboardModel.get_top_prodotti(limite)
        return jsonify(prodotti)
    except Exception as e:
        return jsonify({'error': 'Errore interno'}), 500
