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
        Relies on Streamlit's DOM structure and may need adjustment if it changes.
        Only styles the first matching element if multiple elements have the same text.
    """
    # Inject JavaScript to find and style the target element
    html = f"""
    <script>
        var elems = window.parent.document.querySelectorAll('p');
        var elem = Array.from(elems).find(x => x.innerText == '{label}');
        elem.style.fontSize = '{font_size}';
        elem.style.color = 'Black';
    </script>
    """
    # Render with zero height to avoid affecting layout
    st.components.v1.html(html, height=0)
