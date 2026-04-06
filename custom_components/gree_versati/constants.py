"""Constants for the Gree Versati integration."""
from __future__ import annotations

from typing import Final

from homeassistant.const import Platform

# Domain for the integration
DOMAIN: Final = "gree_versati"

# Configuration keys
CONF_DEVICE_ID: Final = "device_id"
CONF_KEY: Final = "key"
CONF_TIMEOUT: Final = "timeout"
CONF_SCAN_INTERVAL: Final = "scan_interval"

# Default connection settings
DEFAULT_PORT: Final = 7000
DEFAULT_TIMEOUT: Final = 5
DEFAULT_SCAN_INTERVAL: Final = 30
DEFAULT_RETRIES: Final = 2

# Heating water outlet temperature range (°C)
MIN_HE_WAT_OUT_TEMP_SET: Final = 20
MAX_HE_WAT_OUT_TEMP_SET: Final = 60
HE_WAT_OUT_TEMP_SET_STEP: Final = 1

# Cooling water outlet temperature range (°C)
MIN_CO_WAT_OUT_TEMP_SET: Final = 5
MAX_CO_WAT_OUT_TEMP_SET: Final = 25
CO_WAT_OUT_TEMP_SET_STEP: Final = 1

# Water box (DHW) temperature range (°C)
MIN_WAT_BOX_TEMP_SET: Final = 20
MAX_WAT_BOX_TEMP_SET: Final = 60
WAT_BOX_TEMP_SET_STEP: Final = 1

# Parameter keys exposed by the Gree protocol
PARAM_HE_WAT_OUT_TEM_SET: Final = "HeWatOutTemSet"
PARAM_CO_WAT_OUT_TEM_SET: Final = "CoWatOutTemSet"
PARAM_WAT_BOX_TEM_SET: Final = "WatBoxTemSet"

# Sensor parameter keys
PARAM_ALL_IN_WAT_TEM_HI: Final = "AllInWatTemHi"
PARAM_ALL_IN_WAT_TEM_LO: Final = "AllInWatTemLo"
PARAM_ALL_OUT_WAT_TEM_HI: Final = "AllOutWatTemHi"
PARAM_ALL_OUT_WAT_TEM_LO: Final = "AllOutWatTemLo"
PARAM_TEM_UN: Final = "TemUn"
PARAM_ALL_ERR: Final = "AllErr"
PARAM_JF_ERROR_CODE: Final = "JFErrorCode"
PARAM_RSSI: Final = "rssi"
PARAM_MOD: Final = "Mod"
PARAM_POW: Final = "Pow"

# Status parameter keys
PARAM_ASS_HT: Final = "AssHt"
PARAM_ELC_HE1_RUN_STA: Final = "ElcHe1RunSta"
PARAM_ELC_HE2_RUN_STA: Final = "ElcHe2RunSta"
PARAM_WAT_BOX_ELC_HE_RUN_STA: Final = "WatBoxElcHeRunSta"
PARAM_QUIET: Final = "Quiet"
PARAM_FAST_HT_WTER: Final = "FastHtWter"
PARAM_EMEGCY: Final = "Emegcy"
PARAM_AN_FRZZ_RUN_STA: Final = "AnFrzzRunSta"
PARAM_SY_AN_FRO_RUN_STA: Final = "SyAnFroRunSta"

# Diagnostic / device info parameter keys
PARAM_MODEL_TYPE: Final = "ModelType"
PARAM_VERSATI_SERIES: Final = "VersatiSeries"
PARAM_MID: Final = "mid"
PARAM_VER: Final = "ver"
PARAM_HID: Final = "hid"
PARAM_HOST: Final = "host"
PARAM_VENDER: Final = "vender"

# Tuple of all keys that should be polled from the device
POLL_KEYS: Final[tuple[str, ...]] = (
    PARAM_HE_WAT_OUT_TEM_SET,
    PARAM_CO_WAT_OUT_TEM_SET,
    PARAM_WAT_BOX_TEM_SET,
    PARAM_TEM_UN,
    PARAM_ALL_ERR,
    PARAM_JF_ERROR_CODE,
    PARAM_MOD,
    PARAM_POW,
    PARAM_ALL_IN_WAT_TEM_HI,
    PARAM_ALL_IN_WAT_TEM_LO,
    PARAM_ALL_OUT_WAT_TEM_HI,
    PARAM_ALL_OUT_WAT_TEM_LO,
    PARAM_RSSI,
    PARAM_ASS_HT,
    PARAM_ELC_HE1_RUN_STA,
    PARAM_ELC_HE2_RUN_STA,
    PARAM_WAT_BOX_ELC_HE_RUN_STA,
    PARAM_QUIET,
    PARAM_FAST_HT_WTER,
    PARAM_EMEGCY,
    PARAM_AN_FRZZ_RUN_STA,
    PARAM_SY_AN_FRO_RUN_STA,
    PARAM_MODEL_TYPE,
    PARAM_VERSATI_SERIES,
    PARAM_MID,
    PARAM_VER,
    PARAM_HID,
    PARAM_HOST,
    PARAM_VENDER,
)

# Home Assistant services used by the integration
SERVICE_SET_PARAM: Final = "set_param"
SERVICE_GET_PARAMS: Final = "get_params"

# Service/parameter attributes
ATTR_KEY: Final = "key"
ATTR_KEYS: Final = "keys"
ATTR_VALUE: Final = "value"

# Network settings
DEFAULT_MAX_DATAGRAM_BYTES: Final = 8192

# Data keys for storing info in hass.data
DATA: Final = "data"
DATA_ENTRIES: Final = "entries"
DATA_CLIENT: Final = "client"
DATA_COORDINATOR: Final = "coordinator"

# Supported operating mode options (if used by select)
MODE_OPTIONS: Final[dict[str, int]] = {
    "Heat": 1,
    "Cool": 5,
    "Hot water": 2,
    "Cool + hot water": 3,
    "Heat + hot water": 4,
}

# List of supported platforms exposed by the integration
PLATFORMS: Final[tuple[Platform, ...]] = (
    Platform.SENSOR,
    Platform.NUMBER,
    Platform.SELECT,
    Platform.SWITCH,
    Platform.CLIMATE,
)
