"""Constants for TRV valve."""
# Base component constants
NAME = "TRV valve"
DOMAIN = "trv_valve"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.0.1"

ATTRIBUTION = "Data provided by http://jsonplaceholder.typicode.com/"
ISSUE_URL = "https://github.com/gume/trv-valve/issues"

# Icons
ICON = "mdi:valve"

# Platforms
VALVE = "valve"
PLATFORMS = [VALVE]


# Configuration and options
CONF_CLIMATE = "trv"
CONF_NAME = "name"
CONF_OPEN_TEMP = "temp_open"
CONF_CLOSE_TEMP = "temp_close"

# Defaults
DEFAULT_NAME = DOMAIN


STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
