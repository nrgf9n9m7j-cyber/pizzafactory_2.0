// ========================================
// MODULES/ORDINI/TOTALI.JS
// Calcolo Totali
// ========================================

const TotaliModule = {
    // ========================================
    // AGGIORNA TOTALI
    // ========================================
    aggiorna() {
        const carrello = State.getCarrello();
        const subtotale = this.calcolaSubtotale(carrello);
        const sovrapprezzo = this.calcolaSovrapprezzo(subtotale);
        const totale = this.calcolaTotale(subtotale, sovrapprezzo);
        
        // Aggiorna UI
        document.getElementById('subtotale').textContent = Utils.formatMoney(subtotale);
        document.getElementById('sovrapprezzo').textContent = Utils.formatMoney(sovrapprezzo);
        document.getElementById('totale-finale').textContent = Utils.formatMoney(totale);
        document.getElementById('totale-sticky').textContent = Utils.formatMoney(totale);
        
        // Mostra/nascondi riga sovrapprezzo
        if (sovrapprezzo > 0) {
            Utils.show('sovrapprezzo-row');
        } else {
            Utils.hide('sovrapprezzo-row');
        }
    },
    
    // ========================================
    // CALCOLA SUBTOTALE
    // ========================================
    calcolaSubtotale(carrello) {
        return carrello.reduce((sum, item) => sum + (item.prezzo * item.quantita), 0);
    },
    
    // ========================================
    // CALCOLA SOVRAPPREZZO
    // ========================================
    calcolaSovrapprezzo(subtotale) {
        const tipo = State.getTipo();
        
        // Sovrapprezzo solo per consegna (<€15)
        if (tipo === 1 && subtotale > 0 && subtotale < 15) {
            return 2.00;
        }
        
        return 0;
    },
    
    // ========================================
    // CALCOLA TOTALE FINALE
    // ========================================
    calcolaTotale(subtotale, sovrapprezzo) {
        const totaleModificato = State.getTotaleModificato();
        
        // Se modificato manualmente, usa quello
        if (totaleModificato !== null) {
            return totaleModificato;
        }
        
        return subtotale + sovrapprezzo;
    },
    
    // ========================================
    // TOGGLE MODIFICA PREZZO
    // ========================================
    toggleModifica() {
        const displayRow = document.querySelector('.totale-row.modificabile');
        const inputRow = document.getElementById('input-modifica-row');
        
        Utils.hide(displayRow);
        Utils.show(inputRow);
        
        const totaleAttuale = document.getElementById('totale-finale').textContent;
        document.getElementById('totale-custom').value = totaleAttuale;
        document.getElementById('totale-custom').focus();
    },
    
    // ========================================
    // APPLICA MODIFICA
    // ========================================
    applicaModifica() {
        const nuovoTotale = parseFloat(document.getElementById('totale-custom').value);
        
        if (isNaN(nuovoTotale) || nuovoTotale < 0) {
            showAlert('Inserisci un importo valido', 'warning');
            return;
        }
        
        State.setTotaleModificato(nuovoTotale);
        this.aggiorna();
        this.annullaModifica();
    },
    
    // ========================================
    // ANNULLA MODIFICA
    // ========================================
    annullaModifica() {
        Utils.show(document.querySelector('.totale-row.modificabile'));
        Utils.hide('input-modifica-row');
    }
};

// Export per chiamate da HTML
window.toggleModificaPrezzo = () => TotaliModule.toggleModifica();
window.applicaModifica = () => TotaliModule.applicaModifica();
window.annullaModifica = () => TotaliModule.annullaModifica();

console.log('✅ TotaliModule caricato');
