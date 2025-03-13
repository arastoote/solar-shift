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
    "net_present_cost": "Net present cost ($)",
    "capital_cost": "Up front cost ($)",
    "rebates": "Rebates ($)",
    "annual_energy_cost": "Annual cost ($/yr)",
    "annual_fit_opp_cost": "Annual lost FiT revenue ($/yr)",
    "emissions_total": "CO2 emissions (tons/yr)",
    "annual_energy_consumption": "Annual energy consumption (kWh)"
}

metrics = list(metric_columns.values())

other_columns = {
    "profile_HWD": "Usage profile",
}

other = list(other_columns.values())


def load_and_preprocess_data():
    data = pd.read_csv("all_the_cases.csv")
    data = data.rename(columns=group_columns)
    data = data.rename(columns=metric_columns)
    data = data.rename(columns=other_columns)

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


def process_system_data(
        data,
        location,
        occupants,
        tariff,
        heater,
        control,
        solar
):
    location_mask = data["Location"] == location
    occupants_mask = data["Household occupants"] == occupants
    tariff_mask = data["Tariff"] == tariff
    heater_mask = data["Heater"] == heater
    control_mask = data["Heater control"] == control
    solar_mask = data["Solar"] == solar

    mask = (
            location_mask &
            occupants_mask &
            tariff_mask &
            heater_mask &
            control_mask &
            solar_mask
    )

    data = data.loc[mask, :]

    agg_dict = {col: "mean" for col in metrics}

    data = data.groupby(groups, as_index=False).agg(agg_dict)

    return data

