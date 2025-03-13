import pandas as pd

group_columns = {
    "location": "Location",
    "household_size": "Household occupants",
    "tariff_type": "Tariff",
    "heater_type": "Heater",
    "control_type": "Heater control",
    "has_solar": "Solar",
}

groups = list(group_columns.values())

metric_columns = {
    "capital_cost": "Up front cost ($)",
    "annual_energy_cost": "Annual cost ($/yr)",
    "emissions_total": "CO2 emissions (tons/yr)",
    "annual_energy_consumption": "Annual energy consumption (kWh)"
}

metrics = list(metric_columns.values())

def load_and_preprocess_data():
    data = pd.read_csv("all_the_cases.csv")
    data = data.rename(columns=group_columns)
    data = data.rename(columns=metric_columns)

    data["Heater"] = data["Heater"].map(
        {
            "resistive": "Electric",
            "heat_pump": "Heat Pump",
            "solar_thermal": "Solar Thermal",
            "gas_instant": "Gas Instant",
            "gas_storage": "Gas Storage",
        }
    )

    return data