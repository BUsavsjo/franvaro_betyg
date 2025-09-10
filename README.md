# 🐍 Python-projekt: franvaro_betyg

Detta projekt är strukturerat enligt Sävsjö kommuns riktlinjer.

## Struktur
- `src/` – programkod
- `tests/` – testmoduler
- `data/` – ej versionerad data

Projektet använder en **raw/output**-struktur under `data/`:

- `data/raw/betyg/<läsår>/ak6` och `data/raw/betyg/<läsår>/ak9` –
  här läggs SCB-exporterade betygs‑txt‑filer från Edlevo för respektive årskurs.
- `data/raw/franvaro/<läsår>` – här placeras frånvarofiler (`.xls`) från Vklass.
- `data/output/<läsår>` – hit skrivs samtliga genererade Excel‑ och textfiler.
- `data/output/json/<läsår>` – här hamnar de JSON‑filer som webbgränssnittet använder.

### Läsår och mappar

I `src/config_paths.py` finns konstanten `LASAR` som anger vilket läsår som
analyseras (exempelvis `"2024/2025"`). Alla rå- och outputfiler sparas i
undermappar med detta namn, t.ex. `data/raw/betyg/<läsår>` och
`data/output/<läsår>`. På så vis kan flera års data hanteras utan konflikt.

De JSON-filer som genereras för webbgränssnittet hamnar i
`data/output/json/<läsår>`. Kopiera dem vid behov till motsvarande mapp under
`public/json/<läsår>` för att exponera dem via webbplatsen.

### Outputfiler

Efter en lyckad körning ligger sammanställda Excel‑filer och
resultat i `data/output/<läsår>` (t.ex. `betyg_ak6.xlsx`,
`franvaro_total.xlsx`, `betyg_ak6_med_merit.xlsx`).
JSON‑exporter sparas i `data/output/json/<läsår>`.

### Konfiguration av ämnesnamn

För att kunna visa mer lättförståeliga namn för skolämnen i
resultat- och JSON-filer finns filen `config/subject_names.json`. Här kan
varje ämneskolumn från betygsfilen kopplas till ett visningsnamn.
Om en kolumn saknas i filen används kolumnens originalnamn.

Kör hela flödet med:

```bash
python src/busavsjo_pipeline.py
```

Pipelinen kontrollerar automatiskt att nödvändiga Python-beroenden finns och att
datamapparna är skapade. Saknas något får du ett tydligt felmeddelande.

## Installera beroenden

Innan du kör flödet behöver du installera de Python-paket som projektet kräver.
Detta görs med:

```bash
pip install -r requirements.txt
```
