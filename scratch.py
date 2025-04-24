import streamlit as st

# Method 1: Using session state with a key
def force_radio_with_session_state():
    # Create a unique key for this radio
    radio_key = "forced_radio"
    
    # Define options
    options = ["Option A", "Option B", "Option C"]
    
    # Initialize session state if it doesn't exist
    if radio_key not in st.session_state:
        st.session_state[radio_key] = options[0]  # Default value
    
    # Button to force selection to Option B
    if st.button("Force Option B"):
        st.session_state[radio_key] = options[1]
        # Note: No st.rerun() needed as session state persists
    
    # Button to force selection to Option C
    if st.button("Force Option C"):
        st.session_state[radio_key] = options[2]
    
    # Display the radio with the session state as value
    selected = st.radio(
        "Choose an option:", 
        options,
        key=radio_key,  # Critical: this ties the widget to session state
        index=options.index(st.session_state[radio_key])  # Set index based on value
    )
    
    st.write(f"You selected: {selected}")

# Method 2: Using query parameters
def force_radio_with_query_params():
    import streamlit as st
    from urllib.parse import urlencode
    import time
    
    # Get current query params
    query_params = st.experimental_get_query_params()
    
    # Extract radio value from query params if it exists
    radio_value = query_params.get("radio_option", ["Option A"])[0]
    
    options = ["Option A", "Option B", "Option C"]
    
    # Force to Option B with query parameter
    if st.button("Force Option B (Query Param)"):
        # Update query parameters
        new_params = {"radio_option": "Option B"}
        st.experimental_set_query_params(**new_params)
        time.sleep(0.1)  # Small delay
        st.rerun()
        
    # Force to Option C with query parameter
    if st.button("Force Option C (Query Param)"):
        # Update query parameters
        new_params = {"radio_option": "Option C"}
        st.experimental_set_query_params(**new_params)
        time.sleep(0.1)  # Small delay
        st.rerun()
    
    # Use the query param to set the index
    selected_index = options.index(radio_value) if radio_value in options else 0
    
    # Display radio button
    selected = st.radio(
        "Choose an option (Query Param method):", 
        options,
        index=selected_index
    )
    
    st.write(f"You selected: {selected}")
    
# Method 3: Clearing cache and forcing with key changes
def force_radio_with_key_change():
    # Get a potential forced value from session state
    forced_value = st.session_state.get("forced_radio_value", None)
    
    options = ["Option A", "Option B", "Option C"]
    
    # Generate a key that changes when we want to force a new selection
    # This essentially breaks Streamlit's widget state tracking
    key_suffix = st.session_state.get("radio_key_counter", 0)
    radio_key = f"radio_{key_suffix}"
    
    # Force to Option B with key change
    if st.button("Force Option B (Key Change)"):
        st.session_state["forced_radio_value"] = "Option B"
        st.session_state["radio_key_counter"] = key_suffix + 1
        st.rerun()
        
    # Force to Option C with key change
    if st.button("Force Option C (Key Change)"):
        st.session_state["forced_radio_value"] = "Option C"
        st.session_state["radio_key_counter"] = key_suffix + 1
        st.rerun()
    
    # Set default index or use forced value
    if forced_value and forced_value in options:
        default_idx = options.index(forced_value)
    else:
        default_idx = 0
    
    # Display radio with changing key
    selected = st.radio(
        "Choose an option (Key Change method):", 
        options,
        key=radio_key,
        index=default_idx
    )
    
    st.write(f"You selected: {selected}")
    
# Main app
def main():
    st.title("Force Streamlit Radio Button Selection")
    
    st.header("Method 1: Session State")
    st.write("Most reliable method for controlling radio button state")
    force_radio_with_session_state()
    
    st.markdown("---")
    
    st.header("Method 2: Query Parameters")
    st.write("Good for sharing specific states via URL")
    force_radio_with_query_params()
    
    st.markdown("---")
    
    st.header("Method 3: Key Change")
    st.write("Alternative approach that forces Streamlit to reset widget state")
    force_radio_with_key_change()

if __name__ == "__main__":
    main()