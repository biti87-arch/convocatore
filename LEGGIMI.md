# Patto del Convocatore

App per il Convocatore della Collana (Vol. 2 - Classi): costruttore di eidolon con evoluzioni e abilità, evocazioni (Libro delle Evocazioni e Libro degli Elementali) con contatori e metaevocazioni, tutti i 9 archetipi.

## Scaricare l'app
Nella pagina **Releases** del repository:
- **Android**: il file `Convocatore-N.apk` (release `v1.0.N`). Scaricalo dal telefono e aprilo per installarlo.
- **Windows**: release `win-1.0.N`, versione *portatile* (doppio clic, niente installazione) o *installazione*.

Le app si ricompilano da sole a ogni aggiornamento del ramo `main`.

## Come si aggiorna quando cambiano i manuali
1. Metti i .docx aggiornati in `sorgenti/docx/` (Convocatore, Libro delle Evocazioni, Libro degli Elementali).
2. `python3 sorgenti/estrai_testo.py` → testo in `sorgenti/txt/`
3. `python3 sorgenti/parse_convocatore.py` e `python3 sorgenti/parse_evocazioni.py` → JSON
4. `python3 sorgenti/build.py` → `www/index.html`

Le meccaniche delle evoluzioni (attacchi, costi speciali, requisiti) sono nella tabella `MECC` di `parse_convocatore.py`; i testi vengono sempre dal manuale.

## Decisioni di design
Vedi `Convocatore_app_design_v1.md` (decisioni A–L, archetipi, correzioni ai sorgenti).
