// ======================================================
// ORDINI.JS - Gestione tab Ordini e Hook MacroDroid Live
// ======================================================

console.log("✅ Tab Ordini pronto");

// ========================================
// STATO INTERNO
// ========================================
let hookAttivo = false;

// ========================================
// INTEGRAZIONE CON MACRODROID HOOK
// ========================================
async function riceviHook(numero, evento) {
    try {
        console.log(`[HOOK] Numero ricevuto: ${numero}`);
        hookAttivo = true;

        // Passa il numero RAW al modulo cliente, che gestirà la normalizzazione, 
        // l'impostazione del campo e l'avvio della ricerca automatica.
        if (window.ClienteModule && typeof window.ClienteModule.riceviDaHook === "function") {
            window.ClienteModule.riceviDaHook(numero); // <-- CORREZIONE CHIAMATA
        } else {
            console.warn("[HOOK] ClienteModule o riceviDaHook non disponibile");
        }

    } catch (err) {
        console.error("[HOOK] Errore nella gestione numero:", err);
    } finally {
        hookAttivo = false;
    }
}

// ========================================
// TEST MANUALE DA CONSOLE
// ========================================
// Usa: window.simulaHook("+393490633281", "chiamata_in_arrivo");
window.simulaHook = (numero, evento = "chiamata_in_arrivo") => {
    console.log(`[SIMULAZIONE HOOK] ${evento} | Numero: ${numero}`);
    riceviHook(numero, evento);
};

// ========================================
// INIZIALIZZAZIONE ORDINI
// ========================================
const OrdiniModule = {
    init() {
        console.log("🧾 OrdiniModule inizializzato");
        // altre inizializzazioni già presenti nel file originale...
    }
};

document.addEventListener("DOMContentLoaded", () => {
    OrdiniModule.init();
});