// =============================================================================
// MODULO GESTIONE FORMATI PIZZA
// =============================================================================

const FormatiModule = (() => {
    'use strict';

    // State
    let formatoSelezionato = 'classica';

    // =============================================================================
    // FUNZIONI CALCOLO PREZZI
    // =============================================================================

    /**
     * Calcola prezzo baby: prezzo base - €2.00
     */
    function calcolaPrezzoBaby(prezzoBase) {
        return Math.max(0, prezzoBase - 2.00);
    }

    /**
     * Calcola prezzo maxi: (prezzo base × 2.5) arrotondato per eccesso a .50 o .00
     */
    function calcolaPrezzoMaxi(prezzoBase) {
        const calcolato = prezzoBase * 2.5;
        return Math.ceil(calcolato * 2) / 2;
    }

    /**
     * Calcola prezzo tegamino: prezzo base + €1.00
     */
    function calcolaPrezzoTegamino(prezzoBase) {
        return prezzoBase + 1.00;
    }

    /**
     * Calcola prezzo in base al formato
     */
    function calcolaPrezzoConFormato(prezzoBase, formato) {
        switch (formato.toLowerCase()) {
            case 'baby':
                return calcolaPrezzoBaby(prezzoBase);
            case 'maxi':
                return calcolaPrezzoMaxi(prezzoBase);
            case 'tegamino':
                return calcolaPrezzoTegamino(prezzoBase);
            case 'classica':
            case 'pizza':
            default:
                return prezzoBase;
        }
    }

    // =============================================================================
    // GESTIONE FORMATO SELEZIONATO
    // =============================================================================

    /**
     * Cambia il formato selezionato
     */
    function cambiaFormato(formato) {
        formatoSelezionato = formato;
        aggiornaUIFormato();
        aggiornaPreziPizze();
    }

    /**
     * Aggiorna l'UI dei bottoni formato
     */
    function aggiornaUIFormato() {
        document.querySelectorAll('.btn-formato').forEach(btn => {
            if (btn.dataset.formato === formatoSelezionato) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });
    }

    /**
     * Aggiorna i prezzi di tutte le card pizza
     */
    function aggiornaPreziPizze() {
        document.querySelectorAll('.pizza-card').forEach(card => {
            const prezzoBase = parseFloat(card.dataset.prezzoBase);
            const prezzoFinale = calcolaPrezzoConFormato(prezzoBase, formatoSelezionato);
            
            const elementoPrezzo = card.querySelector('.prezzo');
            if (elementoPrezzo) {
                elementoPrezzo.textContent = `€${prezzoFinale.toFixed(2)}`;
            }
            
            // Aggiorna anche il badge formato se presente
            const badgeFormato = card.querySelector('.badge-formato');
            if (badgeFormato) {
                badgeFormato.textContent = formatoSelezionato.charAt(0).toUpperCase() + formatoSelezionato.slice(1);
            }
        });
    }

    // =============================================================================
    // INIZIALIZZAZIONE
    // =============================================================================

    function init() {
        // Aggiungi listener ai bottoni formato
        document.querySelectorAll('.btn-formato').forEach(btn => {
            btn.addEventListener('click', () => {
                const formato = btn.dataset.formato;
                cambiaFormato(formato);
            });
        });

        // Imposta formato di default
        aggiornaUIFormato();
    }

    // =============================================================================
    // API PUBBLICA
    // =============================================================================

    return {
        init,
        cambiaFormato,
        getFormatoSelezionato: () => formatoSelezionato,
        calcolaPrezzoConFormato,
        aggiornaPreziPizze
    };
})();

// Inizializza al caricamento del DOM
document.addEventListener('DOMContentLoaded', () => {
    if (document.querySelector('.btn-formato')) {
        FormatiModule.init();
    }
});
