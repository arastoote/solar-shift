import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set page title and configuration
st.set_page_config(
    page_title="Simple Streamlit Demo",
    page_icon="📊",
    layout="wide"
)

# Add a title and description
st.title("📊 Simple Streamlit Demo")
st.markdown("This is a basic demonstration of Streamlit's capabilities.")

# Sidebar with input options
st.sidebar.header("Settings")
display_data = st.sidebar.checkbox("Display Data Table", value=True)
show_chart = st.sidebar.checkbox("Show Chart", value=True)
sample_size = st.sidebar.slider("Sample Size", 10, 100, 50)
chart_type = st.sidebar.selectbox("Chart Type", ["Line", "Bar", "Scatter"])

# Generate some sample data
def generate_data(size):
    dates = pd.date_range(start="2023-01-01", periods=size)
    np.random.seed(42)  # For reproducibility
    values = np.random.randn(size).cumsum()
    df = pd.DataFrame({"date": dates, "value": values})
    return df

# Generate the data
df = generate_data(sample_size)

# Display data if checkbox is selected
if display_data:
    st.subheader("Sample Data")
    st.dataframe(df)

# Display chart based on selection
if show_chart:
    st.subheader(f"{chart_type} Chart")
    
    fig, ax = plt.subplots(figsize=(10, 4))
    
    if chart_type == "Line":
        ax.plot(df["date"], df["value"])
    elif chart_type == "Bar":
        ax.bar(df["date"], df["value"])
    else:  # Scatter
        ax.scatter(df["date"], df["value"])
    
    ax.set_xlabel("Date")
    ax.set_ylabel("Value")
    ax.grid(True, alpha=0.3)
    
    # Display the chart
    st.pyplot(fig)

# Interactive section
st.header("Interactive Section")
user_name = st.text_input("Enter your name:", "Guest")
user_mood = st.select_slider(
    "How are you feeling today?",
    options=["😞", "😐", "🙂", "😀", "🤩"]
)

if st.button("Submit"):
    st.success(f"Thanks for submitting, {user_name}! You're feeling {user_mood} today.")

# Show raw data if user wants to see it
if st.checkbox("Show Raw Data"):
    st.subheader("Raw Data")
    st.code(df.to_string())

# Footer
st.markdown("---")
st.markdown("Created with ❤️ using Streamlit")