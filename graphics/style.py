import streamlit as st
from typing import Union


def change_label_style(label: str, font_size: Union[str, int] = "12px") -> None:
    """Dynamically changes the style of a Streamlit label using JavaScript injection.

    This function injects JavaScript code to find and modify the style of a specific
    text element in the Streamlit interface. It searches for paragraph elements
    containing the exact text specified and changes their font size and color.

    Args:
        label: The exact text content of the label to modify
        font_size: The desired font size, can be specified as a string with units
                  (e.g., '12px', '1.5em') or as an integer (which will be treated as pixels)

    Returns:
        None

    Note:
        This function relies on the DOM structure of Streamlit's frontend and may
        need adjustment if Streamlit's HTML structure changes in future versions.
    """
    html = f"""
    <script>
        var elems = window.parent.document.querySelectorAll('p');
        var elem = Array.from(elems).find(x => x.innerText == '{label}');
        elem.style.fontSize = '{font_size}';
        elem.style.color = 'Black';
    </script>
    """
    st.components.v1.html(html, height=0)
