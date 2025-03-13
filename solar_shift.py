import streamlit as st
from streamlit.components.v1 import html
import pandas as pd
import plotly.express as px
import time

from graphics import (
    draw_logo,
    apply_chart_formatting
)

from data_preprocessing import (
    load_and_preprocess_data,
    metrics,
    groups,
    other,
    process_system_data
)

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


def create_select(group, default, version):
    options = list(data[group].unique())
    index = options.index(default)
    key = f"select-{group}-{version}"
    return st.selectbox(group, options, index=index, key=key, label_visibility="collapsed")


data = get_data()

home, about, explore, compare, detailed_info = \
    st.tabs(["Home", "About", "Explore", "Compare", "Details"])


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

with about:
    st.markdown("Here we will describe the project.")

with explore:

    st.markdown(
        "<h3 style='text-align: center; color: #FFA000;'>Explore hot water system configurations</h1>",
        unsafe_allow_html=True)

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
                index = groups.index("Heater")
                x = st.selectbox("Side-by-side", groups, index=index)
                color = st.selectbox("Color", groups, index=index)
                index = metrics.index("Annual cost ($/yr)")
                metric = st.selectbox("Comparison metric", metrics, index=index)

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

        show_data = f_data.loc[:,other + groups + metrics]

    with top:

        chart = px.strip(
            f_data,
            y=metric,
            x=x,
            color=color
        )

        chart.update_traces(width=2.0)

        apply_chart_formatting(chart)

        st.plotly_chart(chart, use_container_width=True)

    with bottom:
        table_groups = list(set((x, color)))
        summarise = st.radio("", ["Average", "Show all"])
        if len(table_groups) > 0 and summarise == "Average":
            agg_dict = {col: "mean" for col in metrics}
            show_data = show_data.groupby(table_groups, as_index=False).agg(agg_dict)
        show_data = show_data.sort_values("Net present cost ($)")
        st.dataframe(show_data.style.format(precision=2), hide_index=True)

with (compare):
    st.markdown(
        "<h3 style='text-align: center; color: #FFA000;'>Compare two hot water systems in detail</h1>",
        unsafe_allow_html=True)

    bar_chart = st.container()
    system_config = st.container()
    
    label_width = 0.5
    system_one_width = 1
    system_two_width = 1

    with system_config:
        with st.container():
            label, left, right = st.columns([label_width, system_one_width, system_two_width])

            with left:
                st.markdown("System One")

            with right:
                st.markdown("System One")

    with st.container():
        label, left, right = st.columns([label_width, system_one_width, system_two_width])

        with label:
            st.markdown("Location")

        with left:
            location_one = create_select("Location", "Sydney", "one")

        with right:
            location_two = create_select("Location", "Sydney", "two")

    with st.container():
        label, left, right = st.columns([label_width, system_one_width, system_two_width])
        with label:
            st.markdown("Household occupants")
        with left:
            occupants_one = create_select("Household occupants", 3, "one")
        with right:
            occupants_two = create_select("Household occupants", 3, "two")

        label, left, right = st.columns([label_width, system_one_width, system_two_width])
        with label:
            st.markdown("Tariff")
        with left:
            tariff_one = create_select("Tariff", "flat", "one")
        with right:
            tariff_two = create_select("Tariff", "CL", "two")

        label, left, right = st.columns([label_width, system_one_width, system_two_width])
        with label:
            st.markdown("Heater")
        with left:
            heater_one = create_select("Heater", "Heat Pump", "one")
        with right:
            heater_two = create_select("Heater", "Electric", "two")

        label, left, right = st.columns([label_width, system_one_width, system_two_width])
        with label:
            st.markdown("Heater control")
        with left:
            control_one = create_select("Heater control", "GS", "one")
        with right:
            control_two = create_select("Heater control", "CL3", "two")

        label, left, right = st.columns([label_width, system_one_width, system_two_width])
        with label:
            st.markdown("Solar")
        with left:
            solar_one = create_select("Solar", True, "one")
        with right:
            solar_two = create_select("Solar", True, "two")


    with bar_chart:

        system_one_data = process_system_data(
            data,
            location_one,
            occupants_one,
            tariff_one,
            heater_one,
            control_one,
            solar_one
        )

        system_one_data["System"] = "One"

        system_two_data = process_system_data(
            data,
            location_two,
            occupants_two,
            tariff_two,
            heater_two,
            control_two,
            solar_two
        )

        system_two_data["System"] = "Two"

        system_comparison_data = pd.concat([system_one_data, system_two_data])

        with st.expander("Simple financial comparison", expanded=True):

            columns_to_plot = ["Net present cost ($)"]

            bar_chart = px.bar(
                system_comparison_data, x="System", y=columns_to_plot, barmode="group"
            )

            apply_chart_formatting(
                bar_chart, yaxes_title="Net present cost ($)", show_legend=False
            )

            st.plotly_chart(
                bar_chart,
                use_container_width=True,
                key="Net present cost ($)"
            )

        with st.expander("Spending", expanded=False):

            columns_to_plot = [
                "Up front cost ($)",
                "Rebates ($)",
                "Annual cost ($/yr)",
                "Annual lost FiT revenue ($/yr)"
            ]

            bar_chart = px.bar(
                system_comparison_data, x="System", y=columns_to_plot, barmode="group"
            )

            apply_chart_formatting(bar_chart, yaxes_title="Costs")

            st.plotly_chart(
                bar_chart,
                use_container_width=True,
                key="Spending"
            )

        with st.expander("Environmental comparison", expanded=False):

            columns_to_plot = ["CO2 emissions (tons/yr)"]

            bar_chart = px.bar(
                system_comparison_data, x="System", y=columns_to_plot, barmode="group"
            )

            apply_chart_formatting(
                bar_chart, yaxes_title="CO2 emissions (tons/yr)", show_legend=False
            )

            st.plotly_chart(
                bar_chart,
                use_container_width=True,
                key="Environmental"
            )

with detailed_info:
    st.markdown("Here we can but detailed notes such as describing solar soaking.")


