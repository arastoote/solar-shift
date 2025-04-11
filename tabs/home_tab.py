import time

import streamlit as st
from streamlit.components.v1 import html
from streamlit_extras.stylable_container import stylable_container


from graphics.images import get_image_base64

def switch(tab):
    return f"""
var tabGroup = window.parent.document.getElementsByClassName("stTabs")[0]
var tab = tabGroup.getElementsByTagName("button")
tab[{tab}].click()
"""

def render():
    """Renders the Home tab contents."""
    # Main heading.
    st.markdown(
        "<h1 style='text-align: center; color: #FFA000;'>Welcome to the Solar Shift Explorer!</h1>",
        unsafe_allow_html=True
    )

    img_base64 = get_image_base64("images/house.png")

    st.markdown(
        f"""
        <div style="display: flex; justify-content: center; margin-bottom: 10px;">
            <img src="data:image/png;base64,{img_base64}" width="450">
        </div>
        """,
        unsafe_allow_html=True
    )

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