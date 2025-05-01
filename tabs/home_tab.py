import streamlit as st
from streamlit_extras.stylable_container import stylable_container

from graphics.images import get_image_base64


def render():
    """Renders the Home tab contents."""
    # Main heading.
    st.markdown(
        "<h1 style='text-align: center; color: #FFA000;'>SolarShift Customer Hot Water Roadmap</h1>",
        unsafe_allow_html=True,
    )

    # Display home page image.
    img_base64 = get_image_base64("images/house.png")
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center; margin-bottom: 10px;">
            <img src="data:image/png;base64,{img_base64}" width="450">
        </div>
        """,
        unsafe_allow_html=True,
    )

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
        """
        Set the forced tab value and scroll to the top that tab.
        """
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

    # Add logos at bottom of the page.
    img_base64_1 = get_image_base64("images/ceem-logo.png")
    img_base64_2 = get_image_base64("images/unsw-logo.png")
    img_base64_3 = get_image_base64("images/race-logo.png")

    st.markdown(
        f"""
        <br>
        <div style="display: flex; justify-content: center; margin-bottom: 10px;">
            <img src="data:image/png;base64,{img_base64_1}" width="200">
            <img src="data:image/svg;base64,{img_base64_2}" width="300">
            <img src="data:image/svg;base64,{img_base64_3}" width="200">
        </div>
        """,
        unsafe_allow_html=True,
    )
