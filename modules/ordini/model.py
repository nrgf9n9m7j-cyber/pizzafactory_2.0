#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Model Ordini - solo interazione DB"""

from core.database import get_db_connection
from core.exceptions import DatabaseError, NotFoundError

class OrdineModel:
    
    @staticmethod
    def get_fattore_prezzo_formato(formato):
        """Recupera il fattore prezzo per un formato dalla tabella Formati"""
        conn = get_db_connection()
        try:
            result = conn.execute('''
                SELECT Fattore_Prezzo FROM Formati 
                WHERE Nome_Formato = ?
            ''', (formato,)).fetchone()
            return result['Fattore_Prezzo'] if result else 1.0
        finally:
            conn.close()
    
    @staticmethod
    def get_prezzo_base_prodotto(id_prodotto):
        """Recupera il prezzo base di un prodotto"""
        conn = get_db_connection()
        try:
            result = conn.execute('''
                SELECT Prezzo_Base FROM Prodotti 
                WHERE ID_Prodotto = ?
            ''', (id_prodotto,)).fetchone()
            return result['Prezzo_Base'] if result else 0.0
        finally:
            conn.close()
    
    @staticmethod
    def get_attivi():
        """Recupera ordini non completati"""
        conn = get_db_connection()
        try:
            ordini = conn.execute('''
                SELECT o.*, c.Nome, c.Cognome, c.Telefono, t.Descrizione as Tipo_Ordine
                FROM Ordini o
                LEFT JOIN Clienti c ON o.ID_Cliente = c.ID_Cliente
                LEFT JOIN Tipi_Ordine t ON o.ID_Tipo = t.ID_Tipo
                WHERE o.Stato != 'Completato'
                ORDER BY o.Data_Ordine DESC, o.Ora_Ordine DESC
            ''').fetchall()
            return [dict(o) for o in ordini]
        finally:
            conn.close()
    
    @staticmethod
    def get_by_id(ordine_id):
        """Recupera ordine completo con dettagli"""
        conn = get_db_connection()
        try:
            # Ordine principale
            ordine = conn.execute('''
                SELECT o.*, c.Nome, c.Cognome, c.Telefono, c.Indirizzo, c.Civico,
                       t.Descrizione as Tipo_Ordine, m.Nome_Metodo
                FROM Ordini o
                LEFT JOIN Clienti c ON o.ID_Cliente = c.ID_Cliente
                LEFT JOIN Tipi_Ordine t ON o.ID_Tipo = t.ID_Tipo
                LEFT JOIN Metodi_Pagamento m ON o.ID_Metodo_Pagamento = m.ID_Metodo
                WHERE o.ID_Ordine = ?
            ''', (ordine_id,)).fetchone()
            
            if not ordine:
                return None
            
            # Dettagli prodotti (SOLO Prodotti, no Bibite separate)
            dettagli = conn.execute('''
                SELECT d.*, 
                       p.Nome_Prodotto, p.Formato, p.Categoria
                FROM Dettagli_Ordine d
                LEFT JOIN Prodotti p ON d.ID_Prodotto = p.ID_Prodotto
                LEFT JOIN Impasti_Speciali i ON d.ID_Impasto = i.ID_Impasto
                WHERE d.ID_Ordine = ?
                ORDER BY p.Categoria, p.Formato, p.Nome_Prodotto
            ''', (ordine_id,)).fetchall()
            
            prodotti = []
            for det in dettagli:
                # Ingredienti extra
                ingredienti = conn.execute('''
                    SELECT die.*, ing.Nome_Ingrediente
                    FROM Dettagli_Ingredienti_Extra die
                    JOIN Ingredienti ing ON die.ID_Ingrediente = ing.ID_Ingrediente
                    WHERE die.ID_Dettaglio = ?
                    ORDER BY die.Azione DESC, ing.Nome_Ingrediente
                ''', (det['ID_Dettaglio'],)).fetchall()
                
                # Opzioni
                opzioni = conn.execute('''
                    SELECT op.Nome_Opzione, do.ID_Opzione
                    FROM Dettagli_Opzioni do
                    JOIN Opzioni_Preparazione op ON do.ID_Opzione = op.ID_Opzione
                    WHERE do.ID_Dettaglio = ?
                ''', (det['ID_Dettaglio'],)).fetchall()
                
                prodotti.append({
                    'prodotto': dict(det),
                    'ingredienti_extra': [dict(i) for i in ingredienti],
                    'opzioni': [dict(o) for o in opzioni]
                })
            
            return {
                'ordine': dict(ordine),
                'prodotti': prodotti
            }
        finally:
            conn.close()
    
    @staticmethod
    def create(data, codice_ordine):
        """Crea nuovo ordine"""
        conn = get_db_connection()
        try:
            cursor = conn.execute('''
                INSERT INTO Ordini (
                    Codice_Ordine, ID_Cliente, ID_Tipo, ID_Metodo_Pagamento, Numero_Tavolo,
                    Orario_Ritiro, Orario_Consegna, Indirizzo_Consegna, Civico_Consegna,
                    Citta_Consegna, Telefono_Consegna, Note_Ordine, 
                    Totale_Ordine, Sovrapprezzo_Consegna, Sovrapprezzo_Citta,
                    Stato, Pagato
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                codice_ordine,
                data.get('id_cliente'),
                data.get('id_tipo'),
                data.get('id_metodo_pagamento'),
                data.get('numero_tavolo'),
                data.get('orario_ritiro'),
                data.get('orario_consegna'),
                data.get('indirizzo_consegna'),
                data.get('civico_consegna'),
                data.get('citta_consegna'),
                data.get('telefono_consegna'),
                data.get('note_ordine'),
                data.get('totale_finale'),
                data.get('sovrapprezzo_consegna', 0),
                data.get('sovrapprezzo_citta', 0),
                'In Attesa',
                data.get('pagato', 0)
            ))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise DatabaseError(f"Errore creazione ordine: {e}")
        finally:
            conn.close()
    
    @staticmethod
    def insert_dettaglio_prodotto(ordine_id, prodotto):
        """Inserisce dettaglio prodotto (pizze E bibite)"""
        conn = get_db_connection()
        try:
            # TUTTO va in ID_Prodotto (pizze e bibite)
            cursor = conn.execute('''
                INSERT INTO Dettagli_Ordine (
                    ID_Ordine, ID_Prodotto, ID_Impasto, 
                    Quantita, Prezzo_Unitario, Note_Prodotto
                )
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                ordine_id, 
                prodotto.get('id_prodotto'), 
                prodotto.get('id_impasto'),
                prodotto.get('quantita', 1), 
                prodotto.get('prezzo_unitario'), 
                prodotto.get('note', '')
            ))
            
            dettaglio_id = cursor.lastrowid
            
            # Aggiorna impasto utilizzato (solo se presente)
            if prodotto.get('id_impasto'):
                conn.execute('''
                    UPDATE Impasti_Speciali 
                    SET Quantita_Utilizzata = Quantita_Utilizzata + ?
                    WHERE ID_Impasto = ?
                ''', (prodotto.get('quantita', 1), prodotto.get('id_impasto')))
            
            # Scala scorte se il prodotto le gestisce
            conn.execute('''
                UPDATE Prodotti 
                SET Quantita_Utilizzata = Quantita_Utilizzata + ?
                WHERE ID_Prodotto = ? AND Gestione_Scorte = 1
            ''', (prodotto.get('quantita', 1), prodotto.get('id_prodotto')))
            
            # Decrementa quantità disponibile (per bibite)
            conn.execute('''
                UPDATE Prodotti 
                SET Quantita_Disponibile = Quantita_Disponibile - ?
                WHERE ID_Prodotto = ? AND Gestione_Scorte = 1 AND Quantita_Disponibile > 0
            ''', (prodotto.get('quantita', 1), prodotto.get('id_prodotto')))
            
            conn.commit()
            return dettaglio_id
        except Exception as e:
            conn.rollback()
            raise DatabaseError(f"Errore inserimento dettaglio: {e}")
        finally:
            conn.close()
    
    @staticmethod
    def insert_extra_ingrediente(dettaglio_id, extra):
        """Inserisce ingrediente extra"""
        conn = get_db_connection()
        try:
            conn.execute('''
                INSERT INTO Dettagli_Ingredienti_Extra (ID_Dettaglio, ID_Ingrediente, Azione, Sovrapprezzo)
                VALUES (?, ?, ?, ?)
            ''', (dettaglio_id, extra.get('id_ingrediente'), extra.get('azione'), extra.get('sovrapprezzo', 0)))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise DatabaseError(f"Errore inserimento extra: {e}")
        finally:
            conn.close()
    
    @staticmethod
    def insert_opzione(dettaglio_id, opzione_id):
        """Inserisce opzione preparazione"""
        conn = get_db_connection()
        try:
            conn.execute('''
                INSERT INTO Dettagli_Opzioni (ID_Dettaglio, ID_Opzione)
                VALUES (?, ?)
            ''', (dettaglio_id, opzione_id))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise DatabaseError(f"Errore inserimento opzione: {e}")
        finally:
            conn.close()
    
    @staticmethod
    def update(ordine_id, data):
        """Aggiorna ordine"""
        conn = get_db_connection()
        try:
            conn.execute('''
                UPDATE Ordini SET
                    ID_Cliente=?, ID_Tipo=?, ID_Metodo_Pagamento=?, Numero_Tavolo=?,
                    Orario_Ritiro=?, Orario_Consegna=?, Indirizzo_Consegna=?, Civico_Consegna=?,
                    Citta_Consegna=?, Telefono_Consegna=?, Note_Ordine=?,
                    Totale_Ordine=?, Sovrapprezzo_Consegna=?, Sovrapprezzo_Citta=?, Pagato=?
                WHERE ID_Ordine=?
            ''', (
                data.get('id_cliente'), data.get('id_tipo'), data.get('id_metodo_pagamento'), data.get('numero_tavolo'),
                data.get('orario_ritiro'), data.get('orario_consegna'), data.get('indirizzo_consegna'), data.get('civico_consegna'),
                data.get('citta_consegna'), data.get('telefono_consegna'), data.get('note_ordine'),
                data.get('totale_finale'), data.get('sovrapprezzo_consegna', 0), data.get('sovrapprezzo_citta', 0),
                data.get('pagato', 0), ordine_id
            ))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise DatabaseError(f"Errore aggiornamento ordine: {e}")
        finally:
            conn.close()
    
    @staticmethod
    def delete_dettagli(ordine_id):
        """Elimina dettagli ordine"""
        conn = get_db_connection()
        try:
            conn.execute('DELETE FROM Dettagli_Ordine WHERE ID_Ordine = ?', (ordine_id,))
            conn.commit()
        finally:
            conn.close()
    
    @staticmethod
    def update_pagato(ordine_id, pagato):
        """Aggiorna stato pagamento"""
        conn = get_db_connection()
        try:
            conn.execute('UPDATE Ordini SET Pagato = ? WHERE ID_Ordine = ?', (pagato, ordine_id))
            conn.commit()
        finally:
            conn.close()
    
    @staticmethod
    def delete(ordine_id):
        """Elimina ordine"""
        conn = get_db_connection()
        try:
            conn.execute('DELETE FROM Ordini WHERE ID_Ordine = ?', (ordine_id,))
            conn.commit()
        finally:
            conn.close()
    
    @staticmethod
    def get_totali_attivi():
        """Recupera totali ordini attivi"""
        conn = get_db_connection()
        try:
            totali = conn.execute('''
                SELECT 
                    COUNT(*) as num_ordini,
                    SUM(Totale_Ordine) as totale_euro,
                    SUM(CASE WHEN Pagato = 1 THEN Totale_Ordine ELSE 0 END) as pagato,
                    SUM(CASE WHEN Pagato = 0 THEN Totale_Ordine ELSE 0 END) as da_pagare
                FROM Ordini 
                WHERE Stato != 'Completato'
            ''').fetchone()
            
            return {
                'num_ordini': totali['num_ordini'] or 0,
                'totale_euro': totali['totale_euro'] or 0,
                'pagato': totali['pagato'] or 0,
                'da_pagare': totali['da_pagare'] or 0
            }
        finally:
            conn.close()
    
    @staticmethod
    def update_statistiche_cliente(cliente_id):
        """Aggiorna statistiche cliente dopo ordine"""
        conn = get_db_connection()
        try:
            conn.execute('''
                UPDATE Clienti 
                SET Totale_Ordini = Totale_Ordini + 1, Ultimo_Ordine = CURRENT_DATE
                WHERE ID_Cliente = ?
            ''', (cliente_id,))
            conn.commit()
        finally:
            conn.close()
