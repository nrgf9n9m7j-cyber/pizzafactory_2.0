// ========================================
// CLIENTE MODULE - GESTIONE CLIENTI ORDINI
// ========================================
const ClienteModule = {
    ultimoNumeroHook: null,
    bloccatoHook: false,

    // ========================================
    // RICEVE NUMERO DA HOOK
    // ========================================
    riceviDaHook(numero) {
        console.log("[CLIENTE] Ricevuto numero da hook:", numero);

        if (this.bloccatoHook) return;
        this.bloccatoHook = true;

        // Normalizza
        let pulito = numero.replace(/\D/g, "");
        if (pulito.startsWith("39")) pulito = pulito.slice(2);
        if (pulito.length === 10) {
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

        // Imposta valore SENZA scatenare eventi
        input.removeEventListener("input", this._onInputListener);
        input.value = pulito;
        input.dispatchEvent(new Event("change"));
        input.addEventListener("input", this._onInputListener);

        console.log("[CLIENTE] Ricerca cliente automatica avviata per:", pulito);
        try {
            window.hookCercaCliente(pulito);
        } catch (err) {
            console.warn("[CLIENTE] Errore nella ricerca automatica:", err);
        }

        setTimeout(() => (this.bloccatoHook = false), 800);
    },

    // ========================================
    // RICERCA CLIENTE MANUALE
    // ========================================
    hookCerca(query) {
        if (this.bloccatoHook) return; // evita loop
        if (!query) return;

        console.log("[CLIENTE] Ricerca manuale per:", query);
        try {
            window.hookCercaCliente(query);
        } catch (err) {
            console.warn("[CLIENTE] Errore nella ricerca manuale:", err);
        }
    },

    // ========================================
    // CAMBIA CLIENTE
    // ========================================
    cambia() {
        State.setCliente(null);
        Utils.hide("cliente-recap");
        document.getElementById("search-cliente-hook").focus();
    },

    // ========================================
    // PRECOMPILA FORM
    // ========================================
    precompilaForm(tipo) {
        const cliente = State.getCliente();
        if (!cliente) return;

        if (tipo === 1) {
            document.getElementById("cognome-consegna").value = cliente.Cognome || "";
            document.getElementById("nome-consegna").value = cliente.Nome || "";
            document.getElementById("telefono-consegna").value = cliente.Telefono || "";
            document.getElementById("indirizzo-consegna").value = cliente.Indirizzo || "";
            document.getElementById("civico-consegna").value = cliente.Civico || "";
            document.getElementById("citta-consegna").value = cliente.Citta || "Chieri";
        } else if (tipo === 2) {
            document.getElementById("cognome-ritiro").value = cliente.Cognome || "";
            document.getElementById("telefono-ritiro").value = cliente.Telefono || "";
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

// Init
window.addEventListener("DOMContentLoaded", () => ClienteModule.init());

// Export global
window.ClienteModule = ClienteModule;
window.hookCercaCliente = (query) => ClienteModule.hookCerca(query);
window.cambiaCliente = () => ClienteModule.cambia();

console.log("✅ ClienteModule caricato");