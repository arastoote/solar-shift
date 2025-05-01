import streamlit as st
from streamlit_extras.no_default_selectbox import selectbox
from typing import Dict, List, Optional, Union
import pandas as pd


def filter_data(data: pd.DataFrame, group: str, value: str) -> pd.DataFrame:
    if value is not None:
        data = data[data[group] == value]
    return data


def build_interactive_data_filter(
    data: pd.DataFrame,
    key_version: str,
    big_labels: Optional[Dict[str, Union[str, List[str]]]] = None,
) -> tuple[pd.DataFrame, Dict[str, Optional[str]]]:
    """
    Build an interactive data selector interface with cascading filters.

    This function creates a series of dropdown selectors for filtering the dataset
    based on multiple criteria. The filters are applied sequentially, with each
    subsequent filter showing only options available based on previous selections.
    The function maintains state across Streamlit reruns using session state.

    Args:
        data: DataFrame containing the data to filter
        key_version: String identifier for the session state keys to differentiate
                    between multiple instances of this component
        big_labels: Optional dictionary of labels or instructions for each group.
                   If provided, standard labels are hidden and these are shown instead.
                   Values can be strings or lists of strings (for title + description).

    Returns:
        tuple containing:
            - pd.DataFrame: Filtered DataFrame based on all selections
            - Dict[str, Optional[str]]: Dictionary of selected values for each filter
    """

    if big_labels:
        label_visibility = "collapsed"
    else:
        label_visibility = "visible"

    def make_big_label(group: str) -> None:
        """Create a larger, more prominent label for a filter group.

        Args:
            group: The name of the group to create a label for
        """
        if big_labels:
            if isinstance(big_labels[group], str):
                st.markdown("#### " + big_labels[group])
            if isinstance(big_labels[group], list):
                st.markdown("#### " + big_labels[group][0])
                st.markdown(big_labels[group][1])

    def create_select(data: pd.DataFrame, group: str) -> Optional[str]:
        """Create a select box for a specific filter group.

        This function creates a dropdown selector for a specific column,
        maintaining selection state across Streamlit reruns.

        Args:
            data: DataFrame containing the data to extract options from
            group: The column name to create a selector for

        Returns:
            Optional[str]: The selected value, or None if no selection
        """
        options = list(data[group].unique())
        group_key = group.lower().replace(" ", "_")
        key = f"select_{group_key}_{key_version}"
        KEY = key.upper()

        if KEY not in st.session_state:
            selectbox(group, options, key=key, label_visibility=label_visibility)
        else:
            if st.session_state[KEY] in options:
                index = ([None] + options).index(st.session_state[KEY])
            else:
                index = 0

            selectbox(
                group, options, index=index, key=key, label_visibility=label_visibility
            )

        if st.session_state[key] == "---":
            st.session_state[KEY] = None
        else:
            st.session_state[KEY] = st.session_state[key]

        return st.session_state[KEY]

    values = {}

    data = data.copy()
    make_big_label("Location")
    values["location"] = create_select(data, "Location")
    data = filter_data(data, "Location", values["location"])
    make_big_label("Household occupants")
    values["household_occupants"] = create_select(data, "Household occupants")
    data = filter_data(data, "Household occupants", values["household_occupants"])
    make_big_label("Hot water usage pattern")
    values["hot_water_usage_pattern"] = create_select(data, "Hot water usage pattern")
    data = filter_data(
        data, "Hot water usage pattern", values["hot_water_usage_pattern"]
    )
    make_big_label("Solar")
    values["solar"] = create_select(data, "Solar")
    data = filter_data(data, "Solar", values["solar"])
    make_big_label("Heater")
    values["heater"] = create_select(data, "Heater")
    data = filter_data(data, "Heater", values["heater"])
    make_big_label("Hot water billing type")
    values["hot_water_billing_type"] = create_select(data, "Hot water billing type")
    data = filter_data(data, "Hot water billing type", values["hot_water_billing_type"])
    make_big_label("Heater control")
    values["heater_control"] = create_select(data, "Heater control")
    data = filter_data(data, "Heater control", values["heater_control"])

    if None in values.values():
        data = filter_data(data, "Location", "-")

    return data, values


def export_settings_to_compare_tab(
    values_to_export: Dict[str, Optional[str]], version: str
) -> None:
    """Export filter settings to the comparison tab.

    This function copies the selected filter values from one tab to the
    comparison tab by setting the appropriate session state variables.
    This allows users to compare different configurations side by side.

    Args:
        values_to_export: Dictionary of filter values to export
        version: Identifier string for the target comparison tab (e.g., "two" or "three")

    Returns:
        None
    """
    st.session_state[f"select_location_{version}"] = values_to_export["location"]
    st.session_state[f"select_household_occupants_{version}"] = values_to_export[
        "household_occupants"
    ]
    st.session_state[f"select_hot_water_usage_pattern_{version}"] = values_to_export[
        "hot_water_usage_pattern"
    ]
    st.session_state[f"select_solar_{version}"] = values_to_export["solar"]
    st.session_state[f"select_hot_water_billing_type_{version}"] = values_to_export[
        "hot_water_billing_type"
    ]
    st.session_state[f"select_heater_{version}"] = values_to_export["heater"]
    st.session_state[f"select_heater_control_{version}"] = values_to_export[
        "heater_control"
    ]
