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

Kör hela flödet med:

```bash
python -m franvaro_betyg.busavsjo_pipeline
```
