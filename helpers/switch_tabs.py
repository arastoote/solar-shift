import time

import streamlit as st
from streamlit.components.v1 import html


def switch(tab):
    switch_script = (
        f"""
        var tabGroup = window.parent.document.getElementsByClassName("stTabs")[0];
        var tab = tabGroup.getElementsByTagName("button");
        tab[{tab}].click();
        """
    )
    return switch_script

def scroll():
    st.session_state.scroll_to_top = True

def make_tab_switch_button(text, prompt, tab, call_backs=None, help=""):
    if st.button(text, key=text, on_click=scroll, help=help, use_container_width=True):
        if prompt:
            st.toast("Please finish describing your house and hot water heater.")
            st.session_state[f"scroll_to_top"] = True
        else:
            if call_backs:
                for call_back in call_backs:
                    call_back() 
            with st.empty():
                html(f"<script>{switch(tab)}</script>", height=0)
                time.sleep(1)
                html(f"<div></div>", height=0)
                st.session_state[f"scroll_to_top"] = True
                st.rerun()
