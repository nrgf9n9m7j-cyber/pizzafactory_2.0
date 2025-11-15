// ========================================
// MODULES/ORDINI/FORM.JS
// Gestione Form e Conferma Ordine
// ========================================

const FormModule = {
    // ========================================
    // SELEZIONA TIPO ORDINE
    // ========================================
    selectTipo(tipo, element) {
        State.setTipo(tipo);
        
        // UI: rimuovi selected da tutti
        document.querySelectorAll('.tipo-card').forEach(card => {
            card.classList.remove('selected');
        });
        element.classList.add('selected');
        
        // Nascondi scelta tipo
        Utils.hide('scelta-tipo');
        
        // Mostra main content
        Utils.show('main-content-ordine');
        
        // Mostra form corretto
        this.mostraFormTipo(tipo);
        
        // Precompila se c'è cliente
        ClienteModule.precompilaForm(tipo);
        
        // Imposta orario default
        this.impostaOrarioDefault();
        
        console.log('✅ Tipo ordine:', tipo);
    },
    
    // ========================================
    // MOSTRA FORM TIPO
    // ========================================
    mostraFormTipo(tipo) {
        // Nascondi tutti
        document.querySelectorAll('.form-tipo').forEach(form => {
            Utils.hide(form);
        });
        
        // Mostra quello giusto
        if (tipo === 1) Utils.show('form-consegna');
        else if (tipo === 2) Utils.show('form-ritiro');
        else if (tipo === 3) Utils.show('form-tavolo');
    },
    
    // ========================================
    // IMPOSTA ORARIO DEFAULT
    // ========================================
    impostaOrarioDefault() {
        const now = new Date();
        now.setMinutes(now.getMinutes() + 30); // +30 min
        const timeStr = Utils.formatTime(now);
        
        const orarioConsegna = document.getElementById('orario-consegna');
        const orarioRitiro = document.getElementById('orario-ritiro');
        
        if (orarioConsegna) orarioConsegna.value = timeStr;
        if (orarioRitiro) orarioRitiro.value = timeStr;
    },
    
    // ========================================
    // CONFERMA ORDINE
    // ========================================
    async conferma() {
        // Validazione base
        if (State.getCarrello().length === 0) {
            showAlert('Aggiungi almeno un prodotto', 'warning');
            return;
        }
        
        if (!State.getTipo()) {
            showAlert('Seleziona il tipo di ordine', 'warning');
            return;
        }
        
        // Raccogli dati
        const ordineData = this.raccogliDati();
        if (!ordineData) return;
        
        try {
            const result = await API.creaOrdine(ordineData);
            
            if (result.success) {
                showAlert('✅ Ordine creato con successo!', 'success');
                this.reset();
            } else {
                showAlert('Errore: ' + (result.error || 'Sconosciuto'), 'error');
            }
        } catch (error) {
            console.error('Errore conferma ordine:', error);
            showAlert('Errore di connessione', 'error');
        }
    },
    
    // ========================================
    // RACCOGLI DATI ORDINE
    // ========================================
    raccogliDati() {
        const tipo = State.getTipo();
        const cliente = State.getCliente();
        const carrello = State.getCarrello();
        const totale = parseFloat(document.getElementById('totale-finale').textContent);
        
        const ordine = {
            id_cliente: cliente?.ID_Cliente || null,
            id_tipo: tipo,
            totale_ordine: totale,
            // ✅ FIXED: Rimosso is_bibita, tutto è prodotto!
            prodotti: carrello.map(item => ({
                id_prodotto: item.id,
                quantita: item.quantita,
                prezzo_unitario: item.prezzo
                // Pizze possono avere extra_ingredienti e opzioni
                // Bibite hanno solo id, quantità e prezzo
            }))
        };
        
        // Dati specifici per tipo
        if (tipo === 1) { // Consegna
            const cognome = document.getElementById('cognome-consegna').value;
            const telefono = document.getElementById('telefono-consegna').value;
            const indirizzo = document.getElementById('indirizzo-consegna').value;
            const orario = document.getElementById('orario-consegna').value;
            
            if (!cognome || !telefono || !indirizzo) {
                showAlert('Compila tutti i campi obbligatori', 'warning');
                return null;
            }
            
            ordine.cognome = cognome;
            ordine.nome = document.getElementById('nome-consegna').value;
            ordine.telefono_consegna = telefono;
            ordine.indirizzo_consegna = indirizzo;
            ordine.civico_consegna = document.getElementById('civico-consegna').value;
            ordine.citta_consegna = document.getElementById('citta-consegna').value;
            ordine.orario_consegna = orario;
            ordine.note_ordine = document.getElementById('note-consegna').value;
            
        } else if (tipo === 2) { // Ritiro
            const cognome = document.getElementById('cognome-ritiro').value;
            const orario = document.getElementById('orario-ritiro').value;
            
            if (!cognome) {
                showAlert('Inserisci almeno il cognome', 'warning');
                return null;
            }
            
            ordine.cognome = cognome;
            ordine.telefono_consegna = document.getElementById('telefono-ritiro').value;
            ordine.orario_ritiro = orario;
            ordine.note_ordine = document.getElementById('note-ritiro').value;
            
        } else if (tipo === 3) { // Tavolo
            const tavolo = document.getElementById('numero-tavolo').value;
            
            if (!tavolo) {
                showAlert('Inserisci il numero tavolo', 'warning');
                return null;
            }
            
            ordine.numero_tavolo = parseInt(tavolo);
            ordine.note_ordine = document.getElementById('note-tavolo').value;
        }
        
        return ordine;
    },
    
    // ========================================
    // RESET ORDINE
    // ========================================
    reset() {
        State.resetOrdine();
        
        // Reset UI
        Utils.hide('cliente-recap');
        Utils.show('scelta-tipo');
        Utils.hide('main-content-ordine');
        
        // Reset carrello e totali
        CarrelloModule.render();
        TotaliModule.aggiorna();
        
        // Reset form
        document.querySelectorAll('input[type="text"], input[type="tel"], input[type="number"], textarea').forEach(input => {
            input.value = '';
        });
        
        // Reset cards tipo
        document.querySelectorAll('.tipo-card').forEach(card => {
            card.classList.remove('selected');
        });
    }
};

// Export per chiamate da HTML
window.selectTipoOrdine = (tipo, element) => FormModule.selectTipo(tipo, element);
window.confermaOrdine = () => FormModule.conferma();
window.openMenuCompleto = () => showAlert('Menu Completo in sviluppo', 'info');
window.openBibite = () => MenuBibite.apri();  // ✅ Apre modal bibite

console.log('✅ FormModule caricato (FIXED - rimosso is_bibita)');
