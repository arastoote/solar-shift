import streamlit as st
from streamlit_extras.stylable_container import stylable_container
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

# Get image used as icon in web browser tab.
im = Image.open("favicon.png")


st.set_page_config(
    page_title="Explore!",
    layout="wide",
    page_icon=im
)

# Set width of page content to 90% of web browser width.
st.html("""
    <style>
        .stMainBlockContainer {
            max-width: 90vw;
        }
    </style>
    """
)

# Decrease the white space padding around the main content.
st.markdown("""
<style>

.block-container
{
    max-width: 1300px;
    padding-top: 1rem;
    padding-bottom: 0rem;
    margin-top: 1rem;
}

</style>
""", unsafe_allow_html=True)


# Create the tabs of the webpage.
home, about, explore, compare, detailed_info = \
    st.tabs(["Home", "About", "Explore", "Compare", "Details"])


# Wrap the data loading function in a function with streamlit caching enabled. This way
# the function is only run once when the app is launched.
@st.cache_data
def get_data():
    return load_and_preprocess_data()


data = get_data()

# Create a function that allows the two buttons at the bottom of the homepage to take
# the user to another tab.
def switch(tab):
    return f"""
var tabGroup = window.parent.document.getElementsByClassName("stTabs")[0]
var tab = tabGroup.getElementsByTagName("button")
tab[{tab}].click()
"""


# Create Home page tab contents.
with home:
    # Main heading.
    st.markdown(
        "<h1 style='text-align: center; color: #FFA000;'>Welcome to the Solar Shift Explorer!</h1>",
        unsafe_allow_html=True
    )

    # Home page picture.
    st.markdown(draw_logo(), unsafe_allow_html=True)

    # Columns to space buttons out.
    a, b, c, d = st.columns([0.3, 1, 1, 0.4])

    # Button to take user to the Explore tab.
    with b:
        with stylable_container(
                key="Upload_Data",
                css_styles="""
                    button{
                        float: right;
                    }
                    """
        ):
            if st.button("Explore a variety of hot water solutions"):
                with st.empty():
                    html(f"<script>{switch(2)}</script>", height=0)
                    time.sleep(1)
                    html(f"<div></div>", height=0)

    # Button to take user to the Compare tab.
    with c:
        if st.button("Compare two hot water solutions side-by-side"):
            with st.empty():
                html(f"<script>{switch(3)}</script>", height=0)
                time.sleep(1)
                html(f"<div></div>", height=0)

# Create About contents tab.
with about:
    st.markdown("Here we will describe the project.")

# Create Explore tab contents.
with explore:

    # Write heading at the top of tab.
    with st.container():
        st.markdown(
            "<h3 style='text-align: center; color: #FFA000;'>Explore hot water system configurations</h1>",
            unsafe_allow_html=True)

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
                hs = st.multiselect(
                    "Household size",
                    data["Household occupants"].unique(),
                    default=3,
                    help="The number of people living in the house."
                )
                locs = st.multiselect("Location", data["Location"].unique())
                patterns = st.multiselect(
                    "Hot water usage pattern",
                    data["Hot water usage pattern"].unique(),
                    help="When hot water is typically used in the house."
                )
                tariffs = st.multiselect(
                    "Hot water billing type",
                    data["Hot water billing type"].unique(),
                    help="""
                    How energy used for heating hot water is paid for. 
                    
                    This needs to match with the Heater type options
                    selected and the Control type options. E.g. to view 
                    gas heater options, gas also needs to be the billing type
                    option. Similarly, to use Control type options that
                    restrict when the heater is run the 
                    'Control load discount electricity' needs to be the billing
                    type.
                    """
                )
                solar = st.multiselect(
                    "Solar",
                    data["Solar"].unique(),
                    help="If the house has a solar electricity system."
                )
            with st.expander("Choose a heater"):
                heater = st.multiselect("Heater type", data["Heater"].unique())
                control = st.multiselect("Control type", data["Heater control"].unique())
            with st.expander("Compare"):
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

            # Filter the data using the values from the data selectors defined above.
            f_data = data.copy()
            if len(hs) > 0:
                f_data = f_data[f_data["Household occupants"].isin(hs)]
            if len(locs) > 0:
                f_data = f_data[f_data["Location"].isin(locs)]
            if len(patterns) > 0:
                f_data = f_data[f_data["Hot water usage pattern"].isin(patterns)]
            if len(tariffs) > 0:
                f_data = f_data[f_data["Hot water billing type"].isin(tariffs)]
            if len(solar) > 0:
                f_data = f_data[f_data["Solar"].isin(solar)]
            if len(control) > 0:
                f_data = f_data[f_data["Heater control"].isin(control)]
            if len(heater) > 0:
                f_data = f_data[f_data["Heater"].isin(heater)]

            # Create copy of the data for displaying in a table at the bottom of the
            # Explore tab.
            show_data = f_data.loc[:, groups + metrics]

        # Create the data plot.
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

    # Create a container for displaying the chart data in a table.
    with st.container():
        # A radio selector that allows the user to choose between averaging the data
        # before displaying in the table or display the data for all selected data.
        summarise = st.radio("Data display option", ["Average", "Show all"], label_visibility="collapsed")
        # If user selects Average the data is average across groups which are the
        # combination of the chosen x-axis group and plotting color.
        table_groups = list(set((x, color)))
        if len(table_groups) > 0 and summarise == "Average":
            agg_dict = {col: "mean" for col in metrics}
            show_data = show_data.groupby(table_groups, as_index=False).agg(agg_dict)
        show_data = show_data.sort_values("Net present cost ($)")
        st.dataframe(show_data.style.format(precision=2), hide_index=True)

# Create contents of the Compare tab.
with (compare):

    # Create a helper function which is used to create selectors.
    def create_select(group, default, version):
        options = list(data[group].unique())
        index = options.index(default)
        key = f"select-{group}-{version}"
        return st.selectbox(group, options, index=index, key=key)

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
            location_one = create_select("Location", "Sydney", "one")
            occupants_one = create_select("Household occupants", 3, "one")
            usage_pattern_one = create_select("Hot water usage pattern",
                                              "Morning and evening only", "one")
            solar_one = create_select("Solar", "Yes", "one")
            heater_one = create_select("Heater", "Heat Pump", "one")
            tariff_one = create_select("Hot water billing type", "Flat rate electricity", "one")
            control_one = create_select("Heater control", "Run as needed (no control)",
                                        "one")

        # Create the selectors for defining "System One" in the comparison.
        with st.expander("System two details"):
            location_two = create_select("Location", "Sydney", "two")
            occupants_two = create_select("Household occupants", 3, "two")
            usage_pattern_two = create_select("Hot water usage pattern",
                                              "Morning and evening only", "two")
            solar_two = create_select("Solar", "Yes", "two")
            heater_two = create_select("Heater", "Electric", "two")
            tariff_two = create_select("Hot water billing type", "Flat rate electricity", "two")
            control_two = create_select("Heater control",
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

# Create content for Detail tab.
with detailed_info:
    st.markdown("""
    
    ## Contents
    
    1. [Methodology](#methodology)
    1. [Hot water heaters](#hot-water-heaters)
    1. [billing types (tariffs)](#billing-types)
    1. [Hot water control](#hot-water-control)
    1. [Hot water usage patterns](#hot-water-usage-patterns)
    1. [Options explored](#options-explored)
                
    ## Methodology
                
    Hot water system performance was calculated using a two stage methodology. In 
    the first stage a thermal simulation of the hot water system is performed and 
    in the second stage the cost of operating the system is determined.
                
    ### Thermal simulation
                
    The thermal simulation of the hot water systems dynamically simulated the 
    temperature in the hot water storage tank and the system's use of 
    electricity or gas. Taking into account the:
                
    - Usage of hot water by the house, according to the selected hot water 
        usage pattern,
    - The thermal properties of the hot water tank (e.g. insulation)
    - Energy obtained from solar hot water heating panels (solar 
        thermal systems only)
    - The heating of the hot water when the temperature fell below the
        thermostate turn on set point
    - The efficiency of the heater, how much energy from electricity or gas
        it requires to heat water
    - Note, instantaneous gas systems do not have tanks, so only the energy
        required to directly heat the water as needed is considered.
            
    The key output of these simulations is the time varying energy (gas or
    electrcity) usage across the year.
                
    ### Financial cost
                
    Once a hot water heater's time varying energy usage had been 
    calculated then the cost of operating the heater was determined. For
    electric, heat pump, and solar thermal systems the following method
    was used to calculate the operating cost. For each half hourly period
    in the energy usage results:
            
    1. The cost of heating using electricity from the households solar system
    was determined. If solar electricity was available this was used preferentially
    with an assumed cost equal to solar export payment rate (feed in tariff). 
    The solar export payment rate was applied as a cost because when solar
    electricity was used to heat hot water the household loses the revenue that
    they would otherwise have obtained from exporting.
    2. The cost of heating using grid electrity is determined. Any energy 
    required to heat the hot water that cannot not be provided from solar
    electricity must be imported from the electricity grid. The cost of this
    electricity was determined by the billing type (tariff) selected. For time 
    varying billing types this rate can change throughout the day and year. For
    flate rate and controlled load billing types this rate is constant throughout the
    year.
    3. The cost of heating from solar and from the grid for the half hourly period
    is added together to give the total cost for the period.
                
    Then the cost of heating for a year is determined by summing the costs 
    for all periods in the year. Note, no fixed daily charges are considered 
    for electricity as household must pay these regardless of their heater 
    type or total usage. 
            
    For gas hot water systems the cost was simply calculated by mutipling the
    total gas usage by fixed rate for gas.
                
    ### Environmental cost
                
    For electric, heat pump, and solar hot water the environemental cost in tons of 
    CO2 per year is also calaculated on a time varying basis. 
    For each half hourly period in the year the volume of electricity not met by the 
    households solar was multiplied by the carbon intensity of grid at that time to give the
    CO2 emissions assocaited with using hot water at that time. Then the emissions for all
    half hourly periods across the year were summed to give the total emissions per year.
                
    For gas hot water systems the yearly emssions was simply calculated by mutipling the
    total gas usage by the emissions intensity of gas.
                
    ## Billing type
                
    The billing type, or tariff, determines how the household is charged for electricity
    or gas use. There are three types of billing that considered in the Solar Shift analysis:
                
    1. Flate rate electricity/gas: here a fixed rate for electricity or gas is charged 
    regardless of when it is used. 
    2. Controlled load discount electricity: a fixed rate is also used for controlled 
    load, but a lower rate is charged because the load is typically shifted to times when the cost 
    is lower for grid to supply energy to the household.
    3. Time varying rate electricity: here the rate charged for electricity depends on the
    time of use.
                
    ## 1. Hot water heaters
    
    ### 1.1 Electric
    
    Electric hot water heaters refer to electric tank based systems. Electric hot water
    systems use a resistive element similar to those found in an oven to heat a tank of
    hot water. The tank allows the hot water to be heated and then stored, which means
    these systems can be operated very flexibly, heating when electricity is cheaper, such as overnight, or when solar electricity is available, with the hot water stored 
    for use later. These systems are very simple and, therefore, are cheap to 
    install. Electric hot water heaters can also be paired with a solar electricity 
    diverter, which measures how much electricity is being exported to the grid and 
    adjusts the heater power consumption to match the amount of spare solar electricity. 
    Diverters add to the cost and complexity of the system but can lower electricity bills 
    and carbon emissions.  
    
    ### 1.2 Heat pump
    
    Heat pumps use the same technology found in fridges and air conditioners to suck heat 
    out of the air and pump it into water. As the heat comes from the air rather than
    directly from electricity, they typically use much less energy than simple electric 
    hot water heaters. However, similar to an electric hot water heater, they use a tank 
    to store the hot water, so it can be run flexibly when electricity is 
    cheaper, such as overnight or during the day when solar electricity is available. 
    Heat pumps tend to be more expensive to buy but cheaper to run than simple electric 
    hot water systems.
    
    ### 1.3 Gas instant
    
    Instantaneous gas hot water systems turn on only when you turn on your hot water tap, 
    heating the water on demand as it is needed. They tend to be cheap to install and have a
    moderate running cost. However, there isn't any scope to reduce emissions or lower
    running costs by combining this type of hot water system with solar electricity.
    
    ### 1.4 Gas storage
    
    Gas storage systems use gas to heat the hot water, which is then stored in a tank. 
    These systems tend to be a bit more expensive to install and run compared to 
    instantaneous gas.
    
    ### 1.5 Solar thermal
    
    Solar thermal systems use the sun to heat the water directly, which is then stored in
    a tank for later use. In the Solar Shift project, we also assumed that the Solar 
    thermal systems had an electric booster that heated the hot water tank when its
    temperature dropped below a preset temperature. Solar thermal systems tend to be 
    expensive to install and relatively cheap to run. Additionally, because the sun is 
    being used to heat the water directly, they use less roof space than is required by solar 
    electricity systems. However, the complexity of running water pipes on and off your 
    roof, as well as the pumps needed for some systems is an additional 
    consideration.
    
    ## 2. Hot water control
    
    Some hot water systems can be controlled so they use electricity when it is cheaper 
    or when solar electricity is available. The various control strategies 
    explored in the Solar Shift simulations are described below.
    
    ### 2.1 Run as needed (no control)
    
    Run as needed means the hot water system will just run as per its internal 
    control system. For Electric, Heat pump, and Gas storage, this means the heater will
    run when the water in the tank falls below a preset temperature. For Gas Instant, 
    the heater will run when hot water is used. For Solar thermal the heater
    will run when the sun is shining or the temperature drops below a preset 
    value.
    
    ### 2.2. Off during peak usage times
    
    This control option means the water heater is restricted from running during local 
    peak electricity usage times. The control option is only available for Electric and 
    Heat pump hot water heaters and with the 'Controlled load discount electricity' billing
    type.
    
    ### 2.3 On during off-peak billing times
    
    This control option means the water heater can only run during off-peak billing 
    times (as defined in time varying electricity billing). The control option is only 
    available for Electric and Heat pump hot water heaters and with the 
    'Time varying rate electricity' billing type.
    
    ### 2.4 On overnight
    
    This control option means the water heater can only run overnight. The control 
    option is only available for Electric and Heat pump hot water heaters and with the 
    'Controlled load discount electricity' billing type.
    
    ### 2.5 On overnight and sunny hours
    
    This control option means the water heater can only run overnight and during periods
    of the day that are typically sunny. The control option is only available for 
    Electric and Heat pump hot water heaters and with the 'Controlled load discount 
    electricity' billing type.
    
    ### 2.6 On sunny hours
    
    This control option means the water heater can only run during periods
    of the day that are typically sunny. The control option is only available for 
    Electric and Heat pump hot water heaters and with the 'Flat rate electricity' billing 
    type.
    
    ### 2.7 Active matching to solar
    
    This control option means the water heater runs when there is spare solar 
    electricity being exported to the grid. The control option is only available for 
    Electric heaters with the 'Flat rate electricity' or 'Controlled load discount 
    electricity' billing type.
                
    ## Hot water usage pattern
                
    Hot water heating was simulated with a number of different hot water usage patterns.
    The user can choose the one that best matches their own usage pattern or consider
    how a hot water system might peform across a several patterns if they are unsure
    which one best matches them.
                    
    ![Hot water usage patterns](/usage_patterns.png)
    
    ## 3. Options explored
    
    Not all system configurations have been modelled. Typically, when system 
    configurations have not been modelled this is because the configuration does not 
    make sense from a technical perspective, e.g. it does not make sense to model a Gas
    storage heater with a Flat rate electricity billing type. The complete set of 
    configurations that have been modelled are shown in the table below.
    """
    )
    cols = ["Heater", "Heater control", "Hot water billing type", "Solar"]
    show_data = data.loc[:, cols]
    show_data = show_data.drop_duplicates(cols)
    show_data = show_data.sort_values(by=cols)
    st.dataframe(show_data, hide_index=True)

