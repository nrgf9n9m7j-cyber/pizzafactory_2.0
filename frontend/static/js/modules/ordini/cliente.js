// ========================================
// MODULES/ORDINI/CLIENTE.JS
// Hook Telefonico + Ricerca Cliente
// ========================================

const ClienteModule = {
    searchTimeout: null,
    bloccatoHook: false,
    ultimoNumeroHook: null,
    ultimoTimestampRicerca: 0,
    RICERCA_MIN_DELAY: 50,

    /**
     * Controlla se una stringa è nel formato normalizzato (es. 349-0633281)
     */
    _isNormalizzato(query) {
        return /^\d{3}-\d{7}$/.test(query);
    },

    // ========================================
    // RICEVE NUMERO DA HOOK (Nuova Logica)
    // ========================================
    riceviDaHook(numero) {
        console.log("[CLIENTE] Ricevuto numero da hook:", numero);

        if (this.bloccatoHook) {
            console.log("[CLIENTE] Bloccato: in attesa di sblocco timeout.");
            return;
        }

        this.bloccatoHook = true;

        // 1. Normalizza il numero
        let pulito = numero.replace(/\D/g, "");
        if (pulito.startsWith("39")) pulito = pulito.slice(2);
        if (pulito.length === 10 && !this._isNormalizzato(pulito)) {
            pulito = pulito.slice(0, 3) + "-" + pulito.slice(3);
        }

        console.log("[CLIENTE] Numero normalizzato:", pulito);
        this.ultimoNumeroHook = pulito;

        const input = document.getElementById("search-cliente-hook");
        if (!input) {
            console.warn("[CLIENTE] Campo ricerca non trovato");
            this.bloccatoHook = false;
            return;
        }

        // 2. Imposta valore SENZA scatenare eventi 'input' che attiverebbero hookCerca
        input.removeEventListener("input", this._onInputListener);
        input.value = pulito;
        input.dispatchEvent(new Event("change"));
        input.addEventListener("input", this._onInputListener);
        
        input.focus(); 

        // 3. Avvia la ricerca automatica immediatamente
        console.log("[CLIENTE] Ricerca automatica avviata.");
        this.hookCerca(pulito); 

        // 4. Sblocca la logica dopo un breve ritardo
        setTimeout(() => {
            this.bloccatoHook = false;
            console.log("[CLIENTE] Blocco hook rimosso.");
        }, 800);
    },

    // ========================================
    // HOOK TELEFONICO - RICERCA
    // ========================================
    async hookCerca(query) {
        // Protezione dal loop (anti-spam/anti-ricorsione)
        const now = Date.now();
        if (now - this.ultimoTimestampRicerca < this.RICERCA_MIN_DELAY) {
            return;
        }
        this.ultimoTimestampRicerca = now;
        
        clearTimeout(this.searchTimeout);

        const resultsContainer = document.getElementById('search-results-hook');
        
        if (query.length < 2) {
            Utils.hide(resultsContainer);
            return;
        }
        
        this.searchTimeout = setTimeout(async () => {
            try {
                const clienti = await API.cercaClienti(query);
                
                if (clienti.length === 0) {
                    Utils.hide(resultsContainer);
                    return;
                }
                
                this.renderRisultati(clienti, resultsContainer);
                Utils.show(resultsContainer);
                
            } catch (error) {
                console.error('Errore ricerca clienti:', error);
                Utils.hide(resultsContainer);
            }
        }, 300);
    },
    
    // ========================================
    // RENDER RISULTATI - FIX: rimossi "//" che apparivano nella tendina
    // ========================================
    renderRisultati(clienti, container) {
        const fragment = document.createDocumentFragment();
        
        clienti.forEach(cliente => {
            const lifecycle = Utils.calcolaLifecycle(cliente.Totale_Ordini || 0);
            const rating = Utils.calcolaRating(cliente.Rating);
            
            const item = Utils.createElement('div', 'search-result-item');
            item.innerHTML = `
                <div class="search-result-nome">
                    ${lifecycle.emoji} ${rating.emoji} ${cliente.Cognome} ${cliente.Nome || ''}
                </div>
                <div class="search-result-dettagli">
                    📞 ${cliente.Telefono || 'N/A'} | 📦 ${cliente.Totale_Ordini || 0} ordini
                </div>
            `;
            
            item.onclick = () => this.seleziona(cliente);
            fragment.appendChild(item);
        });
        
        container.innerHTML = '';
        container.appendChild(fragment);
    },
    
    // ========================================
    // SELEZIONA CLIENTE
    // ========================================
    seleziona(cliente) {
        State.setCliente(cliente);
        
        Utils.hide('search-results-hook');
        document.getElementById('search-cliente-hook').value = '';
        
        this.mostraRecap(cliente);
        
        console.log('✅ Cliente selezionato:', cliente);
    },
    
    // ========================================
    // MOSTRA RECAP CLIENTE
    // ========================================
    mostraRecap(cliente) {
        const lifecycle = Utils.calcolaLifecycle(cliente.Totale_Ordini || 0);
        const rating = Utils.calcolaRating(cliente.Rating);
        
        document.getElementById('cliente-nome-recap').textContent =
            `${cliente.Cognome} ${cliente.Nome || ''}`;
        
        document.getElementById('cliente-lifecycle').textContent =
            `${lifecycle.emoji} ${lifecycle.status}`;
        
        document.getElementById('cliente-rating').textContent =
            `${rating.emoji} ${rating.descrizione}`;
        
        document.getElementById('cliente-telefono-recap').textContent =
            cliente.Telefono || 'N/A';
        
        document.getElementById('cliente-indirizzo-recap').textContent =
            `${cliente.Indirizzo || ''} ${cliente.Civico || ''}, ${cliente.Citta || ''}`;
        
        Utils.show('cliente-recap');
    },
    
    // ========================================
    // CAMBIA CLIENTE
    // ========================================
    cambia() {
        State.setCliente(null);
        Utils.hide('cliente-recap');
        document.getElementById('search-cliente-hook').focus();
    },
    
    // ========================================
    // PRECOMPILA FORM
    // ========================================
    precompilaForm(tipo) {
        const cliente = State.getCliente();
        if (!cliente) return;
        
        if (tipo === 1) { // Consegna
            document.getElementById('cognome-consegna').value = cliente.Cognome || '';
            document.getElementById('nome-consegna').value = cliente.Nome || '';
            document.getElementById('telefono-consegna').value = cliente.Telefono || '';
            document.getElementById('indirizzo-consegna').value = cliente.Indirizzo || '';
            document.getElementById('civico-consegna').value = cliente.Civico || '';
            document.getElementById('citta-consegna').value = cliente.Citta || 'Chieri';
        } else if (tipo === 2) { // Ritiro
            document.getElementById('cognome-ritiro').value = cliente.Cognome || '';
            document.getElementById('telefono-ritiro').value = cliente.Telefono || '';
        }
    },

    // ========================================
    // INIT LISTENER
    // ========================================
    init() {
        const input = document.getElementById("search-cliente-hook");
        if (!input) return;
        this._onInputListener = (e) => this.hookCerca(e.target.value);
        input.addEventListener("input", this._onInputListener);
    }
};

// Export funzioni globali
window.ClienteModule = ClienteModule;
window.hookCercaCliente = (query) => ClienteModule.hookCerca(query); 
window.cambiaCliente = () => ClienteModule.cambia();

// Inizializzazione
document.addEventListener("DOMContentLoaded", () => ClienteModule.init());

console.log('✅ ClienteModule caricato (FIXED - no più "//" nella tendina)');
