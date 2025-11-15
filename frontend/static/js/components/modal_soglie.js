/* ============================================
   MODAL SOGLIE SCORTE - JavaScript
   File: frontend/static/js/components/modal_soglie.js
   
   Gestione soglie minime per prodotti con scorte
   ============================================ */

const ModalSoglie = {
    prodotti: [],
    prodottiModificati: new Map(),
    categoriaFiltro: 'tutti',
    
    // ========================================
    // INIT
    // ========================================
    async init() {
        console.log('⚙️ Init Modal Soglie...');
        await this.caricaProdotti();
    },
    
    // ========================================
    // CARICA PRODOTTI CON SCORTE
    // Query: SELECT * FROM Prodotti WHERE Gestione_Scorte = 1 ORDER BY Categoria, Nome_Prodotto
    // ========================================
    async caricaProdotti() {
        try {
            const response = await fetch('/api/prodotti/con-scorte');
            
            if (!response.ok) {
                throw new Error('Errore caricamento prodotti');
            }
            
            this.prodotti = await response.json();
            console.log(`✅ Caricati ${this.prodotti.length} prodotti con scorte`);
            
        } catch (error) {
            console.error('❌ Errore caricamento prodotti:', error);
        }
    },
    
    // ========================================
    // APRI MODAL
    // ========================================
    async apri() {
        const modal = document.getElementById('modal-soglie');
        modal.style.display = 'flex';
        
        // Ricarica prodotti
        await this.caricaProdotti();
        
        // Renderizza tabella
        this.renderTabella();
        
        // Previeni scroll body
        document.body.style.overflow = 'hidden';
    },
    
    // ========================================
    // CHIUDI MODAL
    // ========================================
    chiudi() {
        // Controlla modifiche non salvate
        if (this.prodottiModificati.size > 0) {
            const conferma = confirm('Ci sono modifiche non salvate. Vuoi chiudere comunque?');
            if (!conferma) return;
        }
        
        const modal = document.getElementById('modal-soglie');
        modal.style.display = 'none';
        
        // Reset
        this.prodottiModificati.clear();
        this.categoriaFiltro = 'tutti';
        
        // Ripristina scroll body
        document.body.style.overflow = 'auto';
    },
    
    // ========================================
    // FILTRA PER CATEGORIA
    // ========================================
    filtra(categoria) {
        this.categoriaFiltro = categoria;
        
        // Aggiorna bottoni
        document.querySelectorAll('.btn-filtro').forEach(btn => {
            btn.classList.remove('active');
        });
        event.target.classList.add('active');
        
        // Ri-renderizza
        this.renderTabella();
    },
    
    // ========================================
    // CERCA PRODOTTO
    // ========================================
    cercaProdotto(query) {
        const tbody = document.getElementById('tbody-soglie');
        const righe = tbody.querySelectorAll('tr');
        
        query = query.toLowerCase();
        
        righe.forEach(riga => {
            const nome = riga.querySelector('.nome-prodotto')?.textContent.toLowerCase() || '';
            
            if (nome.includes(query)) {
                riga.style.display = '';
            } else {
                riga.style.display = 'none';
            }
        });
    },
    
    // ========================================
    // RENDER TABELLA
    // ========================================
    renderTabella() {
        const tbody = document.getElementById('tbody-soglie');
        
        // Filtra prodotti
        let prodottiFiltrati = this.prodotti;
        
        if (this.categoriaFiltro !== 'tutti') {
            prodottiFiltrati = this.prodotti.filter(p => p.Categoria === this.categoriaFiltro);
        }
        
        // Se non ci sono prodotti
        if (prodottiFiltrati.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="6" style="text-align: center; padding: 40px;">
                        😔 Nessun prodotto con gestione scorte attiva
                    </td>
                </tr>
            `;
            return;
        }
        
        // Crea righe tabella
        tbody.innerHTML = prodottiFiltrati.map(prodotto => {
            const qta = prodotto.Quantita_Disponibile || 0;
            const soglia = prodotto.Soglia_Minima || 5;
            
            // Determina status
            let badgeClass = 'ok';
            let badgeText = '✅ OK';
            
            if (qta === 0) {
                badgeClass = 'esaurite';
                badgeText = '❌ Esaurite';
            } else if (qta <= soglia) {
                badgeClass = 'basse';
                badgeText = '⚠️ Basse';
            }
            
            return `
                <tr data-id="${prodotto.ID_Prodotto}">
                    <td>
                        <strong class="nome-prodotto">${prodotto.Nome_Prodotto}</strong>
                    </td>
                    <td>${prodotto.Categoria || '-'}</td>
                    <td>
                        <span class="badge-status ${badgeClass}">
                            ${qta} ${prodotto.Unita_Misura || 'pz'}
                        </span>
                    </td>
                    <td>
                        <input type="number" 
                               class="input-soglia" 
                               value="${soglia}"
                               min="1"
                               data-id="${prodotto.ID_Prodotto}"
                               data-valore-originale="${soglia}"
                               onchange="ModalSoglie.modificaSoglia(${prodotto.ID_Prodotto}, this.value)">
                    </td>
                    <td>
                        <select class="select-unita" 
                                data-id="${prodotto.ID_Prodotto}"
                                data-valore-originale="${prodotto.Unita_Misura || 'pz'}"
                                onchange="ModalSoglie.modificaUnita(${prodotto.ID_Prodotto}, this.value)">
                            <option value="pz" ${prodotto.Unita_Misura === 'pz' ? 'selected' : ''}>Pezzi</option>
                            <option value="lt" ${prodotto.Unita_Misura === 'lt' ? 'selected' : ''}>Litri</option>
                            <option value="kg" ${prodotto.Unita_Misura === 'kg' ? 'selected' : ''}>Kg</option>
                            <option value="conf" ${prodotto.Unita_Misura === 'conf' ? 'selected' : ''}>Confezioni</option>
                        </select>
                    </td>
                    <td>
                        <button class="btn-azione btn-reset" 
                                onclick="ModalSoglie.resetProdotto(${prodotto.ID_Prodotto})">
                            ↺ Reset
                        </button>
                    </td>
                </tr>
            `;
        }).join('');
    },
    
    // ========================================
    // MODIFICA SOGLIA
    // ========================================
    modificaSoglia(idProdotto, nuovaSoglia) {
        const input = document.querySelector(`.input-soglia[data-id="${idProdotto}"]`);
        const valoreOriginale = parseInt(input.dataset.valoreOriginale);
        
        nuovaSoglia = parseInt(nuovaSoglia);
        
        // Segna come modificato
        if (nuovaSoglia !== valoreOriginale) {
            input.classList.add('modificato');
            
            // Salva modifica
            if (!this.prodottiModificati.has(idProdotto)) {
                this.prodottiModificati.set(idProdotto, {});
            }
            this.prodottiModificati.get(idProdotto).Soglia_Minima = nuovaSoglia;
            
        } else {
            input.classList.remove('modificato');
            
            // Rimuovi modifica se torna al valore originale
            if (this.prodottiModificati.has(idProdotto)) {
                delete this.prodottiModificati.get(idProdotto).Soglia_Minima;
                if (Object.keys(this.prodottiModificati.get(idProdotto)).length === 0) {
                    this.prodottiModificati.delete(idProdotto);
                }
            }
        }
        
        console.log('📝 Soglia modificata:', idProdotto, nuovaSoglia);
    },
    
    // ========================================
    // MODIFICA UNITÀ MISURA
    // ========================================
    modificaUnita(idProdotto, nuovaUnita) {
        const select = document.querySelector(`.select-unita[data-id="${idProdotto}"]`);
        const valoreOriginale = select.dataset.valoreOriginale;
        
        // Salva modifica
        if (nuovaUnita !== valoreOriginale) {
            if (!this.prodottiModificati.has(idProdotto)) {
                this.prodottiModificati.set(idProdotto, {});
            }
            this.prodottiModificati.get(idProdotto).Unita_Misura = nuovaUnita;
        } else {
            if (this.prodottiModificati.has(idProdotto)) {
                delete this.prodottiModificati.get(idProdotto).Unita_Misura;
                if (Object.keys(this.prodottiModificati.get(idProdotto)).length === 0) {
                    this.prodottiModificati.delete(idProdotto);
                }
            }
        }
        
        console.log('📝 Unità modificata:', idProdotto, nuovaUnita);
    },
    
    // ========================================
    // RESET PRODOTTO
    // ========================================
    resetProdotto(idProdotto) {
        const input = document.querySelector(`.input-soglia[data-id="${idProdotto}"]`);
        const select = document.querySelector(`.select-unita[data-id="${idProdotto}"]`);
        
        // Ripristina valori originali
        input.value = input.dataset.valoreOriginale;
        select.value = select.dataset.valoreOriginale;
        
        input.classList.remove('modificato');
        
        // Rimuovi da modificati
        this.prodottiModificati.delete(idProdotto);
        
        console.log('↺ Prodotto ripristinato:', idProdotto);
    },
    
    // ========================================
    // SALVA TUTTE LE MODIFICHE
    // ========================================
    async salvaTutto() {
        if (this.prodottiModificati.size === 0) {
            alert('ℹ️ Nessuna modifica da salvare');
            return;
        }
        
        console.log('💾 Salvataggio modifiche...', this.prodottiModificati);
        
        try {
            // Converti Map in array per invio
            const modifiche = Array.from(this.prodottiModificati.entries()).map(([id, dati]) => ({
                ID_Prodotto: id,
                ...dati
            }));
            
            const response = await fetch('/api/prodotti/aggiorna-soglie', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ modifiche })
            });
            
            if (!response.ok) {
                throw new Error('Errore salvataggio');
            }
            
            const result = await response.json();
            
            alert(`✅ Salvate ${result.aggiornati} modifiche con successo!`);
            
            // Reset
            this.prodottiModificati.clear();
            
            // Ricarica e chiudi
            await this.caricaProdotti();
            this.chiudi();
            
        } catch (error) {
            console.error('❌ Errore salvataggio:', error);
            alert('❌ Errore durante il salvataggio. Riprova.');
        }
    }
};

// ========================================
// INIT AL CARICAMENTO
// ========================================
document.addEventListener('DOMContentLoaded', () => {
    ModalSoglie.init();
});
