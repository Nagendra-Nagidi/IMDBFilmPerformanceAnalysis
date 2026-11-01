# IMDb Film Atlas

A Streamlit showcase for the three IMDb data notebooks: extraction, cleaning, and exploratory analysis. The app reads the project's raw and cleaned CSV files directly and recalculates the charts from the cleaned data.

## Run locally

From the project root:

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

The app expects these files to remain in place:

- `data/raw/imdb_hollywood_movies_2016_2025_raw.csv`
- `data/processed/imdb_hollywood_movies_2016_2025_cleaned.csv`

The raw and cleaned tables are visible in their respective sections and can also be downloaded. The app surfaces the notebook's extraction checkpoints, missing-value audit, numeric summary, rating/runtime/vote distributions, all eight EDA questions, their supporting summary tables, and the correlation matrix. Charts and summaries are computed from the CSV at app load time, so they stay aligned with the supplied data.

## Data scope

The collection notebook uses a US + English IMDb title alias as a Hollywood-oriented proxy. This does not establish a film's production country and can include international films. Missing ratings, votes, and runtimes are retained as missing values rather than imputed.


## readme change