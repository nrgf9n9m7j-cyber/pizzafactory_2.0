console.log('✅ Tab Ordini pronto');

const OrdiniModule = {
    init() {
        console.log('🧾 OrdiniModule inizializzato');

        // Inizializza ClienteModule se disponibile
        if (window.ClienteModule && typeof ClienteModule.init === 'function') {
            ClienteModule.init();
        }

        // Attendi il caricamento del modulo pizze
        this.attendiTopPizze();

        // Ascolta gli hook provenienti da MacroDroid o simulazioni
        window.addEventListener('hookChiamata', (event) => {
            const numero = event.detail?.numero;
            console.log('[HOOK] Numero ricevuto:', numero);

            if (window.ClienteModule && typeof ClienteModule.hookCerca === 'function') {
                ClienteModule.hookCerca(numero);
            } else {
                console.warn('[HOOK] ClienteModule non disponibile');
            }
        });
    },

attendiTopPizze(tentativo = 0) {
    console.log(`[TENTATIVO ${tentativo}] Verifica PizzeModule...`);
    
    if (window.PizzeModule) {
        console.log('✅ PizzeModule trovato:', typeof PizzeModule.renderTopPizze);
        
        if (typeof PizzeModule.renderTopPizze === 'function') {
            try {
                PizzeModule.renderTopPizze();
                console.log('🍕 Top 8 pizze ricaricate con successo');
                return; // IMPORTANTE: Esce dopo successo
            } catch (err) {
                console.error('❌ Errore nel rendering delle top pizze:', err);
            }
        }
    }
    
    if (tentativo < 10) {
        setTimeout(() => this.attendiTopPizze(tentativo + 1), 500);
    } else {
        console.warn('⚠️ PizzeModule non disponibile dopo 10 tentativi');
        console.log('PizzeModule stato:', window.PizzeModule);
    }
}
};

// =======================================================
// Simulazione hook (solo per test manuale da console)
// =======================================================
window.simulaHook = (numero) => {
    console.log(`[SIMULAZIONE HOOK] chiamata_in_arrivo | Numero: ${numero}`);
    const evento = new CustomEvent('hookChiamata', { detail: { numero } });
    window.dispatchEvent(evento);
};

// =======================================================
// Avvio automatico del modulo
// =======================================================
document.addEventListener('DOMContentLoaded', () => {
    OrdiniModule.init();
});
