// ========================================
// MODULES/ORDINI/PIZZE.JS
// Gestione menu pizze con supporto formati
// ========================================

const PizzeModule = {
    pizze: [],
    
    // ========================================
    // CARICA E RENDER PIZZE
    // ========================================
    async renderTopPizze() {
        try {
            const prodotti = await API.getProdotti('pizza');
            this.pizze = prodotti.slice(0, 8);
            this.render();
            console.log('✅ Top 8 pizze caricate:', this.pizze.length);
        } catch (error) {
            console.error('❌ Errore caricamento pizze:', error);
            this.renderErrore();
        }
    },
    
    async renderTuttePizze() {
        try {
            const prodotti = await API.getProdotti('pizza');
            this.pizze = prodotti;
            this.render();
            console.log('✅ Tutte le pizze caricate:', this.pizze.length);
        } catch (error) {
            console.error('❌ Errore caricamento pizze:', error);
            this.renderErrore();
        }
    },
    
    // ========================================
    // RENDER PIZZE
    // ========================================
    render() {
        const container = document.getElementById('pizza-grid-top8') || document.getElementById('pizza-grid');
        if (!container) {
            console.warn('⚠️ Container pizze non trovato');
            return;
        }
        
        const fragment = document.createDocumentFragment();
        
        this.pizze.forEach((pizza, index) => {
            const card = Utils.createElement('div', 'pizza-card');
            card.dataset.id = pizza.ID_Prodotto;
            card.dataset.nome = pizza.Nome_Prodotto;
            card.dataset.prezzoBase = pizza.Prezzo_Base;  // Prezzo base per calcolo formato
            
            card.innerHTML = `
                <div class="pizza-badge">#${index + 1}</div>
                <div class="pizza-icon">🍕</div>
                <div class="pizza-name">${pizza.Nome_Prodotto}</div>
                <div class="pizza-price prezzo">€${Utils.formatMoney(pizza.Prezzo_Base)}</div>
            `;
            
            // Quando si clicca, usa il formato selezionato
            card.onclick = () => this.aggiungiPizzaConFormato(pizza);
            
            fragment.appendChild(card);
        });
        
        container.innerHTML = '';
        container.appendChild(fragment);
    },
    
    // ========================================
    // AGGIUNGI PIZZA CON FORMATO
    // ========================================
    aggiungiPizzaConFormato(pizza) {
        // Ottieni formato selezionato
        const formatoSelezionato = window.FormatiModule ? 
            window.FormatiModule.getFormatoSelezionato() : 'classica';
        
        // Calcola prezzo con formato
        const prezzoBase = parseFloat(pizza.Prezzo_Base);
        const prezzoFinale = window.FormatiModule ? 
            window.FormatiModule.calcolaPrezzoConFormato(prezzoBase, formatoSelezionato) : 
            prezzoBase;
        
        // Nome pizza con formato (se diverso da classica)
        const nomePizza = formatoSelezionato !== 'classica' ? 
            `${pizza.Nome_Prodotto} (${formatoSelezionato.charAt(0).toUpperCase() + formatoSelezionato.slice(1)})` : 
            pizza.Nome_Prodotto;
        
        // Aggiungi al carrello
        CarrelloModule.aggiungi(
            pizza.ID_Prodotto,
            nomePizza,
            prezzoFinale,
            formatoSelezionato
        );
    },
    
    // ========================================
    // RENDER ERRORE
    // ========================================
    renderErrore() {
        const container = document.getElementById('pizza-grid-top8') || document.getElementById('pizza-grid');
        if (container) {
            container.innerHTML = `
                <div style="grid-column: 1/-1; text-align:center; padding:20px; color:#999;">
                    ❌ Errore caricamento pizze
                </div>
            `;
        }
    }
};

console.log('✔️ PizzeModule caricato con supporto formati');

// Export globale
window.PizzeModule = PizzeModule;
