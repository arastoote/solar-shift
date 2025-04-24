import time

import streamlit as st
from streamlit.components.v1 import html
from streamlit_scroll_to_top import scroll_to_here


def make_tab_switch_button(text, key, prompt, tab, call_backs=None, help=""):

    def scroll():
        st.session_state.current_tab = "Begin"
        # st.session_state.scroll_to_top = True

    st.button(text, key=key, help=help, on_click=scroll, use_container_width=True)
        # if prompt:
        # st.toast("Please finish describing your house and hot water heater.")
        # st.session_state[f"scroll_to_top"] = True
        # print(tab)
        # st.session_state.tabs = tab
        # st.experimental_rerun()
        # else:
        #     if call_backs:
        #         for call_back in call_backs:
        #             call_back()
        
