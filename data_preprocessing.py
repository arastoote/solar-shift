import pandas as pd

group_columns = {
    "location": "Location",
    "household_size": "Household occupants",
    "tariff_type": "Tariff",
    "heater_type": "Heater",
    "control_type": "Heater control",
    "has_solar": "Solar",
    "profile_HWD": "Hotwater usage pattern",
}

groups = list(group_columns.values())

metric_columns = {
    "net_present_cost": "Net present cost ($)",
    "capital_cost": "Up front cost ($)",
    "rebates": "Rebates ($)",
    "annual_energy_cost": "Annual cost ($/yr)",
    "annual_fit_opp_cost": "Annual lost FiT revenue ($/yr)",
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

    data["Heater control"] = data["Heater control"].map(
        {
            "GS": "Run as needed (no control)",
            "CL1": "On overnight",
            "CL2": "Off during peak times",
            "CL3": "On overnight and sunny hours",
            "timer_SS": "On sunny hours",
            "diverter": "Active matching to solar",
            "timer_OP": "On during off-peak TOU"
        }
    )

    data["Hotwater usage pattern"] = data["Hotwater usage pattern"].map(
        {
            1: "Morning and evening only",
            2: "Morning and evening with day time",
            3: "Evenly distributed",
            4: "Morning",
            5: "Evening",
            6: "Late Night",
        }
    )

    data["Tariff"] = data["Tariff"].map(
        {
            "flat": "Flat rate",
            "tou": "Time of use (TOU)",
            "CL": "Controlled load",
            "gas": "Gas",
        }
    )

    return data


def process_system_data(
        data,
        location,
        occupants,
        usage_pattern,
        tariff,
        heater,
        control,
        solar
):
    location_mask = data["Location"] == location
    occupants_mask = data["Household occupants"] == occupants
    usage_pattern_mask = data["Hotwater usage pattern"] == usage_pattern
    tariff_mask = data["Tariff"] == tariff
    heater_mask = data["Heater"] == heater
    control_mask = data["Heater control"] == control
    solar_mask = data["Solar"] == solar

    mask = (
            location_mask &
            occupants_mask &
            usage_pattern_mask &
            tariff_mask &
            heater_mask &
            control_mask &
            solar_mask
    )

    data = data.loc[mask, :]

    agg_dict = {col: "mean" for col in metrics}

    data = data.groupby(groups, as_index=False).agg(agg_dict)

    return data

