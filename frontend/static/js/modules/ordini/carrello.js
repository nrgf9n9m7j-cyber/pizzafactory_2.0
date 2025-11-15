// ========================================
// MODULES/ORDINI/CARRELLO.JS
// Gestione Carrello
// ========================================

const CarrelloModule = {
    // ========================================
    // AGGIUNGI AL CARRELLO
    // ========================================
    aggiungi(id, nome, prezzo) {
        const carrello = State.getCarrello();
        const esistente = carrello.find(item => item.id === id);
        
        if (esistente) {
            esistente.quantita++;
        } else {
            carrello.push({
                id: id,
                nome: nome,
                prezzo: prezzo,
                quantita: 1
            });
        }
        
        this.render();
        TotaliModule.aggiorna();
        
        console.log('➕ Aggiunto:', nome);
    },
    
    // ========================================
    // RIMUOVI DAL CARRELLO
    // ========================================
    rimuovi(id) {
        const carrello = State.getCarrello();
        const index = carrello.findIndex(item => item.id === id);
        
        if (index > -1) {
            carrello.splice(index, 1);
            this.render();
            TotaliModule.aggiorna();
        }
    },
    
    // ========================================
    // MODIFICA QUANTITÀ
    // ========================================
    modificaQuantita(id, delta) {
        const carrello = State.getCarrello();
        const item = carrello.find(item => item.id === id);
        
        if (!item) return;
        
        item.quantita += delta;
        
        if (item.quantita <= 0) {
            this.rimuovi(id);
        } else {
            this.render();
            TotaliModule.aggiorna();
        }
    },
    
    // ========================================
    // RENDER CARRELLO
    // ========================================
    render() {
        const container = document.getElementById('carrello-items');
        const carrello = State.getCarrello();
        
        if (carrello.length === 0) {
            container.innerHTML = `
                <div class="carrello-empty">
                    Nessun prodotto aggiunto.<br>
                    Seleziona una pizza dal menu rapido!
                </div>
            `;
            return;
        }
        
        const fragment = document.createDocumentFragment();
        
        carrello.forEach(item => {
            const div = Utils.createElement('div', 'carrello-item');
            const totaleItem = item.prezzo * item.quantita;
            
            div.innerHTML = `
                <div class="carrello-item-info">
                    <div class="carrello-item-nome">${item.nome}</div>
                    <div class="carrello-item-dettagli">€ ${Utils.formatMoney(item.prezzo)} × ${item.quantita}</div>
                </div>
                <div class="carrello-item-controls">
                    <div class="qty-controls">
                        <button class="qty-btn" onclick="CarrelloModule.modificaQuantita(${item.id}, -1)">−</button>
                        <span class="qty-value">${item.quantita}</span>
                        <button class="qty-btn" onclick="CarrelloModule.modificaQuantita(${item.id}, 1)">+</button>
                    </div>
                    <div class="carrello-item-prezzo">€ ${Utils.formatMoney(totaleItem)}</div>
                    <button class="btn-remove" onclick="CarrelloModule.rimuovi(${item.id})">🗑️</button>
                </div>
            `;
            
            fragment.appendChild(div);
        });
        
        container.innerHTML = '';
        container.appendChild(fragment);
    }
};

// Export per chiamate da HTML
window.CarrelloModule = CarrelloModule;

console.log('✅ CarrelloModule caricato');
