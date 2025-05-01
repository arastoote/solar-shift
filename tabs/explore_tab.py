import streamlit as st
import plotly.express as px

from graphics.charts import apply_chart_formatting
from data_processing.data_processing import metrics, groups


def render(data):
    """Renders the Explore tab contents."""
    f_data = data.copy()
    # Write heading at the top of tab.
    with st.container():
        st.markdown(
            "<h3 style='text-align: center; color: #FFA000;'>Explore hot water system configurations</h1>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<div style='text-align: center;'> The chart below can display many hot water simulation results at once – use the options on the left to explore the results.</div>",
            unsafe_allow_html=True,
        )

    # Create container  which holds data selectors and plot.
    with st.container():
        # Create left column for data selectors and right column for plot.
        left, gap, right = st.columns([1.75, 0.25, 5])

        # Create the data selectors that control what gets plotted and the contents of
        # the table at the bottom of the page.
        with left:
            # Create some space to push the selectors down the page a litte.
            st.markdown("<br>", unsafe_allow_html=True)

            # Create the data selectors.
            with st.expander("Describe your house", expanded=False):
                st.markdown(
                    "",
                    help="The options below are sequential filtered. "
                    "The options in lower selected box are limited by "
                    "the chioces made in select boxes above them.",
                )
                hs = st.multiselect(
                    "Household size",
                    data["Household occupants"].unique(),
                    default=3,
                    help="The number of people living in the house.",
                )
                if len(hs) > 0:
                    f_data = f_data[f_data["Household occupants"].isin(hs)]
                locs = st.multiselect("Location", f_data["Location"].unique())
                if len(locs) > 0:
                    f_data = f_data[f_data["Location"].isin(locs)]
                patterns = st.multiselect(
                    "Hot water usage pattern",
                    f_data["Hot water usage pattern"].unique(),
                    help="When hot water is typically used in the house.",
                )
                if len(patterns) > 0:
                    f_data = f_data[f_data["Hot water usage pattern"].isin(patterns)]
                tariffs = st.multiselect(
                    "Hot water billing type",
                    data["Hot water billing type"].unique(),
                    help="""
                    How energy used for heating hot water is paid for.

                    This needs to match with the Heater type options
                    selected and the Control type options. E.g. to view
                    gas heater options, gas also needs to be selecte 
                    as the billing type. Similarly, to use Control type options that
                    restrict when the heater is run the
                    'Control load discount electricity' needs to be selected 
                    as the billing type.
                    """,
                )
                if len(tariffs) > 0:
                    f_data = f_data[f_data["Hot water billing type"].isin(tariffs)]
                solar = st.multiselect(
                    "Solar",
                    f_data["Solar"].unique(),
                    help="If the house has a solar electricity system.",
                )
                if len(solar) > 0:
                    f_data = f_data[f_data["Solar"].isin(solar)]
            with st.expander("Choose a heater"):
                st.markdown(
                    "",
                    help="The options below are sequential filtered. "
                    "The options in lower selected box are limited by "
                    "the chioces made in select boxes above them,"
                    "including in the 'Describe your house' box.",
                )
                heater = st.multiselect("Heater type", f_data["Heater"].unique())
                if len(heater) > 0:
                    f_data = f_data[f_data["Heater"].isin(heater)]
                control = st.multiselect(
                    "Control type", f_data["Heater control"].unique()
                )
                if len(control) > 0:
                    f_data = f_data[f_data["Heater control"].isin(control)]
            with st.expander("Chart options"):
                # These control how the selected data is plotted.
                # Create a selector which controls how the data is grouped on the x-axis
                # with a default setting of Heater.
                index = groups.index("Heater")
                x = st.selectbox("Side-by-side", groups, index=index)
                # Create a selector which controls how the data is colored with a
                # default setting of Heater.
                color = st.selectbox("Color", groups, index=index)
                index = metrics.index("Annual cost ($/yr)")
                metric = st.selectbox("Comparison metric", metrics, index=index)

            # Create copy of the data for displaying in a table at the bottom of the
            # Explore tab.
            show_data = f_data.loc[:, groups + metrics]

        # Create the data plot.
        with right:
            chart = px.strip(f_data, y=metric, x=x, color=color)

            chart.update_traces(width=2.0)

            apply_chart_formatting(chart)

            st.plotly_chart(chart, use_container_width=True)

    # Create a container for displaying the chart data in a table.
    with st.container():
        # A radio selector that allows the user to choose between averaging the data
        # before displaying in the table or display the data for all selected data.
        summarise = st.radio(
            "Data display option", ["Average", "Show all"], label_visibility="collapsed"
        )
        # If user selects Average the data is average across groups which are the
        # combination of the chosen x-axis group and plotting color.
        table_groups = list(set((x, color)))
        if len(table_groups) > 0 and summarise == "Average":
            agg_dict = {col: "mean" for col in metrics}
            show_data = show_data.groupby(table_groups, as_index=False).agg(agg_dict)
        show_data = show_data.sort_values("Net present cost ($)")
        st.dataframe(show_data.style.format(precision=2), hide_index=True)
