# 🐍 Python-projekt: franvaro_betyg

Detta projekt är strukturerat enligt Sävsjö kommuns riktlinjer.

## Struktur
- `src/` – programkod
- `tests/` – testmoduler
- `data/` – ej versionerad data

Projektet använder en **raw/output**-struktur under `data/`:

- `data/raw/betyg/` – här läggs SCB-exporterade txt-filer från Edlevo.
- `data/raw/franvaro/` – här läggs frånvarofiler (`.xls`) från Vklass.
- `data/output/` – hit skrivs samtliga genererade filer.

### Läsår och mappar

I `src/config_paths.py` finns konstanten `LASAR` som anger vilket läsår som
analyseras (exempelvis `"2024/2025"`). Alla rå- och outputfiler sparas i
undermappar med detta namn, t.ex. `data/raw/betyg/<läsår>` och
`data/output/<läsår>`. På så vis kan flera års data hanteras utan konflikt.

De JSON-filer som genereras för webbgränssnittet hamnar i
`data/output/<läsår>/json/`. Kopiera dem vid behov till motsvarande mapp under
`public/json/<läsår>` för att exponera dem via webbplatsen.

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
