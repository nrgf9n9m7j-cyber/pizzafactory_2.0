// ========================================
// CORE/UTILS.JS - Utility Riutilizzabili
// ========================================

const Utils = {
    // ========================================
    // FORMATTAZIONE
    // ========================================
    formatMoney(amount) {
        return parseFloat(amount).toFixed(2);
    },
    
    formatTime(date = new Date()) {
        return date.toTimeString().slice(0, 5);
    },
    
    // ========================================
    // VALIDAZIONE
    // ========================================
    validaTelefono(telefono) {
        const cleaned = telefono.replace(/\s+/g, '');
        return /^(\+39)?3\d{8,9}$/.test(cleaned);
    },
    
    validaEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    },
    
    // ========================================
    // CALCOLI CLIENTE - TEMA BOTANICO 🌱➡️🌳
    // ========================================
    calcolaLifecycle(numOrdini) {
        if (numOrdini === 0) return { emoji: '❓', status: 'Mai Ordinato' };
        if (numOrdini === 1) return { emoji: '🌱', status: 'Nuovo' };
        if (numOrdini <= 5) return { emoji: '🌿', status: 'In crescita' };
        if (numOrdini <= 15) return { emoji: '🌲', status: 'Abituale' };
        return { emoji: '🌳', status: 'Fidelizzato' };
    },
    
    calcolaRating(rating) {
        const mapping = {
            5: { emoji: '🤩', descrizione: 'Top' },
            4: { emoji: '😊', descrizione: 'Gentile' },
            3: { emoji: '😐', descrizione: 'OK' },
            2: { emoji: '😕', descrizione: 'Poco cordiale' },
            1: { emoji: '😠', descrizione: 'Problematico' }
        };
        return mapping[rating] || { emoji: '❓', descrizione: 'Non valutato' };
    },
    
    // ========================================
    // DEBOUNCE
    // ========================================
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    // ========================================
    // DOM HELPERS
    // ========================================
    createElement(tag, className, innerHTML = '') {
        const el = document.createElement(tag);
        if (className) el.className = className;
        if (innerHTML) el.innerHTML = innerHTML;
        return el;
    },
    
    hide(element) {
        if (typeof element === 'string') {
            element = document.getElementById(element);
        }
        if (element) element.classList.add('hidden');
    },
    
    show(element) {
        if (typeof element === 'string') {
            element = document.getElementById(element);
        }
        if (element) element.classList.remove('hidden');
    },
    
    toggle(element) {
        if (typeof element === 'string') {
            element = document.getElementById(element);
        }
        if (element) element.classList.toggle('hidden');
    }
};

console.log('✅ Utils.js caricato con emoji lifecycle botaniche 🌱🌿🌲🌳');
