def create_basic_heat_pump_config(config):
    config["heater"] = "Heat Pump"

    if config["hot_water_billing_type"] == "Flat rate gas":
        config["hot_water_billing_type"] = "Flat rate electricity"
        config["heater_control"] = "Run as needed (no control)"

    if config["heater_control"] == "Active matching to solar":
        config["heater_control"] = "On sunny hours"

    return config


def create_solar_electric(config):
    config["solar"] = "Yes"

    if config["hot_water_billing_type"] == "Flat rate gas":
        config["heater"] = "Electric"
        config["hot_water_billing_type"] = "Flat rate electricity"
        config["heater_control"] = "Run as needed (no control)"

    return config


def create_electric(config):
    config["heater"] = "Electric"

    if config["hot_water_billing_type"] == "Flat rate gas":
        config["hot_water_billing_type"] = "Flat rate electricity"
        config["heater_control"] = "Run as needed (no control)"

    return config


def create_solar_thermal(config):
    config["heater"] = "Solar Thermal"
    config["hot_water_billing_type"] = "Flat rate electricity"
    config["heater_control"] = "Run as needed (no control)"
    return config


def create_gas_instant(config):
    config["heater"] = "Gas Instant"
    config["hot_water_billing_type"] = "Flat rate gas"
    config["heater_control"] = "Run as needed (no control)"
    return config
