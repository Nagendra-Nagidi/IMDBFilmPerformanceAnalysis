from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


ROOT = Path(__file__).resolve().parent
RAW_PATH = ROOT / "data" / "raw" / "imdb_hollywood_movies_2016_2025_raw.csv"
CLEAN_PATH = ROOT / "data" / "processed" / "imdb_hollywood_movies_2016_2025_cleaned.csv"

st.set_page_config(
    page_title="IMDb Film Atlas | 2016–2025",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

COLORS = {
    "ink": "#17263c",
    "muted": "#64748b",
    "blue": "#3b82f6",
    "teal": "#0f9f91",
    "violet": "#7957d5",
    "amber": "#e8a536",
    "paper": "#f5f7fb",
}

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
    :root { --ink:#17263c; --muted:#64748b; --blue:#3b82f6; --paper:#f5f7fb; }
    html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
    .stApp { background:var(--paper); color:var(--ink); }
    h1,h2,h3 { font-family:'Manrope',sans-serif; letter-spacing:-.035em; }
    .block-container { max-width:1440px; padding-top:2rem; padding-bottom:4rem; }
    [data-testid="stSidebar"] { background:#101d31; }
    [data-testid="stSidebar"] * { color:#e7edf6; }
    .hero { background:linear-gradient(118deg,#102039 0%,#203c62 58%,#315b83 100%);
      color:white; padding:2.3rem 2.7rem; border-radius:24px; position:relative; overflow:hidden;
      box-shadow:0 18px 45px rgba(25,48,79,.16); margin-bottom:1.5rem; }
    .hero:after { content:'✦'; position:absolute; right:7%; top:-48px; font-size:250px; opacity:.06; }
    .eyebrow { text-transform:uppercase; letter-spacing:.17em; font-size:.72rem; font-weight:700; opacity:.72; }
    .hero h1 { color:white; font-size:2.6rem; margin:.45rem 0 .55rem; }
    .hero p { color:#d8e3ef; max-width:760px; font-size:1.03rem; margin:0; line-height:1.65; }
    .source-pill { display:inline-block; margin-top:1.3rem; padding:.4rem .75rem; border-radius:999px;
      background:rgba(255,255,255,.11); color:#eaf2ff; font-size:.77rem; }
    .section-head { padding:1.1rem 1.35rem; border-radius:16px; margin:2.5rem 0 1.25rem; scroll-margin-top:1rem;
      background:white; box-shadow:0 5px 20px rgba(30,50,80,.045); border-left:5px solid var(--accent); }
    .section-head .eyebrow { color:var(--accent); opacity:1; }
    .section-head h2 { color:var(--ink); font-size:1.55rem; margin:.2rem 0 .25rem; }
    .section-head p { color:var(--muted); margin:0; font-size:.93rem; }
    .note { padding:1rem 1.15rem; border-radius:12px; background:#fff; border:1px solid #e6ebf2;
      color:#43536a; line-height:1.6; font-size:.91rem; }
    .stMetric { background:white; padding:1rem 1.1rem; border:1px solid #e8edf4; border-radius:14px;
      box-shadow:0 4px 16px rgba(30,50,80,.035); }
    .stMetric label { color:#64748b !important; }
    div[data-testid="stDataFrame"] { border:1px solid #e5eaf1; border-radius:12px; overflow:hidden; }
    .small-caption { color:#708096; font-size:.82rem; }
    .output-label { color:#718198; text-transform:uppercase; letter-spacing:.11em; font-size:.7rem; font-weight:700; margin:.45rem 0; }
    [data-testid="stExpander"] { background:#fff; border:1px solid #e7edf5; border-radius:14px; }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def get_data(path: Path, label: str) -> pd.DataFrame:
    if not path.exists():
        st.error(f"Could not find the {label} CSV at `{path.relative_to(ROOT)}`.")
        st.stop()
    try:
        return load_data(str(path))
    except Exception as exc:
        st.error(f"Could not read the {label} CSV: {exc}")
        st.stop()


def section(kicker: str, title: str, description: str, color: str, anchor: str) -> None:
    st.markdown(
        f'<div id="{anchor}" class="section-head" style="--accent:{color}"><div class="eyebrow">{kicker}</div>'
        f'<h2>{title}</h2><p>{description}</p></div>',
        unsafe_allow_html=True,
    )


def figure_layout(fig, height=390):
    fig.update_layout(
        height=height,
        margin=dict(l=18, r=18, t=48, b=24),
        paper_bgcolor="rgba(255,255,255,0)",
        plot_bgcolor="rgba(255,255,255,0)",
        font=dict(family="DM Sans, sans-serif", color=COLORS["ink"]),
        title=dict(font=dict(size=16, color=COLORS["ink"])),
        hoverlabel=dict(bgcolor="white", font_size=13),
    )
    fig.update_xaxes(showgrid=True, gridcolor="#edf1f6", zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    return fig


raw = get_data(RAW_PATH, "raw")
clean = get_data(CLEAN_PATH, "cleaned")
raw_rows, clean_rows = len(raw), len(clean)
years = clean["startyear"].dropna()
year_span = f"{int(years.min())}–{int(years.max())}" if not years.empty else "2016–2025"

with st.sidebar:
    st.markdown("## 🎬 IMDb Film Atlas")
    st.caption("A guided look at the data pipeline")
    st.markdown("---")
    st.markdown("**On this page**")
    st.markdown("1. [Data collection](#data-collection)\n2. [Data cleaning](#data-cleaning)\n3. [Exploratory analysis](#exploratory-analysis)")
    st.markdown("---")
    st.caption("Source: IMDb non-commercial datasets\n\nCoverage: 2016–2025")

st.markdown(
    f'<div class="hero"><div class="eyebrow">IMDb • FILM DATA • {year_span}</div>'
    '<h1>From raw records to film insights</h1>'
    '<p>Explore the IMDb collection, see how the records were prepared, then move through the findings from the cleaned movie dataset.</p>'
    f'<span class="source-pill">{clean_rows:,} cleaned records &nbsp;·&nbsp; 3 notebook stages</span></div>',
    unsafe_allow_html=True,
)

# Stage 1: collection
section("01 · COLLECTION", "IMDb data collection", "The extraction notebook narrows IMDb’s bulk files into a focused, inspectable movie dataset.", COLORS["blue"], "data-collection")
c1, c2, c3 = st.columns(3)
c1.metric("Raw movie records", f"{raw_rows:,}", "saved from extraction")
c2.metric("Fields collected", f"{raw.shape[1]}", "movie, title, year, genre, rating & votes")
c3.metric("Release window", year_span, "inclusive")
st.markdown('<div class="output-label">Extraction checkpoints from notebook 01</div>', unsafe_allow_html=True)
f1, f2, f3 = st.columns(3)
f1.metric("Movies in year range", "199,036", "movie titles from IMDb basics")
f2.metric("US + English aliases", "4,455", "distinct title IDs")
f3.metric("Final joined records", f"{raw_rows:,}", "movie details + IMDb ratings")
funnel = pd.DataFrame({"Extraction stage": ["Movies · 2016–2025", "US + English title IDs", "Matched movie records"], "Records": [199036, 4455, raw_rows]})
fig = px.bar(funnel, x="Records", y="Extraction stage", orientation="h", text="Records",
             color="Extraction stage", color_discrete_sequence=["#8db7fa", "#5d91df", COLORS["blue"]],
             title="The extraction narrows the source data")
fig.update_layout(showlegend=False)
fig.update_traces(texttemplate="%{text:,}", textposition="outside", cliponaxis=False)
st.plotly_chart(figure_layout(fig, 260), use_container_width=True)
st.markdown(
    '<div class="note"><b>Collection path</b> &nbsp; IMDb title basics → movie titles released in 2016–2025 → US + English title alias → IMDb ratings and votes. '
    'The US + English alias is a Hollywood-oriented proxy; it does not confirm production country.</div>',
    unsafe_allow_html=True,
)
with st.expander("Extracted raw dataset · all records", expanded=True):
    st.caption("All rows are available below. Use the table controls to sort and inspect fields.")
    st.dataframe(raw, use_container_width=True, height=430, hide_index=True)
    st.download_button("Download raw CSV", raw.to_csv(index=False).encode("utf-8"), "imdb_movies_raw.csv", "text/csv", key="raw-download")

# Stage 2: cleaning
section("02 · PREPARATION", "Cleaning & quality checks", "The cleaning notebook standardizes fields and marks invalid values as missing without inventing replacement data.", COLORS["teal"], "data-cleaning")
missing_raw = raw.isna().sum()
missing_clean = clean.isna().sum()
duplicate_raw = int(raw.duplicated(subset=["tconst"]).sum()) if "tconst" in raw else 0
duplicate_clean = int(clean.duplicated(subset=["tconst"]).sum()) if "tconst" in clean else 0
a, b, c, d = st.columns(4)
a.metric("Rows retained", f"{clean_rows:,}", f"{clean_rows - raw_rows:+,} vs raw")
b.metric("Duplicate IDs", f"{duplicate_clean:,}", f"{duplicate_raw:,} in raw")
c.metric("Missing ratings", f"{int(missing_clean.get('averagerating', 0)):,}", "kept as missing")
d.metric("Missing runtimes", f"{int(missing_clean.get('runtimeminutes', 0)):,}", "kept as missing")

quality = pd.DataFrame({"Raw missing": missing_raw, "Cleaned missing": missing_clean}).fillna(0).astype(int)
quality["Missing after cleaning"] = quality["Cleaned missing"].apply(lambda n: "Yes" if n else "No")
quality.index.name = "Column"
st.markdown('<div class="output-label">Notebook output · missing values by column</div>', unsafe_allow_html=True)
st.dataframe(quality.reset_index(), use_container_width=True, hide_index=True)

left, right = st.columns([1.05, 1])
with left:
    miss = pd.DataFrame({"Raw": missing_raw, "Cleaned": missing_clean}).fillna(0).astype(int)
    miss.index.name = "Field"
    miss = miss.reset_index().melt(id_vars="Field", var_name="Dataset", value_name="Missing values")
    fig = px.bar(miss, x="Field", y="Missing values", color="Dataset", barmode="group",
                 color_discrete_map={"Raw": "#a8b4c5", "Cleaned": COLORS["teal"]}, title="Missing values by field")
    st.plotly_chart(figure_layout(fig, 360), use_container_width=True)
with right:
    st.markdown("#### What the cleaning stage does")
    st.markdown("- Standardizes column names to lowercase snake case.\n- Trims and normalizes text while preserving accented letters.\n- Labels missing genres as **Unknown**.\n- Converts year, runtime, rating and votes to numeric types.\n- Sets out-of-range ratings, runtimes and negative votes to missing.\n- Removes duplicate IMDb IDs and keeps the 2016–2025 period.")
    st.markdown('<div class="note">Missing ratings, votes and runtimes remain missing. Each EDA calculation uses only the rows relevant to that measure.</div>', unsafe_allow_html=True)

st.markdown('<div class="output-label">Notebook output · cleaned numeric summary</div>', unsafe_allow_html=True)
st.dataframe(clean.select_dtypes(include="number").describe().T.reset_index(names="Column"), use_container_width=True, hide_index=True)

with st.expander("Cleaned dataset · all records", expanded=True):
    st.dataframe(clean, use_container_width=True, height=430, hide_index=True)
    st.download_button("Download cleaned CSV", clean.to_csv(index=False).encode("utf-8"), "imdb_movies_cleaned.csv", "text/csv", key="clean-download")

# Stage 3: EDA
section("03 · DISCOVERY", "Exploratory analysis", "Eight questions from the EDA notebook, recalculated from the cleaned CSV so charts always reflect the supplied data.", COLORS["violet"], "exploratory-analysis")
df = clean.copy()
numeric_columns = ["startyear", "runtimeminutes", "averagerating", "numvotes"]
for column in numeric_columns:
    if column in df:
        df[column] = pd.to_numeric(df[column], errors="coerce")
df["log_votes"] = (df["numvotes"] + 1).map(lambda v: __import__("math").log(v) if pd.notna(v) else float("nan"))

valid_ratings = df["averagerating"].dropna()
valid_runtime = df["runtimeminutes"].dropna()
valid_votes = df["numvotes"].dropna()
m1, m2, m3, m4 = st.columns(4)
m1.metric("Average IMDb rating", f"{valid_ratings.mean():.2f}" if len(valid_ratings) else "—", f"median {valid_ratings.median():.1f}" if len(valid_ratings) else "")
m2.metric("Median runtime", f"{valid_runtime.median():.0f} min" if len(valid_runtime) else "—", f"{len(valid_runtime):,} records")
m3.metric("Median IMDb votes", f"{valid_votes.median():,.0f}" if len(valid_votes) else "—", "votes are highly skewed")
m4.metric("Distinct genres", f"{df['genres'].fillna('Unknown').str.split(',').explode().nunique():,}", "after splitting genre labels")

with st.expander("Notebook outputs · distributions of rating, runtime and votes", expanded=True):
    d1, d2 = st.columns(2)
    with d1:
        fig = px.histogram(df, x="averagerating", nbins=20, marginal="box", color_discrete_sequence=[COLORS["blue"]], title="IMDb rating distribution")
        st.plotly_chart(figure_layout(fig, 350), use_container_width=True)
    with d2:
        fig = px.histogram(df, x="runtimeminutes", nbins=20, marginal="box", color_discrete_sequence=[COLORS["teal"]], title="Runtime distribution")
        st.plotly_chart(figure_layout(fig, 350), use_container_width=True)
    fig = px.histogram(df, x="log_votes", nbins=20, color_discrete_sequence=[COLORS["amber"]], title="IMDb votes distribution · log scale")
    st.plotly_chart(figure_layout(fig, 320), use_container_width=True)

st.markdown("#### The questions")

# 1 & 2: annual volume and genre frequency
yearly = df.dropna(subset=["startyear"]).groupby("startyear").size().rename("Movie count").reset_index()
genre_df = df.assign(genre=df["genres"].fillna("Unknown").str.split(",")).explode("genre")
genre_df["genre"] = genre_df["genre"].str.strip()
genre_counts = genre_df["genre"].value_counts().head(10).rename_axis("Genre").reset_index(name="Movie count")
row1a, row1b = st.columns(2)
with row1a:
    fig = px.bar(yearly, x="startyear", y="Movie count", color_discrete_sequence=[COLORS["blue"]], title="1 · Which years had the most releases?")
    fig.update_xaxes(dtick=1, title="Release year")
    st.plotly_chart(figure_layout(fig), use_container_width=True)
    if not yearly.empty:
        peak = yearly.loc[yearly["Movie count"].idxmax()]
        st.caption(f"Peak: {int(peak['startyear'])} with {int(peak['Movie count'])} movies. Counts describe this filtered dataset, not industry-wide production.")
        st.dataframe(yearly.rename(columns={"startyear": "Release year"}), use_container_width=True, hide_index=True)
with row1b:
    fig = px.bar(genre_counts.sort_values("Movie count"), x="Movie count", y="Genre", orientation="h", color_discrete_sequence=[COLORS["teal"]], title="2 · Which genres appear most often?")
    st.plotly_chart(figure_layout(fig), use_container_width=True)
    if not genre_counts.empty:
        st.caption(f"Most common: {genre_counts.iloc[0]['Genre']} ({int(genre_counts.iloc[0]['Movie count'])} titles). Multi-genre movies count once for each genre.")
        st.dataframe(genre_counts, use_container_width=True, hide_index=True)

# 3 & 4: genre ratings, annual rating trend
genre_rating = (genre_df.dropna(subset=["averagerating"]).groupby("genre")
                .agg(movie_count=("tconst", "size"), average_rating=("averagerating", "mean"))
                .query("movie_count >= 50").sort_values("average_rating", ascending=False).head(5).reset_index())
rating_year = df.dropna(subset=["startyear", "averagerating"]).groupby("startyear")["averagerating"].mean().reset_index()
row2a, row2b = st.columns(2)
with row2a:
    fig = px.bar(genre_rating.sort_values("average_rating"), x="average_rating", y="genre", orientation="h", color_discrete_sequence=[COLORS["violet"]], title="3 · Highest-rated genres · 50+ titles")
    fig.update_xaxes(range=[0, 10], title="Average IMDb rating")
    st.plotly_chart(figure_layout(fig), use_container_width=True)
    st.caption("The 50-title threshold reduces small-sample effects. Average ratings do not establish why genres differ.")
    st.dataframe(genre_rating.rename(columns={"genre": "Genre", "movie_count": "Movies", "average_rating": "Average rating"}), use_container_width=True, hide_index=True)
with row2b:
    fig = px.line(rating_year, x="startyear", y="averagerating", markers=True, color_discrete_sequence=[COLORS["teal"]], title="4 · How did average ratings change by year?")
    fig.update_xaxes(dtick=1, title="Release year")
    fig.update_yaxes(title="Average rating", range=[0, 10])
    st.plotly_chart(figure_layout(fig), use_container_width=True)
    st.caption("Recent years may have smaller samples and ratings that are still collecting votes.")
    st.dataframe(rating_year.rename(columns={"startyear": "Release year", "averagerating": "Average rating"}), use_container_width=True, hide_index=True)

# 5 & 6: most votes and highest rated with threshold
top_votes = df.dropna(subset=["numvotes"]).nlargest(10, "numvotes")
top_rated = df[df["numvotes"] >= 10000].nlargest(10, "averagerating")
row3a, row3b = st.columns(2)
with row3a:
    fig = px.bar(top_votes.sort_values("numvotes"), x="numvotes", y="primarytitle", orientation="h", color_discrete_sequence=[COLORS["blue"]], title="5 · Most-voted movies")
    fig.update_xaxes(title="IMDb votes")
    fig.update_yaxes(title="")
    st.plotly_chart(figure_layout(fig, 440), use_container_width=True)
    st.caption("Vote count represents IMDb audience attention, not movie quality.")
    st.dataframe(top_votes[["primarytitle", "startyear", "averagerating", "numvotes"]].rename(columns={"primarytitle": "Movie", "startyear": "Year", "averagerating": "Rating", "numvotes": "IMDb votes"}), use_container_width=True, hide_index=True)
with row3b:
    fig = px.bar(top_rated.sort_values("averagerating"), x="averagerating", y="primarytitle", orientation="h", color_discrete_sequence=[COLORS["violet"]], title="6 · Highest-rated · 10,000+ votes")
    fig.update_xaxes(title="IMDb rating", range=[0, 10])
    fig.update_yaxes(title="")
    st.plotly_chart(figure_layout(fig, 440), use_container_width=True)
    st.caption("The minimum vote threshold helps avoid very small-vote ratings; the title alias filter can still include non-Hollywood films.")
    st.dataframe(top_rated[["primarytitle", "startyear", "averagerating", "numvotes"]].rename(columns={"primarytitle": "Movie", "startyear": "Year", "averagerating": "Rating", "numvotes": "IMDb votes"}), use_container_width=True, hide_index=True)

# 7 & 8: runtime association and genre vote medians
runtime_data = df.dropna(subset=["runtimeminutes", "averagerating"])
runtime_corr = runtime_data[["runtimeminutes", "averagerating"]].corr().iloc[0, 1] if len(runtime_data) > 1 else float("nan")
genre_votes = (genre_df.dropna(subset=["numvotes"]).groupby("genre")["numvotes"].median()
               .nlargest(10).sort_values().rename("Median IMDb votes").reset_index())
row4a, row4b = st.columns(2)
with row4a:
    fig = px.scatter(runtime_data, x="runtimeminutes", y="averagerating", hover_name="primarytitle",
                     color="averagerating", color_continuous_scale="Teal", opacity=.72,
                     title="7 · Does runtime relate to rating?")
    fig.update_xaxes(title="Runtime (minutes)")
    fig.update_yaxes(title="IMDb rating", range=[0, 10])
    st.plotly_chart(figure_layout(fig), use_container_width=True)
    st.caption(f"Pearson correlation: {runtime_corr:.2f}. This is an association, not evidence of causation." if pd.notna(runtime_corr) else "Not enough paired runtime and rating records to calculate correlation.")
with row4b:
    fig = px.bar(genre_votes, x="Median IMDb votes", y="genre", orientation="h", color_discrete_sequence=[COLORS["amber"]], title="8 · Genres with the highest median votes")
    st.plotly_chart(figure_layout(fig), use_container_width=True)
    st.caption("Median vote counts are less affected by a few blockbuster titles than averages.")
    st.dataframe(genre_votes.rename(columns={"genre": "Genre"}), use_container_width=True, hide_index=True)

st.markdown("#### Relationships across numeric fields")
corr_cols = [c for c in ["runtimeminutes", "averagerating", "numvotes"] if c in df]
corr = df[corr_cols].corr()
fig = px.imshow(corr, text_auto=".2f", zmin=-1, zmax=1, color_continuous_scale="Blues", aspect="auto", title="Pearson correlation matrix")
st.plotly_chart(figure_layout(fig, 350), use_container_width=True)
st.dataframe(corr.reset_index(names="Measure"), use_container_width=True, hide_index=True)
st.markdown(
    '<div class="note"><b>How to read this</b> &nbsp; Correlations describe how two measures move together; they do not show cause and effect. Vote counts are strongly skewed, so the Pearson relationships involving votes can be influenced by blockbusters.</div>',
    unsafe_allow_html=True,
)

st.markdown("#### Takeaways & scope")
if not yearly.empty and not genre_counts.empty and not valid_ratings.empty:
    top_genre = genre_counts.iloc[0]
    peak_row = yearly.loc[yearly["Movie count"].idxmax()]
    st.markdown(
        f"- The largest release-year group is **{int(peak_row['startyear'])}** ({int(peak_row['Movie count'])} records).\n"
        f"- **{top_genre['Genre']}** is the most common genre ({int(top_genre['Movie count'])} genre assignments).\n"
        f"- Average rating is **{valid_ratings.mean():.2f}** (median **{valid_ratings.median():.1f}**); missing ratings are excluded from rating calculations.\n"
        "- The US + English title record is only a proxy for Hollywood focus and may include international titles.\n"
        "- IMDb ratings and votes represent IMDb contributors; there is no budget or box-office data in this dataset."
    )

st.markdown("---")
st.markdown('<p class="small-caption">Built from the project CSVs and the three source notebooks · IMDb title datasets · 2016–2025</p>', unsafe_allow_html=True)
