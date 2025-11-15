// ========================================
// MODULES/ORDINI/PERSONALIZZAZIONE.JS
// Modal personalizzazione pizza (ingredienti, impasto, note)
// STUB - Da implementare completamente
// ========================================

const PersonalizzazioneModule = {
    pizzaCorrente: null,
    
    // ========================================
    // APRI MODAL PERSONALIZZAZIONE
    // ========================================
    apri(pizza) {
        console.log('⚙️ Personalizzazione pizza:', pizza.Nome_Prodotto);
        
        // TODO: Implementare modal completo con:
        // - Selezione impasto (normale, integrale, kamut, s/glutine)
        // - Aggiungi ingredienti extra
        // - Rimuovi ingredienti
        // - Note personalizzate
        // - Quantità
        
        // Per ora: alert placeholder
        alert(`Personalizzazione "${pizza.Nome_Prodotto}" in arrivo!
        
Per ora la pizza verrà aggiunta senza modifiche.`);
        
        // Aggiungi senza personalizzazioni (temporaneo)
        if (typeof CarrelloModule !== 'undefined') {
            CarrelloModule.aggiungi(
                pizza.ID_Prodotto,
                pizza.Nome_Prodotto,
                parseFloat(pizza.Prezzo_Base)
            );
        }
    },
    
    chiudi() {
        // TODO: Chiudi modal personalizzazione
        console.log('⚙️ Modal personalizzazione chiuso');
    }
};

// Export globale
window.PersonalizzazioneModule = PersonalizzazioneModule;

console.log('✅ PersonalizzazioneModule caricato (STUB)');
