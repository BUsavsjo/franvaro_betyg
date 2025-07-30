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
python src/busavsjo_pipeline.py
```

## Installera beroenden

Innan du kör flödet behöver du installera de Python-paket som projektet kräver.
Detta görs med:

```bash
pip install -r requirements.txt
```
