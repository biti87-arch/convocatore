# App CONVOCATORE — DESIGN DOC v1

Repo: `biti87-arch/convocatore` · Piattaforme: HTML → Android (APK) → Windows · Architettura come le app Sigillatore e Necrarca.

## STATO LAVORO

| Fase | Stato |
|---|---|
| Analisi regole di classe (eidolon, evoca esterno, doti) | ✅ |
| Decisioni A–H | ✅ confermate 26/09/2026 |
| Mappatura dei 9 archetipi | ✅ |
| Correzioni sorgenti (Convocatore, Vol. 2, Libro delle Evocazioni) | ✅ consegnate 26/09/2026 |
| Estrazione dati in JSON | ⬜ |
| Motore di calcolo eidolon | ⬜ |
| Modulo evocazioni + contatori | ⬜ |
| Archetipi + controllo compatibilità | ⬜ |
| Interfaccia HTML (mobile-first) | ⬜ |
| Build Android + Windows | ⬜ |

## FONTI DATI

| Fonte | Contenuto | Uso nell'app |
|---|---|---|
| Convocatore_v2.4_FINALE.docx | Tabella dell'eidolon, privilegi, 6 forme base, ~60 evoluzioni (1-4 punti), doti, 9 archetipi | `eidolon.json`, `evoluzioni.json`, `doti.json`, `archetipi.json` |
| Libro_evocazioni_v2.5.docx | 100 esterni, gradi I–IX | `esterni.json` |
| Libro_Evocazioni_Elementali_v1.docx (Libro degli Elementali) | 117 elementali, 13 tipi × 9 gradi | `elementali.json` |

I JSON si rigenerano con uno script di estrazione ogni volta che i manuali cambiano: il codice dell'app non contiene regole scritte a mano.

## MODULO 1 — COSTRUTTORE DI EIDOLON

- **Input**: livello convocatore, forma base (Aberrante, Amorfo, Bipede, Quadrupede, Serpentiforme, Taurico), caratteristiche fisiche 16/14/12 a scelta (mentali fisse 10/10/10), affinità (solo Elementalista).
- **Tabella dell'eidolon** applicata per livello: DV (d10), attacchi max, BA naturale e con armi, TS buoni/scarsi della forma, punti abilità, talenti, armatura naturale, For/Des, punti evoluzione.
- **Privilegi automatici**: RD/– per livello, Eludere, Eludere migliorato, Devozione, Multiattacco, Aumenti di caratteristica.
- **Evoluzioni**: controllo di costo, requisiti, catene (→), livello minimo, limite di attacchi, selezioni multiple ammesse ("Speciale"). Considera Punti evoluzione extra (dote), Trasferimento evoluzionistico (punti sottratti all'eidolon) e il −1 dell'Elementalista.
- **Scheda finale**: PF, CA (contatto/impreparato), TS, attacchi con bonus e danni, BMC/DMC, velocità, sensi, immunità, resistenze.

## MODULO 2 — EVOCAZIONI

- Gradi disponibili I–IX secondo la Tabella del convocatore.
- Libro delle Evocazioni per il convocatore base; Libro degli Elementali con l'Elementalista; solo demoni con il Demonologo.
- **Contatori**: usi giornalieri (3 + Car, + Evocazione extra), divieto di evocare lo stesso esterno due volte di fila, blocco se l'eidolon è in campo, timer della durata (1 minuto; 1 minuto per livello con Evocazioni durature; 3 round per il Creativo; 1 round con Evocazioni esplosive).
- **Metaevocazioni**: una alla volta, applicate alla scheda. Le doti non-meta (Evocazioni potenziate, coriacee, vitali) si applicano sempre.
- **Capacità delle creature**: tutte "X per evocazione" (decisione B).

## DECISIONI

| # | Tema | Decisione |
|---|---|---|
| A | Evoluzioni Arti | Esistevano già ma erano fuse dentro il paragrafo di Afferrare: ripristinate come voci separate da 2 punti (**Arti [braccia]**, **Arti [gambe]**, **Attacchi energetici**), Arti selezionabili più volte |
| B | Usi delle capacità | Libro delle Evocazioni allineato a "per evocazione" come il Libro degli Elementali |
| C | PF dell'eidolon | Default 10 al 1° DV + 6 per DV successivo + Cos; campo manuale per i PF tirati |
| D | Volo | Altezza massima 1 m fino al 17° livello del convocatore, poi nessun limite |
| E | Refusi nelle doti | Corretti (Evocazioni caustiche, lunari, coriacee) |
| F | Punti Fatica (Cavalca eidolon) | PF calcolati normalmente e divisi a metà: Fatica per eccesso, Ferita per difetto |
| G | Aumentare Evocazione | Applicato come effetti derivati: +2 per colpire e danni, +2 PF/DV, +2 Tempra, +2 BMC/DMC |
| H | Evoluzioni su esterni (Vincolo prediletto, Mostri Evocati Evoluti) | Applicati i numeri delle evoluzioni che li hanno; le altre aggiunte come testo |
| I | Punti abilità dell'eidolon | (4 + Int) × DV; 5 abilità di classe fisse + 4 a scelta (niente Professione); gradi max = DV; +3 di classe |
| J | Velocità di Scalare, Nuotare, Volare | +8 automatico alla prova corrispondente (Anfibio = Nuotare pari alla velocità su terreno) |
| K | Immunità a un'energia (4 PE) | Sostituita da **Assorbimento energetico (Sop)**: 9° livello, richiede Immunità (Sop) alla stessa energia, recupera PF pari a metà dei danni fino ai massimali |
| L | Aumento di caratteristica (evoluzione) | 1 fino al 5°, 2 fino al 10°, 3 fino al 15°, 4 fino al 20°; distinto dal privilegio dell'eidolon (+1 al 5°, 10°, 15°, 20°) |

## ARCHETIPI

| Archetipo | Eidolon | Evocazioni | Cosa calcola l'app |
|---|---|---|---|
| Elementalista | Esterno elementale, −1 PE, energia, immunità dal 2° | Libro degli Elementali | Affinità, Potere elementale, Detonazione (danni/CD) |
| Demonologo | Base | Solo demoni | Evocazioni potenziate, Offerta di sangue (opz.), Adorazione continua, Teletrasporto funesto |
| Leader empireo | Nessuno | Libro delle Evocazioni | Usi +2, Potenziate scalare (+1 ogni 4 liv.), Coriacee 2°, Vitali 14°, +2d6 al 20°, Cura empirea |
| Signore delle Schiere | Esterno prediletto (regole dell'eidolon) | Libro delle Evocazioni | Usi 5 + Car, Evocazione multipla 1d3 (−1 grado) / 1d4+1 (−2 gradi), Aumentare Evocazione, Vincolo prediletto 2/4 PE, Apoteosi |
| Cavalca eidolon | Solo aberrante/quadrupede/serpentiforme, Cavalcatura, Fatica + Ferita | Nessuna | BAB pieno, Tempra buona, Cura dell'eidolon, cariche |
| Armonizzatore | Resistenza (suono) | Nessuna → Detonazioni acustiche | Danni e CD delle detonazioni, Condotto acustico |
| Profeta | Base; dal 18° supera qualsiasi RD | Nessuna | Presenza soverchiante (CD) |
| Controevocatore | Base | Nessuna → aura | % di fallimento dell'aura (50%, +5% per livello oltre il 10°, max 90%), CD di Indebolire |
| Creativo | Musa, sempre bipede | 3 round, anche con la musa in campo; niente Evocazioni durature | Dal 10° evoca anche la musa |

**Compatibilità**: l'app legge le diciture "Privilegio di classe modificato/sostituito" e impedisce di combinare due archetipi che toccano lo stesso privilegio.

## CORREZIONI APPLICATE AI SORGENTI (26/09/2026)

**Convocatore (manuale singolo + Vol. 2 2.5.1)**
- Arti [braccia], Arti [gambe], Attacchi energetici: separati dal paragrafo di Afferrare, ciascuno con il proprio titolo
- Evocazioni caustiche e Evocazioni lunari: tolto "Inoltre," ripetuto
- Evocazioni coriacee: "+2 la CA Naturale" → "+2 alla CA Naturale"
- Controevocatore, Protezione dalle evocazioni: "s eil" → "se il"
- Controevocatore, Indebolire evocazioni: se il TS riesce la vittima è inferma per 1 round e immune per 24 ore (tolta la contraddizione e "diventa diventare")
- Demonologo: "evoca esterni" → "evoca esterno"; virgola dopo "+3 m alla velocità"; aggiunta la dicitura "Privilegio di classe modificato: Evoca esterno a ciascun livello" a Offerta di sangue
- Armonizzatore: aggiunta la dicitura "Privilegio di classe modificato: Eidolon al 1° livello" ad Affinità al suono
- Elementalista: Evoca elementale e Natura elementale (inserite in precedenza)

- Immunità (Sop) e Magia condivisa (Mag) separate da Fortificazione; tolto il pezzo di "Speciale" finito in Artigli e Schianto; Veleno: "diventa è rallentata" → "diventa rallentata"
- Immunità a un'energia sostituita da Assorbimento energetico (Sop)

**Morfico e Stregone (manuali singoli + Vol. 2)**
- Guarire → Professione (cerusico) dove indica l'abilità

**Libro delle Evocazioni v2.5**
- 88 usi convertiti da "/giorno" e "al giorno" a "per evocazione"
