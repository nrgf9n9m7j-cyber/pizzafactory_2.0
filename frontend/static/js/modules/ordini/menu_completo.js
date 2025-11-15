// ========================================
// MODULES/ORDINI/MENU_COMPLETO.JS
// Modal menu completo - STILE 1.0
// Click diretto su card per aggiungere
// ========================================

const MenuCompletoModule = {
    pizze: [],
    filtroCorrente: 'tutte',
    formatoSelezionato: 'pizza', // Formato corrente selezionato
    
    // ========================================
    // CAMBIA FORMATO PIZZA
    // ========================================
    cambiaFormato(formato) {
        console.log('📐 Cambio formato:', formato);
        
        this.formatoSelezionato = formato;
        
        // Aggiorna bottoni attivi
        document.querySelectorAll('.btn-formato-menu').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-formato="${formato}"]`).classList.add('active');
        
        // Se seleziono Farinata, cambio categoria automaticamente
        if (formato === 'farinata') {
            // TODO: Implementare caricamento prodotti farinata
            alert('Farinata in arrivo! Per ora seleziona Classica.');
            this.cambiaFormato('pizza');
            return;
        }
        
        // Re-render con nuovi prezzi
        this.render();
        
        console.log('✅ Formato aggiornato:', formato);
    },
    
    // ========================================
    // CALCOLA PREZZO CON FORMATO
    // ========================================
    calcolaPrezzo(prezzoBase, formato) {
        const prezzo = parseFloat(prezzoBase);
        
        switch(formato) {
            case 'baby':
                // Baby: prezzo base - €2.00
                return Math.max(prezzo - 2.00, 0);
            
            case 'maxi':
                // Maxi: (prezzo base × 2.5) arrotondato per eccesso a €0.50
                const prezzoMaxi = prezzo * 2.5;
                return Math.ceil(prezzoMaxi * 2) / 2; // Arrotonda a 0.50
            
            case 'tegamino':
                // Tegamino: prezzo base + €1.00
                return prezzo + 1.00;
            
            case 'pizza':
            default:
                // Classica: prezzo base
                return prezzo;
        }
    },
    
    // ========================================
    // APRI MODAL
    // ========================================
    async apri() {
        try {
            console.log('📋 Apertura menu completo...');
            
            // Carica pizze se non già caricate
            if (this.pizze.length === 0) {
                await this.caricaPizze();
            }
            
            // Render
            this.render();
            
            // Mostra modal
            document.getElementById('modal-menu-completo').style.display = 'flex';
            
            console.log('✅ Menu completo aperto:', this.pizze.length, 'pizze');
            
        } catch (error) {
            console.error('❌ Errore apertura menu:', error);
            alert('Errore caricamento menu pizze');
        }
    },
    
    // ========================================
    // CHIUDI MODAL
    // ========================================
    chiudi() {
        document.getElementById('modal-menu-completo').style.display = 'none';
        console.log('📋 Menu completo chiuso');
    },
    
    // ========================================
    // CARICA PIZZE DA API
    // ========================================
    async caricaPizze() {
        try {
            console.log('🔄 Caricamento pizze da API...');
            
            const response = await fetch('/api/prodotti?formato=pizza');
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            
            this.pizze = await response.json();
            
            console.log('✅ Caricate', this.pizze.length, 'pizze');
            
            // Aggiorna badge contatori
            this.aggiornaBadge();
            
        } catch (error) {
            console.error('❌ Errore caricamento pizze:', error);
            throw error;
        }
    },
    
    // ========================================
    // AGGIORNA BADGE CONTATORI
    // ========================================
    aggiornaBadge() {
        const counts = {
            tutte: this.pizze.length,
            Rosse: this.pizze.filter(p => p.Categoria === 'Rosse').length,
            Bianche: this.pizze.filter(p => p.Categoria === 'Bianche').length,
            Vegetariane: this.pizze.filter(p => p.Categoria === 'Vegetariane').length,
            Gourmet: this.pizze.filter(p => p.Categoria === 'Gourmet').length
        };
        
        document.getElementById('badge-tutte').textContent = counts.tutte;
        document.getElementById('badge-rosse').textContent = counts.Rosse;
        document.getElementById('badge-bianche').textContent = counts.Bianche;
        document.getElementById('badge-vegetariane').textContent = counts.Vegetariane;
        document.getElementById('badge-gourmet').textContent = counts.Gourmet;
    },
    
    // ========================================
    // FILTRA PER CATEGORIA
    // ========================================
    filtra(categoria) {
        this.filtroCorrente = categoria;
        
        // Aggiorna bottoni attivi
        document.querySelectorAll('.filtro-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-categoria="${categoria}"]`).classList.add('active');
        
        // Re-render
        this.render();
        
        console.log('🔍 Filtro applicato:', categoria);
    },
    
    // ========================================
    // RENDER GRID PIZZE
    // ========================================
    render() {
        const container = document.getElementById('menu-pizze-grid');
        
        // Filtra pizze
        let pizzeFiltrate = this.pizze;
        if (this.filtroCorrente !== 'tutte') {
            pizzeFiltrate = this.pizze.filter(p => p.Categoria === this.filtroCorrente);
        }
        
        // Empty state
        if (pizzeFiltrate.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">🍕</div>
                    <div class="empty-state-text">Nessuna pizza trovata in questa categoria</div>
                </div>
            `;
            return;
        }
        
        // Render cards
        const fragment = document.createDocumentFragment();
        
        pizzeFiltrate.forEach(pizza => {
            const card = this.creaCard(pizza);
            fragment.appendChild(card);
        });
        
        container.innerHTML = '';
        container.appendChild(fragment);
        
        console.log('✅ Renderizzate', pizzeFiltrate.length, 'pizze');
    },
    
    // ========================================
    // CREA CARD SINGOLA PIZZA (STILE 1.0 + BOTTONI RAPIDI)
    // ========================================
    creaCard(pizza) {
        const card = document.createElement('div');
        card.className = 'pizza-card-full';
        card.dataset.id = pizza.ID_Prodotto;
        
        // Calcola prezzo con formato selezionato
        const prezzoFinale = this.calcolaPrezzo(pizza.Prezzo_Base, this.formatoSelezionato);
        
        // Click handler su tutta la card
        card.addEventListener('click', (e) => this.handleCardClick(e, pizza, prezzoFinale));
        
        // Allergeni (opzionale)
        const allergeni = pizza.Allergeni ? pizza.Allergeni.split(',').map(a => a.trim()) : [];
        const allergeniHTML = allergeni.length > 0 ? `
            <div class="pizza-allergeni">
                ${allergeni.map(a => `<span class="allergene-tag">${a}</span>`).join('')}
            </div>
        ` : '';
        
        // Badge formato (se non è classica)
        let badgeFormato = '';
        if (this.formatoSelezionato !== 'pizza') {
            const nomiFormato = {
                'baby': 'Baby',
                'maxi': 'Maxi',
                'tegamino': 'Tegamino',
                'farinata': 'Farinata'
            };
            badgeFormato = `<span class="badge-formato">${nomiFormato[this.formatoSelezionato]}</span>`;
        }
        
        card.innerHTML = `
            <div class="pizza-name">
                ${pizza.Nome_Prodotto}
                ${badgeFormato}
            </div>
            <span class="pizza-categoria">${pizza.Categoria || 'Classica'}</span>
            
            <div class="pizza-ingredienti">${pizza.Ingredienti || 'Pizza speciale'}</div>
            
            ${allergeniHTML}
            
            <div class="pizza-card-footer">
                <!-- Prima riga: 4 bottoni rapidi -->
                <div class="pizza-actions-row">
                    <button class="btn-action-icon btn-no-mozza" 
                            data-action="no-mozza"
                            title="Senza mozzarella">
                        <span class="icon-with-slash">🧀</span>
                    </button>
                    <button class="btn-action-icon btn-no-pomodoro" 
                            data-action="no-pomodoro"
                            title="Senza pomodoro">
                        <span class="icon-with-slash">🍅</span>
                    </button>
                    <button class="btn-action-icon btn-tagliata" 
                            data-action="tagliata"
                            title="Tagliata">
                        🔪
                    </button>
                    <button class="btn-action-icon btn-ben-cotta" 
                            data-action="ben-cotta"
                            title="Ben cotta">
                        🔥
                    </button>
                </div>
                
                <!-- Seconda riga: Prezzo + Ingranaggio -->
                <div class="pizza-price-row">
                    <div class="pizza-prezzo">€${prezzoFinale.toFixed(2)}</div>
                    <button class="btn-action-icon btn-personalizza-icon" 
                            data-action="personalizza"
                            title="Personalizza">
                        ⚙️
                    </button>
                </div>
            </div>
        `;
        
        return card;
    },
    
    // ========================================
    // GESTISCE CLICK SU CARD (STILE 1.0 + BOTTONI RAPIDI)
    // ========================================
    handleCardClick(event, pizza, prezzoFinale) {
        // Verifica se è un bottone azione
        const action = event.target.dataset.action || 
                      event.target.closest('[data-action]')?.dataset.action;
        
        if (action) {
            event.stopPropagation();
            
            switch(action) {
                case 'tagliata':
                    this.aggiungiConModifica(pizza, prezzoFinale, '🔪 Tagliata');
                    break;
                case 'ben-cotta':
                    this.aggiungiConModifica(pizza, prezzoFinale, '🔥 Ben cotta');
                    break;
                case 'no-mozza':
                    this.aggiungiConModifica(pizza, prezzoFinale, '🧀̷ Senza mozzarella');
                    break;
                case 'no-pomodoro':
                    this.aggiungiConModifica(pizza, prezzoFinale, '🍅̷ Senza pomodoro');
                    break;
                case 'personalizza':
                    this.personalizza(pizza);
                    break;
            }
            return;
        }
        
        // Altrimenti → aggiunta rapida normale
        this.aggiungiRapido(pizza, prezzoFinale, event.currentTarget);
    },
    
    // ========================================
    // AGGIUNGI CON MODIFICA RAPIDA
    // ========================================
    aggiungiConModifica(pizza, prezzoFinale, modifica) {
        if (typeof CarrelloModule !== 'undefined' && CarrelloModule.aggiungi) {
            // Crea nome con modifica
            const nomeCompleto = `${pizza.Nome_Prodotto} ${modifica}`;
            
            // Aggiungi al carrello con formato e modifica
            CarrelloModule.aggiungi(
                pizza.ID_Prodotto,
                nomeCompleto,
                prezzoFinale,
                {
                    formato: this.formatoSelezionato,
                    modifica: modifica
                }
            );
            
            console.log('✅ Pizza aggiunta con modifica:', nomeCompleto);
            this.mostraFeedback(`${nomeCompleto} aggiunta!`);
        } else {
            console.error('CarrelloModule non disponibile');
        }
    },
    
    // ========================================
    // AGGIUNTA RAPIDA (senza modifiche)
    // ========================================
    aggiungiRapido(pizza, prezzoFinale, cardElement) {
        // Aggiungi al carrello con formato
        if (typeof CarrelloModule !== 'undefined' && CarrelloModule.aggiungi) {
            CarrelloModule.aggiungi(
                pizza.ID_Prodotto,
                pizza.Nome_Prodotto,
                prezzoFinale,
                {
                    formato: this.formatoSelezionato
                }
            );
            
            console.log('✅ Pizza aggiunta rapidamente:', pizza.Nome_Prodotto, `(${this.formatoSelezionato})`);
            
            // Feedback visivo (scala card)
            cardElement.style.transform = 'scale(1.1)';
            setTimeout(() => {
                cardElement.style.transform = '';
            }, 200);
            
            // Toast notification
            this.mostraFeedback(`${pizza.Nome_Prodotto} aggiunta al carrello!`);
        } else {
            console.error('CarrelloModule non disponibile');
        }
    },
    
    // ========================================
    // PERSONALIZZA (apre modal personalizzazione)
    // ========================================
    personalizza(pizza) {
        console.log('⚙️ Personalizzazione pizza:', pizza.Nome_Prodotto);
        
        // Chiudi questo modal
        this.chiudi();
        
        // Apri modal personalizzazione
        if (typeof PersonalizzazioneModule !== 'undefined' && PersonalizzazioneModule.apri) {
            PersonalizzazioneModule.apri(pizza);
        } else {
            console.warn('PersonalizzazioneModule non ancora implementato');
            alert(`Personalizzazione "${pizza.Nome_Prodotto}" in arrivo!\n\nPer ora la pizza verrà aggiunta senza modifiche.`);
            
            // Aggiungi senza personalizzazioni (temporaneo)
            if (typeof CarrelloModule !== 'undefined') {
                CarrelloModule.aggiungi(
                    pizza.ID_Prodotto,
                    pizza.Nome_Prodotto,
                    parseFloat(pizza.Prezzo_Base)
                );
            }
        }
    },
    
    // ========================================
    // FEEDBACK VISIVO (toast)
    // ========================================
    mostraFeedback(messaggio) {
        // Rimuovi toast precedente se esiste
        const vecchioToast = document.getElementById('menu-toast');
        if (vecchioToast) vecchioToast.remove();
        
        // Crea nuovo toast
        const toast = document.createElement('div');
        toast.id = 'menu-toast';
        toast.style.cssText = `
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: #28a745;
            color: white;
            padding: 15px 25px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            z-index: 10001;
            font-weight: 600;
            animation: slideIn 0.3s;
        `;
        toast.textContent = messaggio;
        
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.style.animation = 'slideOut 0.3s';
            setTimeout(() => toast.remove(), 300);
        }, 2000);
    }
};

// ========================================
// ANIMAZIONI CSS (inject se non esistono)
// ========================================
if (!document.getElementById('menu-animations')) {
    const style = document.createElement('style');
    style.id = 'menu-animations';
    style.textContent = `
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        @keyframes slideOut {
            from { transform: translateX(0); opacity: 1; }
            to { transform: translateX(100%); opacity: 0; }
        }
    `;
    document.head.appendChild(style);
}

// ========================================
// EXPORT GLOBALE
// ========================================
window.MenuCompletoModule = MenuCompletoModule;

// Funzione helper per aprire da HTML/altri moduli
window.apriMenuCompleto = () => MenuCompletoModule.apri();

console.log('✅ MenuCompletoModule caricato (Stile 1.0)');
