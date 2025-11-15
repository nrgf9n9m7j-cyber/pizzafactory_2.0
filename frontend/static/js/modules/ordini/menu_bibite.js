/* ============================================
   MENU BIBITE - JavaScript
   File: frontend/static/js/modules/ordini/menu_bibite.js
   
   Gestione modal menu bibite con filtri e aggiunta al carrello
   ============================================ */

const MenuBibite = {
    bibite: [],
    categoriaSelezionata: 'tutte',
    
    // ========================================
    // INIT - Carica bibite e prepara modal
    // ========================================
    async init() {
        console.log('🍹 Init Menu Bibite...');
        await this.caricaBibite();
    },
    
    // ========================================
    // CARICA BIBITE DAL SERVER
    // Query: SELECT * FROM Prodotti WHERE Tipo_Prodotto = 'bibita' AND Disponibile = 1
    // ========================================
    async caricaBibite() {
        try {
            const response = await fetch('/api/prodotti/bibite');
            
            if (!response.ok) {
                throw new Error('Errore caricamento bibite');
            }
            
            this.bibite = await response.json();
            console.log(`✅ Caricate ${this.bibite.length} bibite`);
            
        } catch (error) {
            console.error('❌ Errore caricamento bibite:', error);
            alert('Errore nel caricamento delle bibite. Riprova.');
        }
    },
    
    // ========================================
    // APRI MODAL
    // ========================================
    apri() {
        const modal = document.getElementById('modal-bibite');
        modal.style.display = 'flex';
        
        // Renderizza bibite
        this.renderBibite();
        
        // Previeni scroll body
        document.body.style.overflow = 'hidden';
    },
    
    // ========================================
    // CHIUDI MODAL
    // ========================================
    chiudi() {
        const modal = document.getElementById('modal-bibite');
        modal.style.display = 'none';
        
        // Ripristina scroll body
        document.body.style.overflow = 'auto';
    },
    
    // ========================================
    // FILTRA PER CATEGORIA
    // ========================================
    filtraCategoria(categoria) {
        this.categoriaSelezionata = categoria;
        
        // Aggiorna bottoni
        document.querySelectorAll('.btn-categoria').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`.btn-categoria[data-categoria="${categoria}"]`).classList.add('active');
        
        // Ri-renderizza
        this.renderBibite();
    },
    
    // ========================================
    // RENDER BIBITE NEL GRID
    // ========================================
    renderBibite() {
        const grid = document.getElementById('grid-bibite');
        
        // Filtra bibite
        let bibiteFiltrate = this.bibite;
        
        if (this.categoriaSelezionata !== 'tutte') {
            bibiteFiltrate = this.bibite.filter(b => b.Categoria === this.categoriaSelezionata);
        }
        
        // Se non ci sono bibite
        if (bibiteFiltrate.length === 0) {
            grid.innerHTML = `
                <div class="no-results">
                    <p>😕 Nessuna bibita trovata in questa categoria</p>
                </div>
            `;
            return;
        }
        
        // Crea HTML cards
        grid.innerHTML = bibiteFiltrate.map(bibita => {
            const disponibile = bibita.Disponibile === 1;
            const scorteBasse = bibita.Gestione_Scorte === 1 && 
                                bibita.Quantita_Disponibile <= bibita.Soglia_Minima &&
                                bibita.Quantita_Disponibile > 0;
            const esaurita = bibita.Gestione_Scorte === 1 && bibita.Quantita_Disponibile === 0;
            
            // Seleziona icona per categoria
            let icona = '🥤';
            if (bibita.Categoria === 'Acqua') icona = '💧';
            if (bibita.Categoria === 'Birre') icona = '🍺';
            
            return `
                <div class="card-bibita ${!disponibile || esaurita ? 'non-disponibile' : ''}" 
                     onclick="MenuBibite.aggiungiBibita(${bibita.ID_Prodotto})"
                     data-id="${bibita.ID_Prodotto}">
                    
                    ${scorteBasse ? '<div class="badge-scorte-basse">⚠️ Poche</div>' : ''}
                    ${esaurita ? '<div class="badge-scorte-basse">❌ Esaurita</div>' : ''}
                    
                    <div class="badge-categoria ${bibita.Categoria}">
                        ${bibita.Categoria}
                    </div>
                    
                    <div class="icona-bibita">${icona}</div>
                    
                    <div class="nome-bibita">${bibita.Nome_Prodotto}</div>
                    
                    ${bibita.Formato ? `<div class="formato-bibita">${bibita.Formato}</div>` : ''}
                    
                    <div class="prezzo-bibita">€${parseFloat(bibita.Prezzo_Base).toFixed(2)}</div>
                    
                    ${bibita.Gestione_Scorte === 1 ? `
                        <div class="info-scorte" style="font-size: 0.75em; color: #666; margin-top: 6px;">
                            Disponibili: ${bibita.Quantita_Disponibile || 0}
                        </div>
                    ` : ''}
                </div>
            `;
        }).join('');
    },
    
    // ========================================
    // AGGIUNGI BIBITA AL CARRELLO - FIX!
    // ========================================
    aggiungiBibita(idProdotto) {
        const bibita = this.bibite.find(b => b.ID_Prodotto === idProdotto);
        
        if (!bibita) {
            console.error('❌ Bibita non trovata');
            return;
        }
        
        // Controlla disponibilità
        if (bibita.Disponibile !== 1) {
            alert('⚠️ Questa bibita non è attualmente disponibile');
            return;
        }
        
        // Controlla scorte se gestite
        if (bibita.Gestione_Scorte === 1 && bibita.Quantita_Disponibile === 0) {
            alert('❌ Questa bibita è esaurita');
            return;
        }
        
        // ✅ FIX: Usa CarrelloModule invece di Carrello
        // ✅ FIX: Usa aggiungi(id, nome, prezzo) invece di aggiungiProdotto(oggetto)
        if (typeof CarrelloModule !== 'undefined') {
            CarrelloModule.aggiungi(
                bibita.ID_Prodotto,
                bibita.Nome_Prodotto,
                parseFloat(bibita.Prezzo_Base)
            );
            
            // Feedback visivo
            this.feedbackAggiunta(idProdotto);
            
            console.log('✅ Bibita aggiunta al carrello:', bibita.Nome_Prodotto);
        } else {
            console.error('❌ CarrelloModule non trovato');
            alert('⚠️ Errore: impossibile aggiungere al carrello');
        }
    },
    
    // ========================================
    // FEEDBACK VISIVO AGGIUNTA
    // ========================================
    feedbackAggiunta(idProdotto) {
        const card = document.querySelector(`.card-bibita[data-id="${idProdotto}"]`);
        
        if (!card) return;
        
        // Animazione flash verde
        card.style.background = '#d4edda';
        card.style.borderColor = '#71A894';
        
        setTimeout(() => {
            card.style.background = 'white';
            card.style.borderColor = '#e0e0e0';
        }, 500);
    }
};

// ========================================
// INIT AL CARICAMENTO PAGINA
// ========================================
document.addEventListener('DOMContentLoaded', () => {
    MenuBibite.init();
});

// ========================================
// CHIUDI MODAL CON ESC
// ========================================
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        MenuBibite.chiudi();
    }
});

// ========================================
// CHIUDI MODAL CLICCANDO FUORI
// ========================================
document.addEventListener('click', (e) => {
    const modal = document.getElementById('modal-bibite');
    if (e.target === modal) {
        MenuBibite.chiudi();
    }
});

console.log('✅ MenuBibite caricato (FIXED - chiamata corretta a CarrelloModule)');
