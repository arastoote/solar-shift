import time

import streamlit as st
from streamlit.components.v1 import html
import pandas as pd
import plotly.express as px

from graphics.charts import apply_chart_formatting
from data_processing.data_processing import metrics, groups
from helpers.switch_tabs import make_tab_switch_button
from helpers.data_selectors import export_settings_to_compare_tab, build_interactive_data_filter
from data.system_configs import (
    create_basic_heat_pump_config,
    create_solar_electric
)


def render(data):
    """Renders the Compare tab contents."""

    contents_column, right_gap = st.columns([4, 2])

    with contents_column:
        st.markdown(
            "<h3 style='text-align: left; color: #FFA000;'>Tell us about your house:</h1>",
            unsafe_allow_html=True
        )

        data = data.copy()

        st.markdown("Complete the questions below and we will estimate your hot water heating costs.")

        st.markdown("Privacy", help="Please note your data is not stored by Solar Shift.")

        big_labels = {
            "Location": "Where is your house?",
            "Household occupants": "How many people live there?",
            "Hot water usage pattern": [
                    "When do you typically use most of your hot water?",
                    "(please see **Hot water usage patterns** section under the **Details** tab)"
                ],
            "Solar": "Do you have a solar elecricity system (PV)?",
            "Hot water billing type": "How do pay your bill for heating hot water?",
            "Heater": "What type of hot water heater do you have?",
            "Heater control": "Is your hot water heater being controlled?"
        }

        data, values = build_interactive_data_filter(data, key_version="one", big_labels=big_labels)

        # Add a column labeling the data as System One
        data.insert(0, "System", "Your current hot water system")

        st.markdown(
            "<br><h3 style='text-align: left; color: #FFA000;'>Your estimated hot water costs:</h1>",
            unsafe_allow_html=True
        )

        # Create cashflow plot.
        with st.expander("Spending summary", expanded=True):
            columns_to_plot = [
                "Up front cost ($)",
                "Rebates ($)",
                "Annual cost ($/yr)",
                "Decrease in solar export revenue ($/yr)"
            ]

            bar_chart = px.bar(
                data, x="System", y=columns_to_plot, text_auto=True, barmode="group", height=200
            )

            apply_chart_formatting(bar_chart, yaxes_title="Costs")

            st.plotly_chart(
                bar_chart,
                use_container_width=True,
                key="Spending simple"
            )


        # Create net present cost plot.
        with st.expander("Simple financial summary", expanded=False):
            columns_to_plot = ["Net present cost ($)"]

            bar_chart = px.bar(
                data, x="System", y=columns_to_plot, text_auto=True, barmode="group"
            )

            apply_chart_formatting(
                bar_chart, yaxes_title="Net present cost ($)", show_legend=False, height=200
            )

            st.plotly_chart(
                bar_chart,
                use_container_width=True,
                key="Net present cost ($) simple",
            )

        # Create CO2 plot.
        with st.expander("Environmental summary", expanded=False):
            columns_to_plot = ["CO2 emissions (tons/yr)"]

            bar_chart = px.bar(
                data, x="System", y=columns_to_plot, text_auto=True, barmode="group", height=200
            )

            apply_chart_formatting(
                bar_chart, yaxes_title="CO2 emissions (tons/yr)", show_legend=False
            )

            bar_chart.update_traces(
                texttemplate='%{y:.2f}',
            )

            st.plotly_chart(
                bar_chart,
                use_container_width=True,
                key="Environmental simple",
            )

        # Create table with system performance metrics.
        with st.expander("Tabular summary ", expanded=False):
            # This hides these columns.
            column_config = {
                "Location": None,
                "Household occupants": None,
                "Hot water billing type": None,
                "Heater": None,
                "Heater control": None,
                "Solar": None,
                "Hot water usage pattern": None
            }


            data = data.loc[:, ["System"] + groups + metrics]

            st.dataframe(data, hide_index=True, column_config=column_config)

        st.markdown(
            "<br><h3 style='text-align: left; color: #FFA000;'>Compare your hot water system with other options:</h1>",
            unsafe_allow_html=True
        )

        if None in values.values():
            prompt_to_complete_questions=True
        else:
            prompt_to_complete_questions=False

        heat_pump_config = create_basic_heat_pump_config(values.copy())
        make_tab_switch_button(
            text="Compare to a Heat Pump",
            prompt=prompt_to_complete_questions,
            help="If using 'Active matching to solar' switches to 'On sunny hours'.",
            tab=2,
            call_backs=[
                export_settings_to_compare_tab(values, version="two"),
                export_settings_to_compare_tab(heat_pump_config, version="three"),
            ]
        )

        new_config = create_solar_electric(values.copy())
        make_tab_switch_button(
            text="Compare with adding solar electric system (PV)",
            prompt=prompt_to_complete_questions,
            help="Converts to electric if starting with gas.",
            tab=2,
            call_backs=[
                export_settings_to_compare_tab(values, version="two"),
                export_settings_to_compare_tab(new_config, version="three"),
            ]
        )

