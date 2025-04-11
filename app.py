import streamlit as st
from streamlit.components.v1 import html
from PIL import Image

from data_processing.data_processing import (
    load_and_preprocess_data,
)

# Import tab modules
from tabs import home_tab, about_tab, explore_tab, compare_tab, details_tab

# Get image used as icon in web browser tab.
im = Image.open("images/favicon.png")


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

# Create Home page tab contents.
with home:
    home_tab.render()

# Create About contents tab.
with about:
    about_tab.render()

# Create Explore tab contents.
with explore:
    explore_tab.render(data)

# Create contents of the Compare tab.
with compare:
    compare_tab.render(data)

# Create content for Detail tab.
with detailed_info:
    details_tab.render(data)

