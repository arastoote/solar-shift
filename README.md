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
   - **tabs/**: This directory contains individual Python files for each tab in the application (Home, About, Explore, Compare, Details). Each file contains a `render` function responsible for displaying the content of that tab.
   - **data/**: This directory holds the data used by the application.
     - ***hotwater_data.csv***: The core data displayed in the webapp.
   - **data_processing/**: Contains modules related to loading and processing the data.
     - **data_processing.py**: Handles loading data from `hotwater_data.csv` and reformatting it for use in the app.
   - **graphics/**: Contains modules related to visual elements.
     - **visuals.py**: Includes functions for drawing the logo on the home page and loading images.
     - **images.py**: Function for applying consistent formatting to charts.
   - **images/**: Contains static image files used by the app (e.g., favicon, usage patterns chart).
   - **pyproject.toml**: Defines project dependencies managed by `uv`.

# Upkeep and maintenance 

## Updating the results data

- The data the webapp displays can be updated by changing the `data/hotwater_data.csv` file. 
  If the naming conventions are kept the same the webapp code should not need to be 
  modified.

- If new parameter columns are added to the data then the web app may need to be 
  updated in several places, including in `data_processing/data_processing.py`, and anywhere widgets 
  for filter or aggregating data are defined (primarily within the `tabs/` directory).

- If data naming conventions are changed, then `data_processing/data_processing.py` and anywhere a data
  column is referenced (primarily within the `tabs/` directory) may need to be updated.

## Webapp hosting

To be completed once hosting is finalised.



