import time

import streamlit as st
from streamlit.components.v1 import html
from PIL import Image
from streamlit_scroll_to_top import scroll_to_here

from data_processing.data_processing import (
    load_and_preprocess_data,
)

# Import tab modules
from tabs import home_tab, begin_tab, explore_tab, compare_tab, details_tab

# Get image used as icon in web browser tab.
im = Image.open("images/favicon.png")

st.set_page_config(
    page_title="SolarShift",
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
    padding-top: 0.9rem;
    padding-bottom: 0rem;
    margin-top: 1rem;
}

</style>
""", unsafe_allow_html=True)

# # Create the tabs of the webpage.
# home, begin, compare, explore, detailed_info = \
#     st.tabs(["Home", "Begin", "Compare",  "Advanced explorer", "Details"])

if 'scroll_to_top' not in st.session_state:
    st.session_state.scroll_to_top = False

if st.session_state.scroll_to_top:
    scroll_to_here(0, key='top')
    st.session_state.scroll_to_top = False  # Reset the state after scrolling

st.markdown("<br>", unsafe_allow_html=True)

tabs = ["Home", "Begin", "Compare",  "Advanced explorer", "Details"]


if "radio_key_counter" not in st.session_state:
    st.session_state["radio_key_counter"] = 0

forced_tab = st.session_state.get("forced_tab", None)

if forced_tab is not None:
    print("there")

    st.session_state["radio_key_counter"] += 1

    key_suffix = st.session_state.get("radio_key_counter", 0)
    tab_key = f"tab_{key_suffix}"

    current_tab = st.radio(
        "Navigate",
        tabs,
        index=tabs.index(forced_tab),
        key=tab_key,
        horizontal=True,
        label_visibility="collapsed"
    )

    st.session_state.forced_tab = None

else:
    key_suffix = st.session_state.get("radio_key_counter", 0)
    tab_key = f"tab_{key_suffix}"
    current_tab = st.radio(
        "Navigate",
        tabs,
        key=tab_key,
        horizontal=True,
        label_visibility="collapsed"
    )

css = '''
<style>
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
    font-size:1.25rem;
    }
</style>
'''

st.markdown(css, unsafe_allow_html=True)

# Wrap the data loading function in a function with streamlit caching enabled. This way
# the function is only run once when the app is launched.
@st.cache_data
def get_data():
    return load_and_preprocess_data()

data = get_data()

# Create Home page tab contents.
if current_tab == "Home":
    home_tab.render()

# Create Begin contents tab.
if current_tab == "Begin":
    begin_tab.render(data)

# Create contents of the Compare tab.
if current_tab == "Compare":
    compare_tab.render(data)

# Create Explore tab contents.
if current_tab == "Advanced explorer":
    explore_tab.render(data)

# Create content for Detail tab.
if current_tab == "Details":
    details_tab.render(data)