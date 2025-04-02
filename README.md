# Solar-shift streamlit app

This repository contains the source code for the solar-shift streamlit web app.

The app is designed to make the results of the SolarShift project accessible to 
consumers to help inform their hot water heater purchasing decisions. More information 
on the project can be found here: https://www.ceem.unsw.edu.au/our-research/solarshift.

# App technology

The app is built predominantly using the streamlit Python package. The package is 
relatively straight forward to use once the core concepts are understood. The streamlit
intro docs are a great place to start understanding streamlit: 
https://docs.streamlit.io/get-started

# Running the app on a local machine

To run the app on your machine use the following command line steps:

1. install the `uv` python package manager

   Windows:

    `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`

   MacOS and Linux:

   `curl -LsSf https://astral.sh/uv/install.sh | sh`

2. use `uv` to install python 3.12 if you don't already have it:

   `uv python install 3.12`

3. use `uv` to install the solar-shift web app dependencies:

   `uv sync`

4. use `uv` to run the webapp locally:

   `uv run streamlit run solar_shift.py`

# App architecture 

   - **streamlit.py**: Most of the code for the webapp is located in the file 
     streamlit.py. With the five tabs of the web defined sequential in the file.
   - **data_preprocessing.py**: Before the data is used directly in the webapp it is 
     loaded from the csv into pd.DataFrame and reformatted in the function 
     load_and_preprocess_data defined in the file data_preprocessing.py
   - **graphics.py**: The code for drawing the image on the home page, the website icon
      and apply chart formatting are in the file graphics.py
   - **pyproject.toml**: The project dependencies are defined in pyproject.toml.

# Upkeep and maintenance 

## Updating the results data

- The data the webapp displays can be updated by changing the `hotwater_data.csv` file. 
  If the naming conventions are kept the same the webapp code should not need to be 
  modified.

- If new parameter columns are added to the data then the web app may need to be 
  updated in several places, including in data_preprocessing.py, and anywhere widgets 
  for filter or aggregating data are defined.

- If data naming conventions are changed, then data_preprocessing.py and anywhere a data
  column is referenced in solar_shift.py may need to be updated.

## Webapp hosting

To be completed once hosting is finalised.



