#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gestione hook MacroDroid - Versione live + test"""

from flask import Blueprint, request, jsonify, current_app
from .service import gestisci_evento

# Blueprint per il modulo MacroDroid
hooks_bp = Blueprint('hooks', __name__, url_prefix='/api/hooks')


# ============================================================
# 🔴 Endpoint LIVE - utilizzato da MacroDroid reale
# ============================================================
@hooks_bp.route('/macrodroid', methods=['POST'])
def ricevi_evento_macrodroid():
    """Riceve eventi da MacroDroid (live)"""
    data = request.get_json(silent=True) or {}
    numero = data.get("numero")
    evento = data.get("evento")
    token = request.headers.get("Authorization")

    # Verifica token di sicurezza
    secret = current_app.config.get('MACRODROID_SECRET')
    if token != f"Bearer {secret}":
        current_app.logger.warning(f"[HOOK] Accesso negato - Token non valido: {token}")
        return jsonify({"status": "error", "msg": "Token non valido"}), 401

    if not numero or not evento:
        current_app.logger.warning("[HOOK] Richiesta incompleta - Dati mancanti")
        return jsonify({"status": "error", "msg": "Dati mancanti"}), 400

    result = gestisci_evento(numero, evento)
    current_app.logger.info(f"[HOOK] Evento live gestito con successo → {result}")
    return jsonify(result), 200


# ============================================================
# 🧪 Endpoint di test locale (simula evento MacroDroid)
# ============================================================
@hooks_bp.route('/test', methods=['GET'])
def test_evento_macrodroid():
    """Simula un evento MacroDroid per test locale senza telefono."""
    numero_fake = "349-0633281"
    evento_fake = "chiamata_in_arrivo"

    result = gestisci_evento(numero_fake, evento_fake)
    current_app.logger.info(f"[HOOK TEST] Simulazione → {numero_fake} ({evento_fake})")

    return jsonify({
        "test_mode": True,
        "simulato": {"numero": numero_fake, "evento": evento_fake},
        "risultato": result
    }), 200
