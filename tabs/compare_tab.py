import streamlit as st
import pandas as pd
import plotly.express as px

from graphics.charts import apply_chart_formatting
from data_processing.data_processing import metrics, groups, load_and_preprocess_data
from helpers.data_selectors import build_interactive_data_filter, get_rep_postcode_from_postcode


def render(data):
    """Renders the Compare tab for side-by-side system comparison."""

    # Load data and postcode mapping on each rerun
    data, postcode_df = load_and_preprocess_data()
    
    # Ask for postcode to filter dataset to climate zone first
    #postcode = st.text_input(
        #"Enter your postcode",
        #value="",
        #max_chars=4,
        #help="Type your postcode without spinner.",
    #)

    #rep_postcode = None
    #if postcode and postcode.isdigit():
        #rep_postcode = get_rep_postcode_from_postcode(int(postcode), postcode_df)
        #if rep_postcode:
            #data = data[data["Location"] == rep_postcode]
        #else:
            #st.warning("No data found for this postcode, please check your entry.")

    #st.markdown(
        #"<h3 style='text-align: center; color: #FFA000;'>Compare two hot water systems in detail</h1>",
       # unsafe_allow_html=True,
    #)
    
    # Remembering postcode input from Begin tab
    data_two_slice = data.copy()
    loc = st.session_state.get("select_location_two")
    if loc:
        data_two_slice = data_two_slice[data_two_slice["Location"] == loc]

    data_three_slice = data.copy()
    loc = st.session_state.get("select_location_three")
    if loc:
        data_three_slice = data_three_slice[data_three_slice["Location"] == loc]



    #st.write("DEBUG data_two_slice first 3 rows:", data_two_slice.head(3))
    #st.write("DEBUG data_three_slice first 3 rows:", data_three_slice.head(3))

    # Create 3-column layout
    left, middle, right = st.columns([1.75, 5, 1.75])

    with left:
        st.markdown(
            "<h4 style='text-align:center; font-size:20px;'><b>Current system</b></h4>",
            unsafe_allow_html=True
        )
        with st.expander("Current system", expanded=True):
            data_two, values_two = build_interactive_data_filter(data_two_slice, key_version="two")

    with right:
        st.markdown(
            "<h4 style='text-align:center; font-size:20px;'><b>Alternative system</b></h4>",
            unsafe_allow_html=True
        )
        with st.expander("Alternative system", expanded=True):
            data_three, values_three = build_interactive_data_filter(data_three_slice, key_version="three")

    #st.write("DEBUG COMPARE current system selected =", values_two)
    #st.write("DEBUG COMPARE alternative system selected =", values_three)

    with middle:
        # Prepare data for comparison charts
        current_system_data_chart = data_two.copy()
        current_system_data_chart.insert(0, "System", "<span style='font-size:16px;'><b>Current system</b></span>")

        alternative_system_data_chart = data_three.copy()
        alternative_system_data_chart.insert(0, "System", "<span style='font-size:16px;'><b>Alternative system</b></span>")

        system_comparison_chart_data = pd.concat([current_system_data_chart, alternative_system_data_chart])

        # System label for tables (plain text)
        current_system_data_table = data_two.copy()
        current_system_data_table.insert(0, "System", "Current system")

        alternative_system_data_table = data_three.copy()
        alternative_system_data_table.insert(0, "System", "Alternative system")

        system_comparison_table_data = pd.concat([current_system_data_table, alternative_system_data_table])


        # Spending comparison
        with st.expander("Spending comparison", expanded=True):
            columns_to_plot = [
                "Up front cost ($)",
                "Rebates ($)",
                "Annual cost ($/yr)",
                "Decrease in solar export revenue ($/yr)",
            ]
            bar_chart = px.bar(
                system_comparison_chart_data, x="System", y=columns_to_plot,
                text_auto=True, barmode="group", height=400
            )
            apply_chart_formatting(bar_chart, yaxes_title="Costs")
            bar_chart.update_xaxes(
                tickangle=0, automargin=True, tickfont=dict(size=12), ticklabelstandoff=15
            )
            bar_chart.update_layout(legend=dict(orientation="h", y=1.2, x=0.5, xanchor='center'))
            st.plotly_chart(bar_chart, use_container_width=True, key="Spending")

        # Net present cost plot
        with st.expander("Simple financial comparison: over 10 years", expanded=False):
            bar_chart = px.bar(
                system_comparison_chart_data, x="System", y=["Net present cost ($)"],
                text_auto=True, barmode="group"
            )
            apply_chart_formatting(bar_chart, yaxes_title="Net present cost ($)",
                                   show_legend=False, height=250)
            st.plotly_chart(bar_chart, use_container_width=True, key="Net present cost ($)")

        # CO2 emissions
        with st.expander("Environmental comparison", expanded=False):
            bar_chart = px.bar(
                system_comparison_chart_data, x="System", y=["CO2 emissions (tons/yr)"],
                text_auto=True, barmode="group", height=250
            )
            apply_chart_formatting(bar_chart, yaxes_title="CO2 emissions (tons/yr)", show_legend=False)
            bar_chart.update_traces(texttemplate="%{y:.2f}")
            st.plotly_chart(bar_chart, use_container_width=True, key="Environmental")

        # Tabular details
        with st.expander("Tabular details comparison", expanded=False):
            values_two["household_occupants"] = str(values_two["household_occupants"])
            values_three["household_occupants"] = str(values_three["household_occupants"])
            comp = pd.DataFrame({
                "Option": list(map(str,values_two.keys())),
                "Current system": list(map(str,values_two.values())),
                "Alternative system": list(map(str,values_three.values())),
            })
            st.dataframe(comp, hide_index=True)

        # Tabular metrics
        with st.expander("Tabular performance comparison", expanded=False):
            table_df = system_comparison_table_data.loc[:, ["System"] + groups + metrics]
            st.dataframe(table_df, hide_index=True, column_config={
                "Location": None,
                "Household occupants": None,
                "Hot water billing type": None,
                "Heater": None,
                "Heater control": None,
                "Solar": None,
                "Hot water usage pattern": None,
            })
