import streamlit as st
from PIL import Image
from streamlit_scroll_to_top import scroll_to_here

from graphics.style import change_label_style

from data_processing.data_processing import (
    load_and_preprocess_data,
)
from tabs import tab_control, home_tab, begin_tab, explore_tab, compare_tab, details_tab

# Get image used as icon in web browser tab.
im = Image.open("images/favicon.png")

st.set_page_config(page_title="SolarShift", layout="wide", page_icon=im)

# Set width of page content to 90% of web browser width.
st.html(
    """
    <style>
        .stMainBlockContainer {
            max-width: 90vw;
        }
    </style>
    """)

# Decrease the white space padding around the main content.
st.markdown(
    """
    <style>
    
    .block-container
    {
        max-width: 1300px;
        padding-top: 0.9rem;
        padding-bottom: 0rem;
        margin-top: 1rem;
    }
    
    </style>
    """,
    unsafe_allow_html=True,
)

# Setup for functionality that scrolls user view to top of screen.
if "scroll_to_top" not in st.session_state:
    st.session_state.scroll_to_top = False

# Specify location to scroll to when 'top' key is used.
if st.session_state.scroll_to_top:
    scroll_to_here(0, key="top")
    st.session_state.scroll_to_top = False  # Reset the state after scrolling

# Add space that help tabs bar not get hidden.
st.markdown("<br><br>", unsafe_allow_html=True)

# Define tabs.
tab_names = ["Home", "Begin", "Compare", "Advanced explorer", "Details"]

current_tab = tab_control.create(tab_names)

data = load_and_preprocess_data()

# Create Home page tab contents.
if st.session_state["tab"] == "Home":
    home_tab.render()

# Create Begin contents tab.
if st.session_state["tab"] == "Begin":
    begin_tab.render(data)

# Create contents of the Compare tab.
if st.session_state["tab"] == "Compare":
    compare_tab.render(data)

# Create Explore tab contents.
if st.session_state["tab"] == "Advanced explorer":
    explore_tab.render(data)

# Create content for Detail tab.
if st.session_state["tab"] == "Details":
    details_tab.render(data)

for name in tab_names:
    change_label_style(name, font_size="20px")
