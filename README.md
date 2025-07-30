# Solar-shift streamlit app

This repository contains the source code for the solar-shift streamlit webapp.

The webapp is designed to make the results of the SolarShift project accessible to 
consumers to help inform their hot water heater purchasing and operating decisions. 
More information on the project can be found here: 
https://www.ceem.unsw.edu.au/our-research/solarshift.

# App technology

The app is built predominantly using the streamlit Python package. The package is 
relatively straight forward to use once the core concepts are understood. The streamlit
intro docs are a great place to start understanding streamlit: 
https://docs.streamlit.io/get-started

# Running the app on a local machine

To run the app on your machine use the following steps:

1. Clone this repository to your local machine. Then complete steps 2-5 in the 
   command line inside the repository directory.

2. install the `uv` python package manager

   Windows:

  ```
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```

   MacOS and Linux:

   ```
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. use `uv` to install python 3.12 if you don't already have it:

   ```
   uv python install 3.12
   ```

4. use `uv` to install the solar-shift web app dependencies:

   ```
   uv sync
   ```

5. use `uv` to run the webapp locally:

   ```
   uv run streamlit run app.py
   ```

# App architecture 

- **app.py**: The main application file that sets up the Streamlit app structure and orchestrates the different tabs.
- **tabs/**: This directory contains individual Python files for each tab in the application.
  - **home_tab.py**, **about_tab.py**, **explore_tab.py**, **compare_tab.py**, **assumptions_and_details_tab.py**, **begin_tab.py**: Each file contains a `render` function responsible for displaying the content of that tab.
  - **tab_control.py**: Manages tab navigation and selection.
- **data/**: This directory holds the data used by the application.
  - **hotwater_data.csv**: The core data displayed in the webapp.
  - **system_configs.py**: Contains configuration settings for different system types.
- **data_processing/**: Contains modules related to loading and processing the data.
  - **data_processing.py**: Handles loading data from `hotwater_data.csv` and reformatting it for use in the app.
- **helpers/**: Contains utility functions used across the application.
  - **data_selectors.py**: Provides functions for filtering and selecting data based on user inputs.
- **graphics/**: Contains modules related to visual elements.
  - **charts.py**: Functions for creating and formatting charts and visualizations.
  - **images.py**: Functions for loading and displaying images.
  - **style.py**: Defines styling constants and functions for consistent UI appearance.
- **images/**: Contains static image files used by the app (e.g., favicon, logos, usage patterns chart).
  - Various image files including **favicon.png**, **ceem-logo.png**, **unsw-logo.png**, **race-logo.png**, **usage_patterns.png**, etc.
- **pyproject.toml**: Defines project dependencies managed by `uv`.
- **uv.lock**: Lock file that ensures consistent dependency versions across environments.

# Upkeep and maintenance 

## Updating the results data

- The data the webapp displays can be updated by changing the `data/hotwater_data.csv` file. 
  If the naming conventions are kept the same the webapp code should not need to be 
  modified.

- If new parameter columns are added to the data or naming conventions are changed then 
  the web app may need to be updated in several places, including in:
  - `data_processing/data_processing.py`,
  - `helpers.data_selectors.build_interactive_data_filter`
  - `data.system_configs.py`
  - `tabs.begin_tab.py`
  - `tabs.compare_tab.py`
  - `tabs.explore_tab.py`

## Webapp hosting

To be completed once hosting is finalised.
