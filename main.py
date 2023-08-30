import pandas as pd
import plotly.express as px
import streamlit as st
# GDP of each country and region(1960-2020)

# Set streamlit page configuration
st.set_page_config(page_title="GDP from 1960 to 2020",
                   page_icon=":bar_chart:",
                   layout="wide"
)

# Read excel file with pandas
@st.cache_data
def get_data_from_excel():
  df = pd.read_excel(
      io='GDP_1960_2020.xlsx',
      engine='openpyxl',
      skiprows=None,
      usecols='B:G',
      nrows=10135
  )
  return df
df = get_data_from_excel()

# - - - - SIDEBAR - - - -
st.sidebar.header("Please Filter by Country, Year, Rank, and Continent Here:")
countries = st.sidebar.multiselect(
    "Select the Country:",
    options=df["country"].unique(),
    default=df["country"].unique()
)

years = st.sidebar.multiselect(
    "Select the Year:",
    options=df["year"].unique(),
    default=df["year"].unique()
)

ranks = st.sidebar.multiselect(
    "Select the Rank:",
    options=df["rank"].unique(),
    default=df["rank"].unique()
)

continents = st.sidebar.multiselect(
    "Select the Continent:",
    options=df["continent"].unique(),
    default=df["continent"].unique()
)

df_selection = df.query(
    "year == @years & rank == @ranks & country == @countries & continent == @continents"
)

st.dataframe(df_selection)

# GDP PERCENTAGE BY COUNTRY
bar_chart = (
    df_selection.groupby(by=["country"]).sum()[["gdp_percent"]].sort_values(by="gdp_percent")
)
fig_gdp = px.bar(
    bar_chart,
    x="gdp_percent",
    y=bar_chart.index,
    orientation="h",
    title="<b>GDP by country<b>",
    color_discrete_sequence=["#0083B8"],
    template="plotly_white",
    color='gdp_percent',
)
fig_gdp.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

# RANKING BY YEAR CHART
ranking_per_country = df_selection.groupby(by="year").sum()[["rank"]]
fig_ranking = px.bar(
  ranking_per_country,
  x=ranking_per_country.index,
  y="rank",
  title="<b>Ranking by year</b>",
  color_discrete_sequence=["#0083B8"],
  template="plotly_white",
)
fig_ranking.update_layout(
  xaxis=dict(tickmode="linear"),
  plot_bgcolor="rgba(0,0,0,0)",
  yaxis=(dict(showgrid=False)),
)

# PLACE BAR CHARTS NEXT TO EACHOTHER
left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_gdp, use_container_width=True)
right_column.plotly_chart(fig_ranking, use_container_width=True)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """

st.markdown(hide_st_style, unsafe_allow_html=True)