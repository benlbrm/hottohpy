import asyncio
import threading
import time
from .request import CommandMode, Request
from .const import StoveCommands, StoveRegisters, StoveState, StoveManufacturer
from .client import HottohRemoteClient
import logging
from bitstring import BitArray

# _LOGGER = logging.getLogger(__name__)

MAX_CONNECTION_RETRIES = 3

class HottohConnectionError(Exception):
    """Hottoh connection exception."""

    pass

class Hottoh:
    def __init__(self, address, port, id=0):
        """Communicate with HottoH stove wifi module"""
        self.log = logging.getLogger(__name__)
        self.port = port
        self.address = address
        self.client = HottohRemoteClient(self.address, self.port, id)

    def connect(self):
        self.client.start()

    def disconnect(self):
        self.client.stop()

    def is_connected(self):
        return self.client.is_connected()

    def _extractData(self, data):
        # Split data to an array
        return data.split(";")
            
    def _getMac(self):
        return "aabbccddeeff"

    def set_temperature(self, value):
        """Set Target Temperature of the stove"""
        try:
            result = self.client.sendCommand(
                parameters=[
                    str(StoveCommands.PARAM_AMBIANCE_TEMPERATURE_1.value),
                    str(value * 10),
                ]
            )
            return result
        except:
            raise

    def set_water_temperature(self, value):
        """Set Target Water Temperature of the stove"""
        try:
            result = self.client.sendCommand(
                parameters=[
                    str(StoveCommands.INCONNU_4.value),
                    str(value * 10),
                ]
            )
            return result
        except:
            raise

    def set_power_level(self, value):
        """Set power level of the stove"""
        try:
            result = self.client.sendCommand(
                parameters=[str(StoveCommands.PARAM_NIVEAU_PUISSANCE.value), str(value)]
            )
            return result
        except:
            raise

    def set_speed_fan_1(self, value):
        """Set speed level of Fan 1"""
        try:
            result = self.client.sendCommand(
                parameters=[str(StoveCommands.PARAM_NIVEAU_FAN_1.value), str(value)]
            )
            return result
        except:
            raise

    def set_speed_fan_2(self, value):
        """Set speed level of Fan 2"""
        try:
            result = self.client.sendCommand(
                parameters=[str(StoveCommands.PARAM_NIVEAU_FAN_2.value), str(value)]
            )
            return result
        except:
            raise

    def set_speed_fan_3(self, value):
        """Set speed level of Fan 3"""
        try:
            result = self.client.sendCommand(
                parameters=[str(StoveCommands.PARAM_NIVEAU_FAN_3.value), str(value)]
            )
            return result
        except:
            raise

    def set_eco_mode_on(self):
        """Set Eco Mode of the stove"""
        try:
            result = self.client.sendCommand(
                parameters=[str(StoveCommands.PARAM_ECO_MODE.value), "1"]
            )
            return result
        except:
            raise

    def set_eco_mode_off(self):
        """Set Eco Mode of the stove"""
        try:
            result = self.client.sendCommand(
                parameters=[str(StoveCommands.PARAM_ECO_MODE.value), "0"]
            )
            return result
        except:
            raise

    def set_chrono_mode_on(self):
        """Set Eco Mode of the stove"""
        try:
            result = self.client.sendCommand(
                parameters=[str(StoveCommands.PARAM_CHRONO_ON_OFF.value), "1"]
            )
            return result
        except:
            raise

    def set_chrono_mode_off(self):
        """Set Eco Mode of the stove"""
        try:
            result = self.client.sendCommand(
                parameters=[str(StoveCommands.PARAM_CHRONO_ON_OFF.value), "0"]
            )
            return result
        except:
            raise

    def set_on(self):
        """Set On/ Off  the stove"""
        try:
            result = self.client.sendCommand(
                parameters=[str(StoveCommands.PARAM_ON_OFF.value), "1"]
            )
            return result
        except:
            raise

    def set_off(self):
        """Set On/ Off  the stove"""
        try:
            result = self.client.sendCommand(
                parameters=[str(StoveCommands.PARAM_ON_OFF.value), "0"]
            )
            return result
        except:
            raise

    def get_smoke_temperature(self):
        return float(self._getSmokeTemperature())

    def get_water_temperature(self):
        return float(self._getTemperatureWater())

    def get_set_water_temperature(self):
        return float(self._getSetTemperatureWater())

    def get_set_min_water_temperature(self):
        return float(self._getSetMinTemperatureWater())

    def get_set_max_water_temperature(self):
        return float(self._getSetMaxTemperatureWater())

    def get_speed_fan_smoke(self):
        return float(self._getSpeedFanSmoke())

    def get_temperature_room_1(self):
        return float(self._getTemperatureRoom1())
    
    def get_set_temperature_room_1(self):
        return float(self._getSetTemperatureRoom1())

    def get_set_min_temperature_room_1(self):
        return float(self._getSetMinTemperatureRoom1())

    def get_set_max_temperature_room_1(self):
        return float(self._getSetMaxTemperatureRoom1())

    def get_temperature_room_2(self):
        return float(self._getTemperatureRoom2())
    
    def get_set_temperature_room_2(self):
        return float(self._getSetTemperatureRoom2())

    def get_set_min_temperature_room_2(self):
        return float(self._getSetMinTemperatureRoom2())

    def get_set_max_temperature_room_2(self):
        return float(self._getSetMaxTemperatureRoom2())

    def get_temperature_room_3(self):
        return float(self._getTemperatureRoom3())
    
    def get_set_temperature_room_3(self):
        return float(self._getSetTemperatureRoom3())

    def get_set_min_temperature_room_3(self):
        return float(self._getSetMinTemperatureRoom3())

    def get_set_max_temperature_room_3(self):
        return float(self._getSetMaxTemperatureRoom3())

    def get_speed_fan_1(self):
        return int(self._getSpeedFan1())

    def get_set_speed_fan_1(self):
        return int(self._getSetSpeedFan1())

    def get_set_max_speed_fan_1(self):
        return int(self._getSetMaxSpeedFan1())

    def get_speed_fan_2(self):
        return float(self._getSpeedFan2())

    def get_set_speed_fan_2(self):
        return float(self._getSetSpeedFan2())

    def get_set_max_speed_fan_2(self):
        return float(self._getSetMaxSpeedFan2())

    def get_speed_fan_3(self):
        return float(self._getSpeedFan3())

    def get_set_speed_fan_3(self):
        return float(self._getSetSpeedFan3())

    def get_set_max_speed_fan_3(self):
        return float(self._getSetMaxSpeedFan3()) 

    def get_power_level(self):
        return float(self._getPowerLevel())
    
    def get_set_power_level(self):
        return float(self._getSetPowerLevel())

    def get_set_min_power_level(self):
        return float(self._getSetMinPowerLevel())

    def get_set_max_power_level(self):
        return float(self._getSetMaxPowerLevel())

    def get_air_ex_1(self):
        return float(self._getAirEx1())

    def get_air_ex_2(self):
        return float(self._getAirEx2())

    def get_air_ex_3(self):
        return float(self._getAirEx3())

    def get_action(self):
        if self._getStoveState() in ['switched_off', 'black_out', 'eco_stop_2', 'eco_stop_3']:
            return 'off'
        if self._getStoveState() in ['starting_1_check']:
            return 'check'
        if self._getStoveState() in ['starting_2_clean_all']:
            return 'clean_all'
        if self._getStoveState() in ['starting_3_loading']:
            return 'loading'
        if self._getStoveState() in ['starting_4_waiting', 'starting_5_waiting']:
            return 'waiting'
        if self._getStoveState() in ['starting_6_ignition']:
            return 'ignition'
        if self._getStoveState() in ['starting_7_stabilization']:
            return 'stabilization'
        if self._getStoveState() in ['power']:
            return 'heating'
        if self._getStoveState() in ['stopping_1_wait_standby', 'stopping_2_wait_standby']:
            return 'stopping'
        if self._getStoveState() in ['eco_stop_1_standby', 'standby']:
            return 'idle'
        return self._getStoveState()

    def get_is_on(self):
        return self._getStoveIsOn() == 'on'

    def get_eco_mode(self):
        return self._getEcoMode() == 'on'

    def get_chrono_mode(self):
        return self._getChronoMode() == 'on'
        
    def get_mode(self):
        return self._getStoveIsOn()

    def get_name(self):
        if self.get_manufacturer() is None:
            return None
        return "Stove " + self.get_manufacturer()
        
    def get_firmware(self):
        return self._getFirmwareVersion()

    def get_wifi(self):
        return self._getWifiSignal()

    def get_manufacturer(self):
        return self._getManufacturer()

    def get_water_pump(self):
        if int(self._getGenericPump()) == 0:
            return False
        return True

    def _getFirmwareVersion(self):
        if self.client._info is None:
            return None
        return self.client._info[StoveRegisters.INDEX_FW]

    def _getWifiSignal(self):
        if self.client._info is None:
            return None
        return self.client._info[StoveRegisters.INDEX_WIFI]

    def _getPageIndex(self):
        if self.client._data is None:
            return None
        return self.client._data[StoveRegisters.INDEX_PAGE]

    def _getManufacturer(self):
        if self.client._data is None:
            return None
        if int(self.client._data[StoveRegisters.INDEX_MANUFACTURER]) == StoveManufacturer.STOVE_MANUFACTURER_CMG:
            return "CMG"
        if int(self.client._data[StoveRegisters.INDEX_MANUFACTURER]) == StoveManufacturer.STOVE_MANUFACTURER_EDILKAMIN:
            return "EdilKamin"
        return str(self.client._data[StoveRegisters.INDEX_MANUFACTURER])

    def _getIsBitmapVisible(self):
        if self.client._data is None:
            return None
        return self.client._data[StoveRegisters.INDEX_BITMAP_VISIBLE]

    def _getIsValid(self):
        if self.client._data is None:
            return None
        return self.client._data[StoveRegisters.INDEX_VALID]

    def _getStoveType(self):
        if self.client._data is None:
            return 0
        return int(self.client._data[StoveRegisters.INDEX_STOVE_TYPE])

    def _getStoveState(self):
        if self.client._data is None:
            return "not_connected"
        if StoveState.STATUS_OFF == int(self.client._data[StoveRegisters.INDEX_STOVE_STATE]):
            return "switched_off"
        if StoveState.STATUS_STARTING_1 == int(self.client._data[StoveRegisters.INDEX_STOVE_STATE]):
            return "starting_1_check"
        if StoveState.STATUS_STARTING_2 == int(self.client._data[StoveRegisters.INDEX_STOVE_STATE]):
            return "starting_2_clean_all"
        if StoveState.STATUS_STARTING_3 == int(self.client._data[StoveRegisters.INDEX_STOVE_STATE]):
            return "starting_3_loading"
        if StoveState.STATUS_STARTING_4 == int(self.client._data[StoveRegisters.INDEX_STOVE_STATE]):
            return "starting_4_waiting"
        if StoveState.STATUS_STARTING_5 == int(self.client._data[StoveRegisters.INDEX_STOVE_STATE]):
            return "starting_5_waiting"
        if StoveState.STATUS_STARTING_6 == int(self.client._data[StoveRegisters.INDEX_STOVE_STATE]):
            return "starting_6_ignition"
        if StoveState.STATUS_STARTING_7 == int(self.client._data[StoveRegisters.INDEX_STOVE_STATE]):
            return "starting_7_stabilization"
        if StoveState.STATUS_POWER == int(self.client._data[StoveRegisters.INDEX_STOVE_STATE]):
            return "power"
        if StoveState.STATUS_STOPPING_1 == int(self.client._data[StoveRegisters.INDEX_STOVE_STATE]):
            return "stopping_1_wait_standby"
        if StoveState.STATUS_STOPPING_2 == int(self.client._data[StoveRegisters.INDEX_STOVE_STATE]):
            return "stopping_2_wait_standby"
        if StoveState.STATUS_ECO_STOP_1 == int(self.client._data[StoveRegisters.INDEX_STOVE_STATE]):
            return "eco_stop_1_standby"
        if StoveState.STATUS_ECO_STOP_2 == int(self.client._data[StoveRegisters.INDEX_STOVE_STATE]):
            return "eco_stop_2"
        if StoveState.STATUS_ECO_STOP_3 == int(self.client._data[StoveRegisters.INDEX_STOVE_STATE]):
            return "eco_stop_3"
        if StoveState.STATUS_LOW_PELLET == int(self.client._data[StoveRegisters.INDEX_STOVE_STATE]):
            return "low_pellet"
        if StoveState.STATUS_END_PELLET == int(self.client._data[StoveRegisters.INDEX_STOVE_STATE]):
            return "end_pellet"
        if StoveState.STATUS_BLACK_OUT == int(self.client._data[StoveRegisters.INDEX_STOVE_STATE]):
            return "black_out"
        if StoveState.STATUS_INGNITION_FAILED == int(self.client._data[StoveRegisters.INDEX_STOVE_STATE]):
            return "error_ignition_failed"
        if StoveState.STATUS_ANTI_FREEZE == int(self.client._data[StoveRegisters.INDEX_STOVE_STATE]):
            return "anti_freeze"
        if StoveState.STATUS_COVER_OPEN == int(self.client._data[StoveRegisters.INDEX_STOVE_STATE]):
            return "error_cover_open"
        if StoveState.STATUS_NO_PELLET== int(self.client._data[StoveRegisters.INDEX_STOVE_STATE]):
            return "error_no_pellet"
        return str(self.client._data[StoveRegisters.INDEX_STOVE_STATE])

    def _getStoveIsOn(self):
        if self.client._data is None:
            return None
        if self.client._data[StoveRegisters.INDEX_STOVE_ON] == "1":
            return "on"
        else:
            return "off"

    def _getEcoMode(self):
        if self.client._data is None:
            return None
        if self.client._data[StoveRegisters.INDEX_ECO_MODE] == "1":
            return "on"
        else:
            return "off"

    def _getChronoMode(self):
        if self.client._data is None:
            return None
        if self.client._data[StoveRegisters.INDEX_TIMER_ON] == "1":
            return "on"
        else:
            return "off"

    def _getTemperatureRoom1(self):
        if self.client._data is not None:
            return str(int(self.client._data[StoveRegisters.INDEX_AMBIENT_T1]) / 10)
        return 0

    def _getSetTemperatureRoom1(self):
        if self.client._data is not None:
            return str(int(self.client._data[StoveRegisters.INDEX_AMBIENT_T1_SET]) / 10)
        return 0

    def _getSetMaxTemperatureRoom1(self):
        if self.client._data is None:
            return 0
        return str(int(self.client._data[StoveRegisters.INDEX_AMBIENT_T1_SET_MAX]) / 10)

    def _getSetMinTemperatureRoom1(self):
        if self.client._data is None:
            return 0
        return str(int(self.client._data[StoveRegisters.INDEX_AMBIENT_T1_SET_MIN]) / 10)

    def _getTemperatureRoom2(self):
        if self.client._data is None:
            return 0
        return str(int(self.client._data[StoveRegisters.INDEX_AMBIENT_T2]) / 10)

    def _getSetTemperatureRoom2(self):
        if self.client._data is None:
            return 0
        return str(int(self.client._data[StoveRegisters.INDEX_AMBIENT_T2_SET]) / 10)

    def _getSetMaxTemperatureRoom2(self):
        if self.client._data is None:
            return 0
        return str(int(self.client._data[StoveRegisters.INDEX_AMBIENT_T2_SET_MAX]) / 10)

    def _getSetMinTemperatureRoom2(self):
        if self.client._data is None:
            return 0
        return str(int(self.client._data[StoveRegisters.INDEX_AMBIENT_T2_SET_MIN]) / 10)

    def _getTemperatureRoom3(self):
        if self.client._data2 is None:
            return None
        return str(int(self.client._data2[StoveRegisters.INDEX_ROOM_TEMP_3]) / 10)

    def _getSetTemperatureRoom3(self):
        if self.client._data2 is None:
            return None
        return str(int(self.client._data2[StoveRegisters.INDEX_ROOM_TEMP_3_SET]) / 10)

    def _getSetMinTemperatureRoom3(self):
        if self.client._data2 is None:
            return None
        return str(int(self.client._data2[StoveRegisters.INDEX_ROOM_TEMP_3_SET_MIN]) / 10)

    def _getSetMaxTemperatureRoom3(self):
        if self.client._data2 is None:
            return None
        return str(int(self.client._data2[StoveRegisters.INDEX_ROOM_TEMP_3_SET_MAX]) / 10)

    def _getTemperatureWater(self):
        if self.client._data is None:
            return 0
        return str(int(self.client._data[StoveRegisters.INDEX_WATER]) / 10)

    def _getSetTemperatureWater(self):
        if self.client._data is None:
            return 0
        return str(int(self.client._data[StoveRegisters.INDEX_WATER_SET]) / 10)

    def _getSetMaxTemperatureWater(self):
        if self.client._data is None:
            return 0
        return str(int(self.client._data[StoveRegisters.INDEX_WATER_SET_MAX]) / 10)

    def _getSetMinTemperatureWater(self):
        if self.client._data is None:
            return 0
        return str(int(self.client._data[StoveRegisters.INDEX_WATER_SET_MIN]) / 10)

    def _getSmokeTemperature(self):
        if self.client._data is not None:
            return str(int(self.client._data[StoveRegisters.INDEX_SMOKE_T]) / 10)
        return 0

    def _getPowerLevel(self):
        if self.client._data is None:
            return 0
        return self.client._data[StoveRegisters.INDEX_POWER_LEVEL]

    def _getSetPowerLevel(self):
        if self.client._data is None:
            return 0
        return self.client._data[StoveRegisters.INDEX_POWER_SET]

    def _getSetMaxPowerLevel(self):
        if self.client._data is None:
            return 0
        return self.client._data[StoveRegisters.INDEX_POWER_MAX]

    def _getSetMinPowerLevel(self):
        if self.client._data is None:
            return 0
        return self.client._data[StoveRegisters.INDEX_POWER_MIN]

    def _getSpeedFanSmoke(self):
        if self.client._data is None:
            return 0
        return self.client._data[StoveRegisters.INDEX_FAN_SMOKE]

    def _getSpeedFan1(self):
        if self.client._data is None:
            return 0
        return self.client._data[StoveRegisters.INDEX_FAN_1]

    def _getSetSpeedFan1(self):
        if self.client._data is None:
            return 0
        return self.client._data[StoveRegisters.INDEX_FAN_1_SET]

    def _getSetMaxSpeedFan1(self):
        if self.client._data is None:
            return 0
        return self.client._data[StoveRegisters.INDEX_FAN_1_SET_MAX]

    def _getSpeedFan2(self):
        if self.client._data is None:
            return 0
        return self.client._data[StoveRegisters.INDEX_FAN_2]

    def _getSetSpeedFan2(self):
        if self.client._data is None:
            return 0
        return self.client._data[StoveRegisters.INDEX_FAN_2_SET]

    def _getSetMaxSpeedFan2(self):
        if self.client._data is None:
            return 0
        return self.client._data[StoveRegisters.INDEX_FAN_2_SET_MAX]

    def _getSpeedFan3(self):
        if self.client._data is None:
            return 0
        return self.client._data[StoveRegisters.INDEX_FAN_3]

    def _getSetSpeedFan3(self):
        if self.client._data is None:
            return 0
        return self.client._data[StoveRegisters.INDEX_FAN_3_SET]

    def _getSetMaxSpeedFan3(self):
        if self.client._data is None:
            return 0
        return self.client._data[StoveRegisters.INDEX_FAN_3_SET_MAX]

## Datapoints from data2
    def _getFlowSwitch(self):
        if self.client._data2 is None:
            return 0
        return self.client._data2[StoveRegisters.INDEX_FLOW_SWITCH]

    def _getGenericPump(self):
        if self.client._data2 is None:
            return 0
        return self.client._data2[StoveRegisters.INDEX_GENERIC_PUMP]

    def _getAirEx1(self):
        if self.client._data2 is None:
            return None
        return self.client._data2[StoveRegisters.INDEX_AIREX_1]

    def _getAirEx2(self):
        if self.client._data2 is None:
            return None
        return self.client._data2[StoveRegisters.INDEX_AIREX_2]

    def _getAirEx3(self):
        if self.client._data2 is None:
            return None
        return self.client._data2[StoveRegisters.INDEX_AIREX_3]

    def _getPuffer(self):
        if self.client._data2 is None:
            return None
        return self.client._data2[StoveRegisters.INDEX_PUFFER]

    def _getSetPuffer(self):
        if self.client._data2 is None:
            return None
        return self.client._data2[StoveRegisters.INDEX_PUFFER_SET]

    def _getSetMinPuffer(self):
        if self.client._data2 is None:
            return None
        return self.client._data2[StoveRegisters.INDEX_PUFFER_SET_MIN]

    def _getSetMaxPuffer(self):
        if self.client._data2 is None:
            return None
        return self.client._data2[StoveRegisters.INDEX_PUFFER_SET_MAX]

    def _getBoiler(self):
        if self.client._data2 is None:
            return None
        return self.client._data2[StoveRegisters.INDEX_BOILER]

    def _getSetBoiler(self):
        if self.client._data2 is None:
            return None
        return self.client._data2[StoveRegisters.INDEX_BOILER_SET]

    def _getSetMinBoiler(self):
        if self.client._data2 is None:
            return None
        return self.client._data2[StoveRegisters.INDEX_BOILER_SET_MIN]

    def _getSetMaxBoiler(self):
        if self.client._data2 is None:
            return None
        return self.client._data2[StoveRegisters.INDEX_BOILER_SET_MAX]

    def _getDhw(self):
        if self.client._data2 is None:
            return None
        return self.client._data2[StoveRegisters.INDEX_DHW]

    def _getSetDhw(self):
        if self.client._data2 is None:
            return None
        return self.client._data2[StoveRegisters.INDEX_DHW_SET]

    def _getSetMinDhw(self):
        if self.client._data2 is None:
            return None
        return self.client._data2[StoveRegisters.INDEX_DHW_SET_MIN]

    def _getSetMaxDhw(self):
        if self.client._data2 is None:
            return None
        return self.client._data2[StoveRegisters.INDEX_DHW_SET_MAX]

    def _getStoveTypeBitArray(self):
        return BitArray(uint=self._getStoveType(), length=16)

    def isBoilerEnabled(self):
        type = self._getStoveTypeBitArray()
        return type[9]

    def isDomesticHotWaterEnabled(self):
        type = self._getStoveTypeBitArray()
        return type[10]

    def getFanNumber(self):
        type = self._getStoveTypeBitArray()
        nb = type[12:14]
        return nb.int
    
    def isTempRoom1Enabled(self):
        type = self._getStoveTypeBitArray()
        return type[15]

    def isTempRoom2Enabled(self):
        type = self._getStoveTypeBitArray()
        return type[8]

    def isTempRoom3Enabled(self):
        type = self._getStoveTypeBitArray()
        return type[7]

    def isTempWaterEnabled(self):
        type = self._getStoveTypeBitArray()
        return type[14]

    def isPumpEnabled(self):
        type = self._getStoveTypeBitArray()
        return type[4]

