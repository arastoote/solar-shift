import streamlit as st
from streamlit.components.v1 import html
import pandas as pd
import plotly.express as px
import time

from graphics import draw_logo
from data_preprocessing import load_and_preprocess_data, metrics, groups

st.set_page_config(
    page_title="Explore!",
    layout="wide",
)

st.html("""
    <style>
        .stMainBlockContainer {
            max-width:80rem;
        }
    </style>
    """
)


@st.cache_data
def get_data():
    return load_and_preprocess_data()


data = get_data()

home, explore, compare = st.tabs(["Home", "Explore", "Compare"])


def switch(tab):
    return f"""
var tabGroup = window.parent.document.getElementsByClassName("stTabs")[0]
var tab = tabGroup.getElementsByTagName("button")
tab[{tab}].click()
"""


with home:
    # st.header("Welcome to the Solar Shift Explorer!")
    st.markdown("<h1 style='text-align: center; color: #FFA000;'>Welcome to the Solar Shift Explorer!</h1>",
                unsafe_allow_html=True)

    st.markdown(draw_logo(), unsafe_allow_html=True)

    a, b, c, d = st.columns([0.4, 1, 1, 0.4])
    with b:
        if st.button("Explore a variety of hot water solutions"):
            with st.empty():
                html(f"<script>{switch(1)}</script>", height=0)
                time.sleep(1)
                html(f"<div></div>", height=0)
    with c:
        if st.button("Compare two hot water solutions side-by-side"):
            with st.empty():
                html(f"<script>{switch(2)}</script>", height=0)
                time.sleep(1)
                html(f"<div></div>", height=0)

with explore:
    top = st.container()
    middle = st.container()
    bottom = st.container()

    with middle:

        middle_left, middle_middle, middle_right = st.columns([1, 1, 1])

        with middle_left:
            with st.expander("Describe your house"):
                hs = st.multiselect("Household size", data["Household occupants"].unique(), default=3)
                locs = st.multiselect("Location", data["Location"].unique())
                tariffs = st.multiselect("Tariff", data["Tariff"].unique())
                solar = st.multiselect("Solar", data["Solar"].unique())
        with middle_middle:
            with st.expander("Choose a heater"):
                heater = st.multiselect("Heater type", data["Heater"].unique())
                control = st.multiselect("Control type", data["Heater control"].unique())
        with middle_right:
            with st.expander("Compare"):
                x = st.selectbox("Side-by-side", groups, index=3)
                color = st.selectbox("Color", groups, index=3)
                metric = st.selectbox("Comparison metric", metrics, index=1)

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

        show_data = f_data.loc[:, groups + metrics]

    with top:

        chart = px.strip(
            f_data,
            y=metric,
            x=x,
            color=color
        )

        chart.update_traces(width=2.0)

        chart.update_layout(
            margin={
                't': 20,
                'b': 20,
            },
            legend=dict(
                font=dict(size=18)
            ),
            legend_title_text=""
        )
        chart.update_xaxes(
            tickfont=dict(size=18),
            title_font=dict(size=18),
            title_text=""
        )
        chart.update_yaxes(
            tickfont=dict(size=18),
            title_font=dict(size=18),
        )


        st.plotly_chart(chart, use_container_width=True)


    with bottom:
        table_groups = list(set((x, color)))
        summarise = st.radio("", ["Average", "Show all"])
        if len(table_groups) > 0 and summarise == "Average":
            agg_dict = {col: "mean" for col in metrics}
            show_data = show_data.groupby(table_groups, as_index=False).agg(agg_dict)
        show_data = show_data.sort_values("Annual cost ($/yr)")
        st.dataframe(show_data.style.format(precision=2), hide_index=True)
