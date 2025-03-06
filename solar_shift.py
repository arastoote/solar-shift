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
    data =  pd.read_csv("all_the_cases.csv")
    data = data.rename(
        columns={
            "location": "Location",
            "household_size": "Household occupants",
            "tariff_type": "Tariff",
            "control_type": "Heater control",
            "annual_energy_cost": "Cost ($/yr)",
            "heater_type": "Heater",
            "has_solar": "Solar",
            "emissions_total": "CO2 emissions (tons/yr)"
        }
    )
    data["Heater"] = data["Heater"].map(
        {
            "resistive": "Electric",
            "heat_pump": "Heat Pump",
            "solar_thermal": "Solar Thermal",
            "gas_instant": "Gas Instant",
            "gas_storage": "Gas Storage",
        }
    )
    return data

data = get_data()

groups = [
    "Location",
    "Household occupants",
    "Heater",
    "Tariff",
    "Heater control",
    "Solar"
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
    middle = st.container()
    bottom = st.container()

    with middle:

        middle_left, middle_middle, middle_right = st.columns([1, 1, 1])

        with middle_left:
            with st.expander("Your house"):
                hs = st.multiselect("Household size", data["Household occupants"].unique(), default=3)
                locs = st.multiselect("Location", data["Location"].unique())
                tariffs = st.multiselect("Tariff", data["Tariff"].unique())
                solar = st.multiselect("Solar", data["Solar"].unique())
        with middle_middle:
            with st.expander("Heater choices"):
                heater = st.multiselect("Heater type", data["Heater"].unique())
                control = st.multiselect("Control type", data["Heater control"].unique())
        with middle_right:
            with st.expander("Compare"):
                x = st.selectbox("Side-by-side", groups, index=2)
                color = st.selectbox("Color", groups, index=2)

        f_data = data.copy()

        if len(hs) > 0:
            f_data = f_data[f_data["Household occupants"].isin(hs)]

        if len(locs) > 0:
            f_data = f_data[f_data["Location"].isin(locs)]

        if len(tariffs) > 0:
            f_data = f_data[f_data["Tariff"].isin(tariffs)]

        if len(solar) > 0:
            f_data = f_data[f_data["Solar"].isin(solar)]

        if len(control) > 0:
            f_data = f_data[f_data["Heater control"].isin(control)]

        if len(heater) > 0:
            f_data = f_data[f_data["Heater"].isin(heater)]

        show_data = f_data.loc[:, [
                                      "Location",
                                      "Household occupants",
                                      "Heater",
                                      "Tariff",
                                      "Heater control",
                                      "Solar",
                                      "Cost ($/yr)",
                                      "CO2 emissions (tons/yr)"
                                  ]
                    ]

    with top:

        chart = px.strip(
            f_data,
            y='Cost ($/yr)',
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

        st.plotly_chart(chart, use_container_width=True)


    with bottom:
        table_groups = list(set((x, color)))
        summarise = st.radio("", ["Average", "Show all"])
        if len(table_groups) > 0 and summarise == "Average":
            show_data = show_data.groupby(table_groups, as_index=False).agg(
                {"Cost ($/yr)": "mean", "CO2 emissions (tons/yr)": "mean"}
            )
        show_data = show_data.sort_values("Cost ($/yr)")
        st.dataframe(show_data.style.format(precision=2), hide_index=True)
