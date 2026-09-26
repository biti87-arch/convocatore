# Patto del Convocatore

App per il Convocatore della Collana (Vol. 2 - Classi): costruttore di eidolon, evocazioni con contatori e metaevocazioni, tutti i 9 archetipi.

## Versione attuale
Solo pagina HTML (`www/index.html`), da provare prima di creare le versioni Android e Windows.

## Come si aggiorna quando cambiano i manuali
1. Metti i .docx aggiornati in `sorgenti/docx/` (Convocatore, Libro delle Evocazioni, Libro degli Elementali).
2. `python3 sorgenti/estrai_testo.py` → testo in `sorgenti/txt/`
3. `python3 sorgenti/parse_convocatore.py` e `python3 sorgenti/parse_evocazioni.py` → JSON
4. `python3 sorgenti/build.py` → `www/index.html`

Le meccaniche delle evoluzioni (attacchi, costi speciali, requisiti) sono nella tabella `MECC` di `parse_convocatore.py`; i testi vengono sempre dal manuale.

## Decisioni di design
Vedi `Convocatore_app_design_v1.md` (decisioni A–H, archetipi, correzioni ai sorgenti).
