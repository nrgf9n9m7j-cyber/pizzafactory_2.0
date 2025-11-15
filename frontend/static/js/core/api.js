// ========================================
// CORE/API.JS - Chiamate API Centralizzate
// ========================================

const API = {
    // Base URL (opzionale, Flask lo gestisce)
    baseUrl: '',
    
    // ========================================
    // CLIENTI
    // ========================================
    async cercaClienti(query) {
        const response = await fetch(`/api/clienti/cerca?q=${encodeURIComponent(query)}`);
        if (!response.ok) throw new Error('Errore ricerca clienti');
        return response.json();
    },
    
    async getCliente(id) {
        const response = await fetch(`/api/clienti/${id}`);
        if (!response.ok) throw new Error('Cliente non trovato');
        return response.json();
    },
    
    async creaCliente(data) {
        const response = await fetch('/api/clienti', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if (!response.ok) throw new Error('Errore creazione cliente');
        return response.json();
    },
    
    // ========================================
    // PRODOTTI
    // ========================================
    async getProdotti(formato = null) {
        const url = formato ? `/api/prodotti?formato=${formato}` : '/api/prodotti';
        const response = await fetch(url);
        if (!response.ok) throw new Error('Errore caricamento prodotti');
        return response.json();
    },
    
    async getIngredienti() {
        const response = await fetch('/api/ingredienti');
        if (!response.ok) throw new Error('Errore caricamento ingredienti');
        return response.json();
    },
    
    async getBibite() {
        const response = await fetch('/api/bibite');
        if (!response.ok) throw new Error('Errore caricamento bibite');
        return response.json();
    },
    
    async getMenuCompleto() {
        const response = await fetch('/api/menu');
        if (!response.ok) throw new Error('Errore caricamento menu');
        return response.json();
    },
    
    // ========================================
    // ORDINI
    // ========================================
    async creaOrdine(data) {
        const response = await fetch('/api/ordini', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if (!response.ok) throw new Error('Errore creazione ordine');
        return response.json();
    },
    
    async getOrdiniAttivi() {
        const response = await fetch('/api/ordini');
        if (!response.ok) throw new Error('Errore caricamento ordini');
        return response.json();
    },
    
    async getOrdine(id) {
        const response = await fetch(`/api/ordini/${id}`);
        if (!response.ok) throw new Error('Ordine non trovato');
        return response.json();
    },
    
    async aggiornaOrdine(id, data) {
        const response = await fetch(`/api/ordini/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if (!response.ok) throw new Error('Errore aggiornamento ordine');
        return response.json();
    },
    
    async eliminaOrdine(id) {
        const response = await fetch(`/api/ordini/${id}`, {
            method: 'DELETE'
        });
        if (!response.ok) throw new Error('Errore eliminazione ordine');
        return response.json();
    }
};

console.log('✅ API.js caricato');
