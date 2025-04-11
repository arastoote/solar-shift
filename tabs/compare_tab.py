import streamlit as st
import pandas as pd
import plotly.express as px

from graphics.charts import apply_chart_formatting
from data_processing.data_processing import metrics, groups, process_system_data

def create_select(data, group, default, version):
    options = list(data[group].unique())
    index = options.index(default)
    key = f"select-{group}-{version}"
    return st.selectbox(group, options, index=index, key=key)

def render(data):
    """Renders the Compare tab contents."""
    # Create the heading at the top of the tab.
    st.markdown(
        "<h3 style='text-align: center; color: #FFA000;'>Compare two hot water systems in detail</h1>",
        unsafe_allow_html=True
    )

    # Create columns for the tab layout, left column for selectors and right column
    # for charts.
    left, gap, right = st.columns([1.75, 0.25, 5])

    with left:
        # Create the selectors for defining "System One" in the comparison.
        with st.expander("System one details", expanded=True):
            location_one = create_select(data, "Location", "Sydney", "one")
            occupants_one = create_select(data, "Household occupants", 3, "one")
            usage_pattern_one = create_select(data, "Hot water usage pattern",
                                              "Morning and evening only", "one")
            solar_one = create_select(data, "Solar", "Yes", "one")
            heater_one = create_select(data, "Heater", "Heat Pump", "one")
            tariff_one = create_select(data, "Hot water billing type", "Flat rate electricity", "one")
            control_one = create_select(data, "Heater control", "Run as needed (no control)",
                                        "one")

        # Create the selectors for defining "System One" in the comparison.
        with st.expander("System two details"):
            location_two = create_select(data, "Location", "Sydney", "two")
            occupants_two = create_select(data, "Household occupants", 3, "two")
            usage_pattern_two = create_select(data, "Hot water usage pattern",
                                              "Morning and evening only", "two")
            solar_two = create_select(data, "Solar", "Yes", "two")
            heater_two = create_select(data, "Heater", "Electric", "two")
            tariff_two = create_select(data, "Hot water billing type", "Flat rate electricity", "two")
            control_two = create_select(data, "Heater control",
                                        "Run as needed (no control)",
                                        "two")

    with right:
        # Filter and aggregate data for System One.
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

        # Add a column labeling the data as System One
        system_one_data.insert(0, "System", "One")

        # Filter and aggregate data for System One.
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

        # Add a column labeling the data as System Two
        system_two_data.insert(0, "System", "Two")

        # Combine system one and two data for plotting and displaying in tables.
        system_comparison_data = pd.concat([system_one_data, system_two_data])

        # Create net present cost plot.
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

        # Create cashflow plot.
        with st.expander("Spending", expanded=True):
            columns_to_plot = [
                "Up front cost ($)",
                "Rebates ($)",
                "Annual cost ($/yr)",
                "Decrease in solar export revenue ($/yr)"
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

        # Create CO2 plot.
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

        # Create table with comparison of system configurations.
        with st.expander("Tabular details comparison", expanded=False):
            comp = pd.DataFrame({
                "Option": ["Location", "Household occupants", "Hot water usage pattern", "Solar", "Heater", "Hot water billing type", "Heater control"],
                "System one": [location_one, str(occupants_one), usage_pattern_one, solar_one, heater_one, tariff_one, control_one],
                "System two": [location_two, str(occupants_two), usage_pattern_two, solar_two, heater_two, tariff_two, control_two],
            })

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
                "Hot water usage pattern": None
            }

            # Create copy of the data for displaying in a table at the bottom of the
            # Explore tab.
            system_comparison_data = system_comparison_data.loc[:, ["System"] + groups + metrics]

            st.dataframe(system_comparison_data, hide_index=True, column_config=column_config)

        with st.container():
            st.info(
                '''
                Note: Some Heater/Heater control/Tariff combinations are not available.
                If no inputs are returned try adjusting the selected control or tariff option.
                Read further about the available options in the **Details** tab.
                '''
            ) 