ct_income_dashboard.py

import streamlit as st
import pandas as pd
import altair as alt

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/iantonios/dsc205/refs/heads/main/CT-towns-income-census-2020.csv"
    df = pd.read_csv(url)
    return df

df = load_data()

st.title("CT Towns Median Household Income Dashboard")

st.sidebar.write("Columns:", df.columns.tolist())

county_col = "County"      
town_col = "Town"          
income_col = "Median Household Income"  

counties = df[county_col].dropna().unique().tolist()
selected_county = st.sidebar.selectbox("Select a County", sorted(counties))

df_county = df[df[county_col] == selected_county]

st.subheader(f"Towns in {selected_county} County")
st.dataframe(df_county[[town_col, income_col]], width=800, height=200)

min_income = int(df[income_col].min())
max_income = int(df[income_col].max())

income_range = st.sidebar.slider(
    "Select income range (USD)",
    min_value=min_income,
    max_value=max_income,
    value=(min_income, max_income),
    step=1000
)

low, high = income_range
df_income = df[(df[income_col] >= low) & (df[income_col] <= high)]

st.subheader(f"Towns with Median Income between ${low:,} and ${high:,}")
st.dataframe(df_income[[town_col, county_col, income_col]], width=800, height=200)

st.subheader("Top 5 and Bottom 5 Towns by Median Household Income")

df_sorted = df.sort_values(by=income_col)

bottom5 = df_sorted.head(5)

top5 = df_sorted.tail(5)

df_plot = pd.concat([bottom5, top5])

chart = (
    alt.Chart(df_plot)
    .mark_bar()
    .encode(
        x=alt.X(f"{town_col}:N", sort=None, title="Town / City"),
        y=alt.Y(f"{income_col}:Q", title="Median Household Income (USD)"),
        color=alt.condition(
            alt.datum[income_col] <= df_plot[income_col].median(),
            alt.value("steelblue"),
            alt.value("orange")
        ),
        tooltip=[town_col, county_col, income_col]
    )
    .properties(width=800, height=400)
)

st.altair_chart(chart, use_container_width=False)
