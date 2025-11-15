#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PizzaFactory 2.0 - Entry Point"""

from flask import Flask, render_template
from config.settings import Config

def create_app():
    """Factory per creare app Flask"""
    app = Flask(__name__, 
                template_folder='frontend/templates',
                static_folder='frontend/static')
    
    app.config.from_object(Config)
    
    # ðŸ‘‰ Inizializza il sistema di logging
    from config.logging import setup_logging
    setup_logging()
    
    Config.init_app()
    
    # Registra tutti i moduli
    from modules.clienti.routes import clienti_bp
    from modules.ordini.routes import ordini_bp
    from modules.menu.routes import menu_bp
    from modules.serata.routes import serata_bp
    from modules.dashboard.routes import dashboard_bp
    from modules.pagamenti.routes import pagamenti_bp
    from modules.hooks.routes import hooks_bp
    from modules.scorte.routes import scorte_bp
    
    app.register_blueprint(clienti_bp)
    app.register_blueprint(ordini_bp)
    app.register_blueprint(menu_bp)
    app.register_blueprint(serata_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(pagamenti_bp)
    app.register_blueprint(hooks_bp)
    app.register_blueprint(scorte_bp) 
    
    # Route principale
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/mappa_clienti')
    def mappa_clienti():
        return render_template('mappa_clienti.html')
    
    # Gestione errori
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Endpoint non trovato'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {'error': 'Errore interno del server'}, 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    print("=" * 60)
    print("ðŸ• PizzaFactory 2.0 - Architettura Modulare COMPLETA")
    print("=" * 60)
    print(f"ðŸ“¡ Server: http://{Config.HOST}:{Config.PORT}")
    print(f"ðŸ—„ï¸  Database: {Config.DB_PATH}")
    print(f"ðŸ“ Logs: {Config.LOG_FILE}")
    print("ðŸ“¦ Moduli attivi:")
    print("   âœ… clienti")
    print("   âœ… ordini")
    print("   âœ… menu")
    print("   âœ… serata")
    print("   âœ… dashboard")
    print("   âœ… pagamenti")
    print("   âœ… scorte")
    print("=" * 60)
    print()
    
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
