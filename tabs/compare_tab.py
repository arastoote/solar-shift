import streamlit as st
import pandas as pd
import plotly.express as px

from graphics.charts import apply_chart_formatting
from data_processing.data_processing import metrics, groups
from helpers.data_selectors import build_interactive_data_filter


def render(data):
    """Renders the Compare tab contents."""

    # Create the heading at the top of the tab.
    st.markdown(
        "<h3 style='text-align: center; color: #FFA000;'>Compare two hot water systems in detail</h1>",
        unsafe_allow_html=True,
    )

    # Create columns for the tab layout, left column for selectors and right column
    # for charts.
    left, gap, right = st.columns([1.75, 0.25, 5])

    with left:
        # Create the selectors for defining "System One" in the comparison.
        with st.expander("Current system", expanded=False):
            st.markdown(
                "",
                help="The options below are sequential filtered. "
                "The options in lower selected box are limited by the chioces made in select boxes above them.",
            )

            data_two, values_two = build_interactive_data_filter(
                data, key_version="two"
            )

        # Create the selectors for defining "System One" in the comparison.
        with st.expander("Alternative system", expanded=True):
            st.markdown(
                "",
                help="The options below are sequential filtered. "
                "The options in lower selected box are limited by the chioces made in select boxes above them.",
            )

            data_three, values_three = build_interactive_data_filter(
                data, key_version="three"
            )

    with right:
        current_system_data = data_two.copy()
        current_system_data.insert(0, "System", "Current system")
        alternative_system = data_three.copy()
        alternative_system.insert(0, "System", "Alternative system")
        system_comparison_data = pd.concat([current_system_data, alternative_system])

        # Create net present cost plot.
        with st.expander("Simple financial comparison", expanded=False):
            columns_to_plot = ["Net present cost ($)"]

            bar_chart = px.bar(
                system_comparison_data,
                x="System",
                text_auto=True,
                y=columns_to_plot,
                barmode="group",
            )

            apply_chart_formatting(
                bar_chart,
                yaxes_title="Net present cost ($)",
                show_legend=False,
                height=200,
            )

            st.plotly_chart(
                bar_chart,
                use_container_width=True,
                key="Net present cost ($)",
            )

        # Create cashflow plot.
        with st.expander("Spending comparison", expanded=True):
            columns_to_plot = [
                "Up front cost ($)",
                "Rebates ($)",
                "Annual cost ($/yr)",
                "Decrease in solar export revenue ($/yr)",
            ]

            bar_chart = px.bar(
                system_comparison_data,
                x="System",
                y=columns_to_plot,
                text_auto=True,
                barmode="group",
                height=200,
            )

            apply_chart_formatting(bar_chart, yaxes_title="Costs")

            st.plotly_chart(bar_chart, use_container_width=True, key="Spending")

        # Create CO2 plot.
        with st.expander("Environmental comparison", expanded=False):
            columns_to_plot = ["CO2 emissions (tons/yr)"]

            bar_chart = px.bar(
                system_comparison_data,
                x="System",
                y=columns_to_plot,
                text_auto=True,
                barmode="group",
                height=200,
            )

            apply_chart_formatting(
                bar_chart, yaxes_title="CO2 emissions (tons/yr)", show_legend=False
            )

            bar_chart.update_traces(
                texttemplate="%{y:.2f}",
            )

            st.plotly_chart(
                bar_chart,
                use_container_width=True,
                key="Environmental",
            )

        # Create table with comparison of system configurations.
        with st.expander("Tabular details comparison", expanded=False):
            values_two["household_occupants"] = str(values_two["household_occupants"])
            values_three["household_occupants"] = str(
                values_three["household_occupants"]
            )
            comp = pd.DataFrame(
                {
                    "Option": values_two.keys(),
                    "Current system": values_two.values(),
                    "Alternative system": values_three.values(),
                }
            )

            st.dataframe(comp, hide_index=True)

        # Create table with system performance metrics.
        with st.expander("Tabular performance comparison", expanded=False):
            # This hides these columns.
            column_config = {
                "Location": None,
                "Household occupants": None,
                "Hot water billing type": None,
                "Heater": None,
                "Heater control": None,
                "Solar": None,
                "Hot water usage pattern": None,
            }

            # Create copy of the data for displaying in a table at the bottom of the
            # Explore tab.
            system_comparison_data = system_comparison_data.loc[
                :, ["System"] + groups + metrics
            ]

            st.dataframe(
                system_comparison_data, hide_index=True, column_config=column_config
            )
