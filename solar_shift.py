import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Explore!",
    layout="wide"
)

left_col, middle_col, right_col = st.columns([1, 2, 1])

@st.cache_data
def get_data():
    return pd.read_csv("all_the_cases.csv")

data = get_data()

with left_col:
    st.subheader("Dive into")
    hs = st.multiselect("Household size", data["household_size"].unique())
    locs = st.multiselect("Location", data["location"].unique())
    st.subheader("Compare across")
    groups = []
    if st.checkbox("Heater type", value=False):
        groups.append("heater_type")

f_data = data.copy()

if len(hs) > 0:
    f_data = f_data[f_data["household_size"].isin(hs)]

if len(locs) > 0:
    f_data = f_data[f_data["location"].isin(locs)]

kwargs = {}

if len(groups) > 0:
    kwargs["color"] = groups.pop(0)

if len(groups) > 0:
    kwargs["symbol"] = groups.pop(0)

chart = px.scatter(
    f_data,
    x='emissions_total',
    y='annual_energy_cost',
    # tooltip=["has_solar", "control_type", "tariff_type"],
    **kwargs
)

with middle_col:
    st.plotly_chart(chart, use_container_width=True)