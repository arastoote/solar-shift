import streamlit as st
from typing import List, Callable


def create(tab_names: List[str]) -> None:
    """Creates a horizontal navigation bar with tab buttons for application navigation.

    This function generates a row of evenly-spaced buttons that act as navigation tabs.
    The currently active tab is highlighted with an orange underline.
    Tab state is maintained across Streamlit reruns using session state.

    Args:
        tab_names: List of tab names to create buttons for. Each name will become
                  a button label and also serve as the key in session state.

    Returns:
        None
    """

    # Set default tab if none selected
    if "tab" not in st.session_state:
        st.session_state["tab"] = "Home"

    def change_tab_home(tab: str) -> Callable[[], None]:
        """Creates a callback function for a specific tab button.

        This closure creates a function that, when called, will change the active tab
        and set a flag to scroll to the top of the page.

        Args:
            tab: The name of the tab to switch to when the button is clicked

        Returns:
            Callable[[], None]: A callback function that updates the session state
        """

        def func() -> None:
            # Update tab and trigger scroll on next rerun
            st.session_state.tab = tab
            st.session_state.scroll_to_top = True

        return func

    # Create buttons in equal-width columns
    for name, col in zip(tab_names, st.columns([1, 1, 1, 1, 1])):
        with col:
            # Create full-width button with click handler
            st.button(
                name,
                key=name,
                on_click=change_tab_home(name),
                use_container_width=True,
            )
            # Highlight active tab with orange underline
            if st.session_state["tab"] == name:
                st.markdown(
                    """
                <style>
                .redline {
                    display: block;
                    width: 100%;
                    height: 4px;
                    background-color: #FFA000;
                    margin-top: -10px;
                }
                </style>
                <div class="redline"></div>
                """,
                    unsafe_allow_html=True,
                )
