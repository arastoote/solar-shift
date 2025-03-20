import streamlit as st
from streamlit.components.v1 import html
import pandas as pd
import plotly.express as px
import time
from PIL import Image

from graphics import (
    draw_logo,
    apply_chart_formatting
)

from data_preprocessing import (
    load_and_preprocess_data,
    metrics,
    groups,
    process_system_data
)

im = Image.open("favicon.png")

st.set_page_config(
    page_title="Explore!",
    layout="wide",
    page_icon=im
)

st.html("""
    <style>
        .stMainBlockContainer {
            max-width:90vw;
        }
    </style>
    """
)

st.markdown("""
<style>

.block-container
{
    padding-top: 1rem;
    padding-bottom: 0rem;
    margin-top: 1rem;
}

</style>
""", unsafe_allow_html=True)


@st.cache_data
def get_data():
    return load_and_preprocess_data()


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
    st.markdown("<h1 style='text-align: center; color: #FFA000;'>Welcome to the Solar Shift Explorer!</h1>",
                unsafe_allow_html=True)

    st.markdown(draw_logo(), unsafe_allow_html=True)

    a, b, c, d = st.columns([0.4, 1, 1, 0.4])
    with b:
        if st.button("Explore a variety of hot water solutions"):
            with st.empty():
                html(f"<script>{switch(2)}</script>", height=0)
                time.sleep(1)
                html(f"<div></div>", height=0)
    with c:
        if st.button("Compare two hot water solutions side-by-side"):
            with st.empty():
                html(f"<script>{switch(3)}</script>", height=0)
                time.sleep(1)
                html(f"<div></div>", height=0)

with about:
    st.markdown("Here we will describe the project.")

with explore:

    with st.container():
        st.markdown(
            "<h3 style='text-align: center; color: #FFA000;'>Explore hot water system configurations</h1>",
            unsafe_allow_html=True)

    with st.container():

        left, gap, right = st.columns([1.75, 0.25, 5])

        with left:
            st.markdown("<br><br><br>", unsafe_allow_html=True)

            with st.expander("Describe your house", expanded=False):
                hs = st.multiselect("Household size", data["Household occupants"].unique(), default=3)
                locs = st.multiselect("Location", data["Location"].unique())
                patterns = st.multiselect("Hot water usage pattern", data["Hot water usage pattern"].unique())
                tariffs = st.multiselect("Tariff", data["Tariff"].unique())
                solar = st.multiselect("Solar", data["Solar"].unique())
            with st.expander("Choose a heater"):
                heater = st.multiselect("Heater type", data["Heater"].unique())
                control = st.multiselect("Control type", data["Heater control"].unique())
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

            if len(patterns) > 0:
                f_data = f_data[f_data["Hot water usage pattern"].isin(patterns)]

            if len(tariffs) > 0:
                f_data = f_data[f_data["Tariff"].isin(tariffs)]

            if len(solar) > 0:
                f_data = f_data[f_data["Solar"].isin(solar)]

            if len(control) > 0:
                f_data = f_data[f_data["Heater control"].isin(control)]

            if len(heater) > 0:
                f_data = f_data[f_data["Heater"].isin(heater)]

            show_data = f_data.loc[:,groups + metrics]

        with right:

            chart = px.strip(
                f_data,
                y=metric,
                x=x,
                color=color
            )

            chart.update_traces(width=2.0)

            apply_chart_formatting(chart)

            st.plotly_chart(chart, use_container_width=True)

    with st.container():

        table_groups = list(set((x, color)))
        summarise = st.radio("", ["Average", "Show all"])
        if len(table_groups) > 0 and summarise == "Average":
            agg_dict = {col: "mean" for col in metrics}
            show_data = show_data.groupby(table_groups, as_index=False).agg(agg_dict)
        show_data = show_data.sort_values("Net present cost ($)")
        st.dataframe(show_data.style.format(precision=2), hide_index=True)

with (compare):
    def create_select(group, default, version):
        options = list(data[group].unique())
        index = options.index(default)
        key = f"select-{group}-{version}"
        return st.selectbox(group, options, index=index, key=key)

    st.markdown(
        "<h3 style='text-align: center; color: #FFA000;'>Compare two hot water systems in detail</h1>",
        unsafe_allow_html=True)

    left, gap, right = st.columns([1.75, 0.25, 5])

    with left:
        with st.expander("System one details", expanded=True):
            location_one = create_select("Location", "Sydney", "one")
            occupants_one = create_select("Household occupants", 3, "one")
            usage_pattern_one = create_select("Hot water usage pattern",
                                              "Morning and evening only", "one")
            solar_one = create_select("Solar", True, "one")
            heater_one = create_select("Heater", "Heat Pump", "one")
            tariff_one = create_select("Tariff", "Flat rate", "one")
            control_one = create_select("Heater control", "Run as needed (no control)",
                                        "one")

        with st.expander("System two details"):
            location_two = create_select("Location", "Sydney", "two")
            occupants_two = create_select("Household occupants", 3, "two")
            usage_pattern_two = create_select("Hot water usage pattern",
                                              "Morning and evening only", "two")
            solar_two = create_select("Solar", True, "two")
            heater_two = create_select("Heater", "Electric", "two")
            tariff_two = create_select("Tariff", "Flat rate", "two")
            control_two = create_select("Heater control",
                                        "Run as needed (no control)",
                                        "two")


    with right:

        system_one_data = process_system_data(
            data,
            location_one,
            occupants_one,
            usage_pattern_one,
            tariff_one,
            heater_one,
            control_one,
            solar_one
        )

        system_one_data.insert(0, "System", "One")

        system_two_data = process_system_data(
            data,
            location_two,
            occupants_two,
            usage_pattern_two,
            tariff_two,
            heater_two,
            control_two,
            solar_two
        )

        system_two_data.insert(0, "System", "Two")

        system_comparison_data = pd.concat([system_one_data, system_two_data])

        with st.expander("Simple financial comparison", expanded=False):

            columns_to_plot = ["Net present cost ($)"]

            bar_chart = px.bar(
                system_comparison_data, x="System", y=columns_to_plot, barmode="group"
            )

            apply_chart_formatting(
                bar_chart, yaxes_title="Net present cost ($)", show_legend=False, height=200
            )

            st.plotly_chart(
                bar_chart,
                use_container_width=True,
                key="Net present cost ($)",
            )

        with st.expander("Spending", expanded=True):

            columns_to_plot = [
                "Up front cost ($)",
                "Rebates ($)",
                "Annual cost ($/yr)",
                "Annual lost FiT revenue ($/yr)"
            ]

            bar_chart = px.bar(
                system_comparison_data, x="System", y=columns_to_plot, barmode="group", height=200
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
                system_comparison_data, x="System", y=columns_to_plot, barmode="group", height=200
            )

            apply_chart_formatting(
                bar_chart, yaxes_title="CO2 emissions (tons/yr)", show_legend=False
            )

            st.plotly_chart(
                bar_chart,
                use_container_width=True,
                key="Environmental",
            )

        with st.expander("Tabular details comparison", expanded=False):

            comp = pd.DataFrame({
                "Option": ["Location", "Household occupants", "Hot water usage pattern", "Solar", "Heater", "Tariff", "Heater control"],
                "System one": [location_one, occupants_one, usage_pattern_one, solar_one, heater_one, tariff_one, control_one],
                "System two": [location_two, occupants_two, usage_pattern_two, solar_two, heater_two, tariff_two, control_two],
            })

            st.dataframe(comp, hide_index=True)

        with st.expander("Tabular performance comparison", expanded=False):

            column_config = {
                "Location": None,
                "Household occupants": None,
                "Tariff": None,
                "Heater": None,
                "Heater control": None,
                "Solar": None,
                "Hot water usage pattern": None

            }

            st.dataframe(system_comparison_data, hide_index=True, column_config=column_config)

        with st.container():
            st.info(
                '''
                Note: Some Heater/Heater control/Tariff combinations are not available. 
                If no inputs are returned try adjusting the selected control or tariff option.
                Read further about the available options in the **Details** tab.
                '''
            )

with detailed_info:
    st.markdown("Here we can put detailed notes such as describing solar soaking.")


