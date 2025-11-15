// ========================================
// CORE/STATE.JS - Gestione Stato Globale
// ========================================

const State = {
    // Stato ordine corrente
    ordine: {
        tipo: null,              // 1=Consegna, 2=Ritiro, 3=Tavolo
        cliente: null,           // Oggetto cliente selezionato
        carrello: [],            // Array prodotti
        totaleModificato: null   // Totale custom (se modificato)
    },
    
    // Reset ordine
    resetOrdine() {
        this.ordine.tipo = null;
        this.ordine.cliente = null;
        this.ordine.carrello = [];
        this.ordine.totaleModificato = null;
        console.log('🔄 Stato ordine resettato');
    },
    
    // Getters
    getTipo() {
        return this.ordine.tipo;
    },
    
    getCliente() {
        return this.ordine.cliente;
    },
    
    getCarrello() {
        return this.ordine.carrello;
    },
    
    getTotaleModificato() {
        return this.ordine.totaleModificato;
    },
    
    // Setters
    setTipo(tipo) {
        this.ordine.tipo = tipo;
        console.log('✅ Tipo ordine:', tipo);
    },
    
    setCliente(cliente) {
        this.ordine.cliente = cliente;
        console.log('✅ Cliente selezionato:', cliente?.Cognome);
    },
    
    setTotaleModificato(totale) {
        this.ordine.totaleModificato = totale;
        console.log('✅ Totale modificato:', totale);
    }
};

console.log('✅ State.js caricato');
