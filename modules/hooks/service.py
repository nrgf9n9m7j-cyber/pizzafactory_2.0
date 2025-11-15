import logging
from core.database import get_db_connection

# Logger dedicato per MacroDroid
logger = logging.getLogger("macrodroid")


def normalizza_numero(numero: str) -> str:
    """
    Normalizza il numero rimuovendo spazi, simboli e prefissi internazionali
    per garantire confronti coerenti tra formati diversi.
    """
    if not numero:
        return ""

    numero = numero.strip()
    for simbolo in [" ", "-", "(", ")", ".", "_"]:
        numero = numero.replace(simbolo, "")

    # Rimuovi prefisso +39 o 0039 se presente
    if numero.startswith("+39"):
        numero = numero[3:]
    elif numero.startswith("0039"):
        numero = numero[4:]

    # Mantieni solo cifre (elimina eventuali caratteri strani)
    numero = "".join(filter(str.isdigit, numero))
    return numero


def gestisci_evento(numero, evento):
    """
    Gestisce l'evento inviato da MacroDroid e determina l'azione da eseguire.
    Restituisce un dizionario compatibile con la risposta JSON dell'API.
    """
    numero_originale = numero
    numero = normalizza_numero(numero)
    logger.info(f"[HOOK] Evento: {evento} | Numero: {numero_originale} → {numero}")

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Normalizzazione anche lato query
        cur.execute("""
            SELECT nome, cognome, telefono 
            FROM clienti
            WHERE REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(telefono, ' ', ''), '-', ''), '(', ''), ')', ''), '.', ''), '+39', '') = ?
            OR REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(telefono, ' ', ''), '-', ''), '(', ''), ')', ''), '.', ''), '0039', '') = ?
        """, (numero, numero))

        row = cur.fetchone()
        conn.close()

        if row:
            nome_completo = f"{row['nome']} {row['cognome']}".strip()
            logger.info(f"[HOOK] ✅ Cliente riconosciuto: {nome_completo}")
            return {
                "status": "ok",
                "cliente_trovato": True,
                "nome": nome_completo,
                "telefono": row["telefono"],
                "azione": "Apri scheda ordine"
            }

        logger.info("[HOOK] ⚠️ Numero non riconosciuto.")
        return {
            "status": "ok",
            "cliente_trovato": False,
            "azione": "Mostra form nuovo cliente"
        }

    except Exception as e:
        logger.exception(f"[HOOK] ❌ Errore durante la gestione evento: {e}")
        return {
            "status": "error",
            "msg": str(e)
        }
