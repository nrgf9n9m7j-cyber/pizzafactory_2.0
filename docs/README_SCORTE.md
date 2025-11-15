# 📦 SISTEMA GESTIONE SCORTE - PIZZAFACTORY 2.0

## 🎯 PANORAMICA

Sistema completo per gestione scorte bibite con:
- ✅ Import automatico clienti e bibite da DB vecchio
- ✅ Gestione soglie minime personalizzabili
- ✅ Alert automatici per scorte basse
- ✅ Form carico merce con supporto barcode scanner (futuro)
- ✅ Tracking completo movimenti di magazzino

---

## 📋 FILE CREATI

### 1. **migration_scorte.py**
Aggiunge colonne gestione scorte al database

### 2. **import_clienti.py**
Importa 29 clienti dal vecchio database

### 3. **popola_bibite.py**
Importa 12 bibite dal vecchio database con scorte attive

### 4. **modal_menu_bibite.html + menu_bibite.js**
Modal per visualizzare e aggiungere bibite al carrello

### 5. **modal_soglie_scorte.html + modal_soglie.js**
Modal per modificare soglie minime e parametri scorte

### 6. **carico_scorte_demo.html**
Form standalone per carico merce in entrata

---

## 🚀 INSTALLAZIONE

### STEP 1: PREPARAZIONE DATABASE

```bash
# 1. Copia il vecchio database nella directory del progetto
cp pizzeria_OLD.db /path/to/progetto/

# 2. Esegui migration scorte
python3 migration_scorte.py
```

**Output atteso:**
```
🔄 MIGRATION: Sistema Gestione Scorte
✅ Colonna 'Gestione_Scorte' aggiunta
✅ Colonna 'Quantita_Disponibile' aggiunta
✅ Colonna 'Soglia_Minima' aggiunta
✅ Colonna 'Unita_Misura' aggiunta
✅ Colonna 'Quantita_Utilizzata' aggiunta
✅ Tabella Movimenti_Scorte creata
✅ MIGRATION COMPLETATA CON SUCCESSO!
```

---

### STEP 2: IMPORT CLIENTI

```bash
python3 import_clienti.py
```

**Output atteso:**
```
📥 IMPORT CLIENTI DA VECCHIO DATABASE
📊 Clienti trovati nel vecchio DB: 29
✅ Importati 29/29 clienti...
✅ IMPORT COMPLETATO!
```

---

### STEP 3: POPOLA BIBITE

```bash
python3 popola_bibite.py
```

**Output atteso:**
```
🍹 IMPORT BIBITE CON GESTIONE SCORTE
📊 Bibite trovate nel vecchio DB: 12
✅ Coca Cola 33cl                    €2.00  Cat:Bibite     Soglia:10
✅ Coca Cola Zero 33cl               €2.00  Cat:Bibite     Soglia:10
✅ Fanta 33cl                        €2.00  Cat:Bibite     Soglia:10
[...]
✅ IMPORT BIBITE COMPLETATO!
```

---

### STEP 4: INTEGRAZIONE FRONTEND

#### A) AGGIUNGI MODAL BIBITE

```html
<!-- In: frontend/templates/base.html o index.html -->
<!-- Prima del tag </body> -->
{% include 'components/modal_menu_bibite.html' %}
<script src="{{ url_for('static', filename='js/modules/ordini/menu_bibite.js') }}"></script>
```

#### B) AGGIUNGI MODAL SOGLIE

```html
<!-- In: frontend/templates/base.html -->
{% include 'components/modal_soglie_scorte.html' %}
<script src="{{ url_for('static', filename='js/components/modal_soglie.js') }}"></script>
```

#### C) AGGIUNGI BOTTONE MENU BIBITE

```html
<!-- In: frontend/templates/pages/nuovo_ordine/menu_rapido.html -->
<button class="btn-menu" onclick="MenuBibite.apri()">
    🍹 Bibite
</button>
```

#### D) AGGIUNGI LINK CARICO SCORTE

```html
<!-- Nel menu hamburger -->
<a href="/carico-scorte" class="menu-item">
    📦 Carico Scorte
</a>
```

---

### STEP 5: BACKEND ROUTES

Aggiungi questi endpoint in `modules/menu/routes.py`:

```python
@menu_bp.route('/api/prodotti/bibite')
def get_bibite():
    """Restituisce tutte le bibite disponibili"""
    try:
        conn = get_db_connection()
        bibite = conn.execute('''
            SELECT * FROM Prodotti 
            WHERE Tipo_Prodotto = 'bibita' AND Disponibile = 1
            ORDER BY Categoria, Nome_Prodotto
        ''').fetchall()
        conn.close()
        
        return jsonify([dict(b) for b in bibite])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@menu_bp.route('/api/prodotti/con-scorte')
def get_prodotti_con_scorte():
    """Restituisce prodotti con gestione scorte attiva"""
    try:
        conn = get_db_connection()
        prodotti = conn.execute('''
            SELECT * FROM Prodotti 
            WHERE Gestione_Scorte = 1
            ORDER BY Categoria, Nome_Prodotto
        ''').fetchall()
        conn.close()
        
        return jsonify([dict(p) for p in prodotti])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@menu_bp.route('/api/prodotti/aggiorna-soglie', methods=['POST'])
def aggiorna_soglie():
    """Aggiorna soglie minime prodotti"""
    try:
        data = request.json
        modifiche = data.get('modifiche', [])
        
        conn = get_db_connection()
        aggiornati = 0
        
        for mod in modifiche:
            id_prodotto = mod['ID_Prodotto']
            updates = []
            params = []
            
            if 'Soglia_Minima' in mod:
                updates.append('Soglia_Minima = ?')
                params.append(mod['Soglia_Minima'])
            
            if 'Unita_Misura' in mod:
                updates.append('Unita_Misura = ?')
                params.append(mod['Unita_Misura'])
            
            if updates:
                query = f"UPDATE Prodotti SET {', '.join(updates)} WHERE ID_Prodotto = ?"
                params.append(id_prodotto)
                conn.execute(query, params)
                aggiornati += 1
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'aggiornati': aggiornati})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

Aggiungi endpoint carico scorte in `modules/scorte/routes.py` (nuovo modulo):

```python
from flask import Blueprint, request, jsonify, render_template
from core.database import get_db_connection

scorte_bp = Blueprint('scorte', __name__)

@scorte_bp.route('/carico-scorte')
def carico_scorte_page():
    """Pagina carico scorte"""
    return render_template('pages/carico_scorte.html')

@scorte_bp.route('/api/scorte/carico', methods=['POST'])
def carico_scorte():
    """Registra carico scorte"""
    try:
        data = request.json
        movimenti = data.get('movimenti', [])
        
        conn = get_db_connection()
        
        for mov in movimenti:
            id_prodotto = mov['ID_Prodotto']
            quantita = mov['Quantita']
            note = mov.get('Note', '')
            
            # Leggi quantità attuale
            qta_attuale = conn.execute(
                'SELECT Quantita_Disponibile FROM Prodotti WHERE ID_Prodotto = ?',
                (id_prodotto,)
            ).fetchone()[0] or 0
            
            # Calcola nuova quantità
            qta_nuova = qta_attuale + quantita
            
            # Aggiorna prodotto
            conn.execute('''
                UPDATE Prodotti 
                SET Quantita_Disponibile = ? 
                WHERE ID_Prodotto = ?
            ''', (qta_nuova, id_prodotto))
            
            # Registra movimento
            conn.execute('''
                INSERT INTO Movimenti_Scorte 
                (ID_Prodotto, Tipo_Movimento, Quantita, Quantita_Precedente, Quantita_Nuova, Note)
                VALUES (?, 'Carico', ?, ?, ?, ?)
            ''', (id_prodotto, quantita, qta_attuale, qta_nuova, note))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'movimenti': len(movimenti)})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Registra blueprint in app.py
# app.register_blueprint(scorte_bp)
```

---

## 🎨 INTEGRAZIONE DASHBOARD

Nella dashboard, aggiungi schedina alert scorte basse:

```html
<!-- Alert Scorte Basse -->
<div id="alert-scorte-basse" class="alert warning" style="display: none;">
    <span class="alert-icon">⚠️</span>
    <span class="alert-text" id="alert-scorte-text"></span>
</div>

<script>
// Controlla scorte basse
async function controllaScorte() {
    const response = await fetch('/api/prodotti/scorte-basse');
    const prodotti = await response.json();
    
    if (prodotti.length > 0) {
        const alert = document.getElementById('alert-scorte-basse');
        const text = document.getElementById('alert-scorte-text');
        
        text.textContent = `${prodotti.length} prodotti sotto soglia minima`;
        alert.style.display = 'flex';
    }
}
</script>
```

---

## 📊 STRUTTURA DATABASE

### Tabella: Prodotti (modificata)
```sql
Gestione_Scorte       INTEGER   -- 0=no, 1=sì
Quantita_Disponibile  INTEGER   -- Scorte attuali
Soglia_Minima         INTEGER   -- Alert quando <= soglia
Unita_Misura          TEXT      -- pz, lt, kg, conf
Quantita_Utilizzata   INTEGER   -- Totale venduto (tracking)
```

### Tabella: Movimenti_Scorte (nuova)
```sql
ID_Movimento          INTEGER PRIMARY KEY
ID_Prodotto           INTEGER
Tipo_Movimento        TEXT      -- Carico, Scarico, Vendita, Inventario, Rettifica
Quantita              INTEGER
Quantita_Precedente   INTEGER
Quantita_Nuova        INTEGER
Data_Movimento        DATETIME
Note                  TEXT
Utente                TEXT
```

---

## 🔧 UTILIZZO

### 1. CARICO MERCE
1. Apri `/carico-scorte`
2. Cerca prodotto o filtra per categoria
3. Inserisci quantità e clicca "Aggiungi"
4. Aggiungi note (es. numero fattura)
5. Conferma carico

### 2. MODIFICA SOGLIE
1. Dashboard → Menu hamburger → "Gestione Soglie"
2. Cerca prodotto
3. Modifica soglia minima e/o unità misura
4. Salva modifiche

### 3. MENU BIBITE
1. Nuovo Ordine → Bottone "Bibite"
2. Filtra per categoria
3. Clicca sulla bibita per aggiungerla al carrello
4. Badge "⚠️ Poche" per scorte basse

---

## 🎯 FUNZIONALITÀ FUTURE

- [ ] Barcode scanner hardware/mobile
- [ ] Export movimenti in Excel/PDF
- [ ] Grafici consumo per prodotto
- [ ] Previsione riordino automatico
- [ ] Integrazione con fornitori
- [ ] Gestione lotti e scadenze

---

## 📝 NOTE IMPORTANTI

1. **Primo carico**: Dopo import bibite, tutte hanno quantità = 0. Usa "Carico Scorte" per caricare quantità iniziali.

2. **Alert automatici**: Il sistema mostra alert quando scorte ≤ soglia minima.

3. **Vendite**: Quando vendi una bibita, la quantità viene decrementata automaticamente e registrato movimento tipo "Vendita".

4. **Backup**: Prima di eseguire migration, fai backup del database!

---

## 🐛 TROUBLESHOOTING

**Problema**: Migration fallisce con "table Prodotti has no column named Gestione_Scorte"
**Soluzione**: La migration non è stata completata. Riesegui `migration_scorte.py`

**Problema**: Import clienti dice "database non trovato"
**Soluzione**: Assicurati che `pizzeria_OLD.db` sia nella stessa directory dello script

**Problema**: Modal bibite non si apre
**Soluzione**: Verifica che `menu_bibite.js` sia caricato e che l'endpoint `/api/prodotti/bibite` funzioni

---

## ✅ CHECKLIST INSTALLAZIONE

- [ ] Migration database eseguita
- [ ] Clienti importati (29)
- [ ] Bibite importate (12)
- [ ] Modal bibite integrato
- [ ] Modal soglie integrato
- [ ] Form carico scorte accessibile
- [ ] Endpoint backend attivi
- [ ] Alert dashboard configurati
- [ ] Primo carico scorte effettuato
- [ ] Test vendita bibita (verifica decremento)

---

**Fatto! Sistema scorte completo e funzionante! 🎉**
