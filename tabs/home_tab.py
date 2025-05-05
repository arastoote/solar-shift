import streamlit as st
from streamlit_extras.stylable_container import stylable_container


def render():
    """Renders the Home tab contents with introduction and project information."""
    # Main heading.
    st.markdown(
        "<h1 style='text-align: center; color: #FFA000;'>SolarShift Customer Hot Water Roadmap</h1>",
        unsafe_allow_html=True,
    )

    # Add home page image using columns for centering
    a, b, c = st.columns([1, 2, 1])
    with b:
        st.image("images/house.png", use_container_width=True)

    # Write home page intro text.
    st.markdown(
        """
        <br>
                    
        Welcome to the **SolarShift Hot Water Roadmap Tool** – your personalized guide to smarter, greener, and more cost-effective water heating solutions!
        Our tool is designed to help households across Australia explore and compare a variety of water heating options, including:
        
        - **Resistive heating**
        - **Heat pumps**
        - **Solar self-consumption** strategies (e.g., controlled loads, timers, diverters)
        - **Solar thermal systems**
        - **Gas water heaters**
        
        ### Why Use the SolarShift Tool?
                
        - [x] **Discover Your Savings Potential**: See how much you can save on annual energy bills with each option.
        - [x] **Reduce Your Carbon Footprint**: Understand the environmental impact of your choices.
        - [x] **Tailored to You**: Get recommendations based on your unique household needs and preferences.
        - [x] **Empower Your Decisio**n: Make informed choices when upgrading or purchasing a water heating system.
        
        ### How It Works
        1. **Answer a Few Questions**: Tell us about your household and water usage.
        2. **Explore Your Options**: Compare the financial and environmental impacts of different water heating solutions.
        3. **Plan Your Upgrade**: Get clear, actionable steps to transition to a system that works best for you.
    
        Start your journey to smarter water heating today!
        """,
        unsafe_allow_html=True,
    )

    def change_tab():
        """Switch to Begin tab and scroll to top."""
        st.session_state.tab = "Begin"
        st.session_state.scroll_to_top = True

    # Columns to centre the button defined below.
    (
        a,
        b,
        c,
    ) = st.columns([1, 1, 1])

    # Button to take user to the Begin tab.
    with b:
        with stylable_container(
            key="jump_to_begin_container",
            css_styles="""
                    button{
                        float: right;
                    }
                    """,
        ):
            st.button(
                "Start your journey to smarter water heating today!",
                key="jump_to_begin",
                on_click=change_tab,
            )

    st.markdown(
        "This tool is developed by Collaboration on Energy and Environmental (CEEM) research team at University of New South Wales (UNSW) Sydney as part of SolarShift Project sponsored by RACE for 2030 program."
    )

    # Add logos using columns for centering
    a, b, c, d, e = st.columns([1, 1, 1, 1, 1])
    with b:
        st.image("images/ceem-logo.png", use_container_width=True)
    with c:
        st.image("images/unsw-logo.png", use_container_width=True)
    with d:
        st.image("images/race-logo.png", use_container_width=True)


