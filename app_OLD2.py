#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PizzaFactory 2.0 - Entry Point SEMPLIFICATO"""

from flask import Flask, render_template, jsonify, request
import sqlite3
import os

# ========================================
# CONFIGURAZIONE
# ========================================
class Config:
    HOST = '0.0.0.0'
    PORT = 5000
    DEBUG = True
    DB_PATH = 'data/pizzeria.db'

# ========================================
# UTILITY DATABASE
# ========================================
def get_db():
    """Connessione database con row_factory per dict"""
    conn = sqlite3.connect(Config.DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ========================================
# CREA APP
# ========================================
app = Flask(__name__,
            template_folder='frontend/templates',
            static_folder='frontend/static')

app.config.from_object(Config)

# ========================================
# ROUTE PAGINE HTML
# ========================================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mappa_clienti')
def mappa_clienti():
    return render_template('mappa_clienti.html')

@app.route('/test_diagnostico')
def test_diagnostico():
    return render_template('test_diagnostico.html')

# ========================================
# API ENDPOINTS
# ========================================

# ========================================
# API: PRODOTTI
# ========================================

# Route SPECIFICA – deve venire PRIMA
@app.route('/api/menu/prodotti/<formato>', methods=['GET'])
def get_prodotti_menu(formato):
    """Endpoint: /api/menu/prodotti/pizza"""
    print(f"📦 GET /api/menu/prodotti/{formato}")
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM Prodotti WHERE Formato = ? ORDER BY Nome_Prodotto',
            (formato,)
        )
        rows = cursor.fetchall()
        prodotti = [dict(row) for row in rows]
        conn.close()
        return jsonify(prodotti), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Route GENERICA – deve venire DOPO
@app.route('/api/prodotti', methods=['GET'])
def get_prodotti():
    """Endpoint: /api/prodotti?formato=pizza"""
    formato = request.args.get('formato', None)
    disponibile = request.args.get('disponibile', None)

    print(f"📦 GET /api/prodotti?formato={formato}&disponibile={disponibile}")

    try:
        conn = get_db()
        cursor = conn.cursor()

        query = 'SELECT * FROM Prodotti WHERE 1=1'
        params = []

        if formato:
            query += ' AND Formato = ?'
            params.append(formato)

        if disponibile is not None:
            query += ' AND Disponibile = ?'
            params.append(int(disponibile))

        query += ' ORDER BY Ordinamento, Nome_Prodotto'

        cursor.execute(query, params)
        rows = cursor.fetchall()

        prodotti = [dict(row) for row in rows]

        conn.close()

        return jsonify(prodotti), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ========================================
# API: INGREDIENTI
# ========================================
@app.route('/api/ingredienti', methods=['GET'])
def get_ingredienti():
    """
    GET /api/ingredienti
    GET /api/ingredienti?categoria=Latticini
    """
    categoria = request.args.get('categoria', None)

    try:
        conn = get_db()
        cursor = conn.cursor()

        query = 'SELECT * FROM Ingredienti WHERE 1=1'
        params = []

        if categoria:
            query += ' AND Categoria = ?'
            params.append(categoria)

        query += ' ORDER BY Categoria, Nome_Ingrediente'

        cursor.execute(query, params)
        rows = cursor.fetchall()

        ingredienti = [dict(row) for row in rows]

        conn.close()

        return jsonify(ingredienti), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ========================================
# API: CLIENTI
# ========================================
@app.route('/api/clienti/cerca', methods=['GET'])
def cerca_clienti():
    """GET /api/clienti/cerca?q=mario"""
    query = request.args.get('q', '')

    if not query or len(query) < 2:
        return jsonify([]), 200

    try:
        conn = get_db()
        cursor = conn.cursor()

        search_pattern = f'%{query}%'

        cursor.execute('''
            SELECT * FROM Clienti 
            WHERE Nome LIKE ? 
               OR Cognome LIKE ? 
               OR Telefono LIKE ?
            ORDER BY Totale_Ordini DESC
            LIMIT 10
        ''', (search_pattern, search_pattern, search_pattern))

        rows = cursor.fetchall()
        clienti = [dict(row) for row in rows]

        conn.close()

        return jsonify(clienti), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/clienti', methods=['POST'])
def crea_cliente():
    """POST /api/clienti - Crea nuovo cliente"""
    data = request.get_json()

    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO Clienti (Nome, Cognome, Telefono, Indirizzo, Civico, Citta, Note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('nome'),
            data.get('cognome'),
            data.get('telefono'),
            data.get('indirizzo'),
            data.get('civico'),
            data.get('citta', 'Chieri'),
            data.get('note')
        ))

        conn.commit()
        id_cliente = cursor.lastrowid
        conn.close()

        return jsonify({'success': True, 'id': id_cliente}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ========================================
# API: ORDINI
# ========================================
@app.route('/api/ordini', methods=['POST'])
def crea_ordine():
    """POST /api/ordini - Crea nuovo ordine"""
    data = request.get_json()

    try:
        conn = get_db()
        cursor = conn.cursor()

        # Inserisci ordine
        cursor.execute('''
            INSERT INTO Ordini (
                ID_Cliente, Tipo_Ordine, Totale, 
                Sovrapprezzo_Consegna, Metodo_Pagamento, Note
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data.get('id_cliente'),
            data.get('tipo_ordine'),
            data.get('totale'),
            data.get('sovrapprezzo', 0),
            data.get('metodo_pagamento', 'Contanti'),
            data.get('note')
        ))

        id_ordine = cursor.lastrowid

        # Inserisci prodotti ordine
        for item in data.get('prodotti', []):
            cursor.execute('''
                INSERT INTO Ordini_Prodotti (
                    ID_Ordine, ID_Prodotto, Quantita, 
                    Prezzo_Unitario, Formato, Note
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                id_ordine,
                item['id'],
                item['quantita'],
                item['prezzo'],
                item.get('formato', 'pizza'),
                item.get('note')
            ))

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'id_ordine': id_ordine}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ========================================
# GESTIONE ERRORI
# ========================================
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint non trovato'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Errore interno del server'}), 500


# ========================================
# MAIN
# ========================================
if __name__ == '__main__':
    print("=" * 60)
    print("🍕 PizzaFactory 2.0 - Versione Semplificata")
    print("=" * 60)
    print(f"🌐 Server: http://{Config.HOST}:{Config.PORT}")
    print(f"🗄️  Database: {Config.DB_PATH}")
    print()
    print("📋 API Endpoints disponibili:")
    print("   • GET  /api/prodotti?formato=pizza")
    print("   • GET  /api/menu/prodotti/<formato>")
    print("   • GET  /api/ingredienti")
    print("   • GET  /api/clienti/cerca?q=...")
    print("   • POST /api/clienti")
    print("   • POST /api/ordini")
    print()
    print("🌍 Pagine:")
    print("   • http://localhost:5000/")
    print("   • http://localhost:5000/test_diagnostico")
    print("   • http://localhost:5000/mappa_clienti")
    print("=" * 60)
    print()

    if not os.path.exists(Config.DB_PATH):
        print("⚠️  ATTENZIONE: Database non trovato!")
        print("   Esegui prima: python setup_database.py")
        print()

    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
