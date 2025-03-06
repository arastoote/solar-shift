import streamlit as st
from streamlit.components.v1 import html
import pandas as pd
import plotly.express as px
import time

st.set_page_config(
    page_title="Explore!",
    layout="wide"
)

@st.cache_data
def get_data():
    return pd.read_csv("all_the_cases.csv")

data = get_data()

groups = [
    "location",
    "household_size",
    "heater_type",
    "tariff_type",
    "control_type",
    "has_solar"
]

home, explore, compare = st.tabs(["Home", "Explore", "Compare"])


def switch(tab):
    return f"""
var tabGroup = window.parent.document.getElementsByClassName("stTabs")[0]
var tab = tabGroup.getElementsByTagName("button")
tab[{tab}].click()
"""


with home:
    # st.header("Welcome to the Solar Shift Explorer!")
    st.markdown("<h1 style='text-align: center;'>Welcome to the Solar Shift Explorer!</h1>",
                unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>We've simulated the operation of thousands of hot water heaters. </h1>",
                unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Start exploring and find a system that lowers your bills and carbon emissions.</h1>",
                unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'> better intro text/graphics </h1>",
                unsafe_allow_html=True)
    a, b, c = st.columns([1.25, 1, 1])
    with b:
        if st.button("Explore Now"):
            with st.empty():
                html(f"<script>{switch(1)}</script>", height=0)
                time.sleep(1)
                html(f"<div></div>", height=0)

with explore:
    top = st.container()
    bottom = st.container()
    with top:

        left_col, padding_left, right_col, padding = st.columns([3, 0.5, 7, 0.5])

        with left_col:
            with st.expander("Your house", expanded=True):
                hs = st.multiselect("Household size", data["household_size"].unique(), default=3)
                locs = st.multiselect("Location", data["location"].unique())
                tariffs = st.multiselect("Tariff", data["tariff_type"].unique())
                solar = st.multiselect("Solar", data["has_solar"].unique())
            with st.expander("Heater choices"):
                heater = st.multiselect("Heater type", data["heater_type"].unique())
                control = st.multiselect("Control type", data["control_type"].unique())
            # with st.expander("Plot comparisons"):
            #     x = st.selectbox("Side-by-side", groups, index=0)
            #     color = st.selectbox("Color", groups)

        f_data = data.copy()

        if len(hs) > 0:
            f_data = f_data[f_data["household_size"].isin(hs)]

        if len(locs) > 0:
            f_data = f_data[f_data["location"].isin(locs)]

        if len(tariffs) > 0:
            f_data = f_data[f_data["tariff_type"].isin(tariffs)]

        if len(solar) > 0:
            f_data = f_data[f_data["has_solar"].isin(solar)]

        if len(control) > 0:
            f_data = f_data[f_data["control_type"].isin(control)]

        if len(heater) > 0:
            f_data = f_data[f_data["heater_type"].isin(heater)]


    show_data = f_data.loc[:, [
            "location",
            "household_size",
            "heater_type",
            "tariff_type",
            "control_type",
            "has_solar",
            "annual_energy_cost",
            "emissions_total"
        ]
    ]


    with bottom:
        bl, bm, br, _ = st.columns([2.5, 2, 2, 1])
        with bm:
            x = st.selectbox("Side-by-side", groups, index=2)
        with br:
            color = st.selectbox("Color", groups, index=2)


    with top:
        chart = px.strip(
            f_data,
            y='annual_energy_cost',
            x=x,
            color=color
        )
        chart.update_traces(width=2.0)

        chart.update_layout(
            margin={
                't': 20,
                'b': 20,
            }
        )

        with right_col:
            st.plotly_chart(chart, use_container_width=True)


    with bottom:
        table_groups = list(set((x, color)))
        summarise = st.radio("", ["Average", "Show all"])
        if len(table_groups) > 0 and summarise == "Average":
            show_data = show_data.groupby(table_groups, as_index=False).agg(
                {"annual_energy_cost": "mean", "emissions_total": "mean"}
            )
        show_data = show_data.sort_values("annual_energy_cost")
        st.dataframe(show_data.style.format(precision=2), hide_index=True)
