import asyncio
import threading
import time
from .request import CommandMode, Request
from .const import StoveCommands, StoveRegisters, StoveState
from .client import HottohRemoteClient
import logging

# _LOGGER = logging.getLogger(__name__)

MAX_CONNECTION_RETRIES = 3

class HottohConnectionError(Exception):
    """Hottoh connection exception."""

    pass

class Hottoh:
    _fetching = False
    def __init__(self, address, port):
        """Communicate with HottoH stove wifi module"""
        self.log = logging.getLogger(__name__)
        self.port = port
        self.address = address
        self._buffsize = 1024
        self.is_connected = False
        self.hottoh_connected = False
        self._reader = None
        self._writer = None
        self.client = HottohRemoteClient(self.address, self.port)
        self.delay = 1
        self.periodic_connection_running = False
        self.stop_connection = False
        self._thread = threading.Thread(
            target=self.periodic_connection, name="hottohpy"
        )
        self.client_error = None
        self.on_disconnect_callbacks = []

    def register_on_disconnect_callback(self, callback):
        self.on_disconnect_callbacks.append(callback)

    def periodic_connection(self):
        # only one connection thread at a time!
        if self.periodic_connection_running:
            return
        self.periodic_connection_running = True
        while not self.stop_connection:
            try:
                self.is_connected = self._connect()
            except HottohConnectionError as error:
                self.periodic_connection_running = False
                self.on_disconnect(error)
                return
            time.sleep(self.delay)

        self.client.disconnect()
        self.periodic_connection_running = False

    def connect(self):
        if self.is_connected or self.periodic_connection_running:
            return

        self._thread.daemon = True
        self._thread.start()
        
        self.time = time.time()  # save connection time

    def _connect(self):
        is_connected = self.client.connect()
        if not is_connected:
            raise HottohConnectionError(
                "Unable to connect to Hottoh at {}".format(
                    self.client.address
                )
            )
        return is_connected

    def disconnect(self):
        self.stop_connection = True

    def on_disconnect(self, error):
        self.hottoh_connected = False
        self.client_error = error
        if error is not None:
            self.log.warning(
                "Unexpectedly disconnected from Hottoh %s, code %s",
                self.client.address,
                error,
            )

            # call the callback functions
            for callback in self.on_disconnect_callbacks:
                callback(error)

            return

        self.log.info("Disconnected from Hottoh %s", self.client.address)

    def check(self):
        """Test connectivity with the stove."""
        return self.client.check()

    def _extractData(self, data):
        # Split data to an array
        return data.split(";")
            
    def _getMac(self):
        return "aabbccddeeff"

    async def _setCommand(self, parameters):
        """Set data from to the stove"""
        # mutex.acquire()
        request = Request(command="DAT", mode="W", parameters=parameters)
        reader, writer = await asyncio.open_connection(self.ip, self.port)
        writer.write(request.getRequest())
        await writer.drain()
        data = await reader.read(self._buffsize)
        self.log.debug(data)
        writer.close()
        await writer.wait_closed()
        # mutex.release()
        return self._extractData(f"{data}")

    def setTemperature(self, value):
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

    def setPowerLevel(self, value):
        """Set power level of the stove"""
        try:
            result = self.client.sendCommand(
                parameters=[str(StoveCommands.PARAM_NIVEAU_PUISSANCE.value), str(value)]
            )
            return result
        except:
            raise

    def setEcoModeOn(self):
        """Set Eco Mode of the stove"""
        try:
            result = self.client.sendCommand(
                parameters=[str(StoveCommands.PARAM_ECO_MODE.value), "1"]
            )
            return result
        except:
            raise

    def setEcoModeOff(self):
        """Set Eco Mode of the stove"""
        try:
            result = self.client.sendCommand(
                parameters=[str(StoveCommands.PARAM_ECO_MODE.value), "0"]
            )
            return result
        except:
            raise

    def setChronoModeOn(self):
        """Set Eco Mode of the stove"""
        try:
            result = self.client.sendCommand(
                parameters=[str(StoveCommands.PARAM_CHRONO_ON_OFF.value), "1"]
            )
            return result
        except:
            raise

    def setChronoModeOff(self):
        """Set Eco Mode of the stove"""
        try:
            result = self.client.sendCommand(
                parameters=[str(StoveCommands.PARAM_CHRONO_ON_OFF.value), "0"]
            )
            return result
        except:
            raise

    def setOn(self):
        """Set On/ Off  the stove"""
        try:
            result = self.client.sendCommand(
                parameters=[str(StoveCommands.PARAM_ON_OFF.value), "1"]
            )
            return result
        except:
            raise

    def setOff(self):
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

    def get_fan_speed(self):
        return float(self._getSpeedFanSmoke())

    def get_temperature(self):
        return float(self._getTemperatureRoom1())
    
    def get_set_temperature(self):
        return float(self._getSetTemperatureRoom1())
    
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
        if self._getStoveState() in ['low_pellet', 'end_pellet']:
            return 'end_pellet'
        return 'off'

    def get_is_on(self):
        return self._getStoveIsOn() == 'on'

    def get_eco_mode(self):
        return self._getEcoMode() == 'on'
        
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
        if self.client._data[StoveRegisters.INDEX_MANUFACTURER] == "9":
            return "CMG"
        else:
            return str(self._data[StoveRegisters.INDEX_MANUFACTURER])

    def _getIsBitmapVisible(self):
        if self.client._data is None:
            return None
        return self.client._data[StoveRegisters.INDEX_BITMAP_VISIBLE]

    def _getIsValid(self):
        if self.client._data is None:
            return None
        return self._data[StoveRegisters.INDEX_VALID]

    def _getStoveType(self):
        if self.client._data is None:
            return None
        return str(self.client._data[StoveRegisters.INDEX_STOVE_TYPE])

    def _getStoveState(self):
        if self.client._data is None:
            return "not_connected"
        if StoveState.STATUS_OFF == int(
            self.client._data[StoveRegisters.INDEX_STOVE_STATE]
        ):
            return "switched_off"
        if StoveState.STATUS_STARTING_1 == int(
            self.client._data[StoveRegisters.INDEX_STOVE_STATE]
        ):
            return "starting_1_check"
        if StoveState.STATUS_STARTING_2 == int(
            self.client._data[StoveRegisters.INDEX_STOVE_STATE]
        ):
            return "starting_2_clean_all"
        if StoveState.STATUS_STARTING_3 == int(
            self.client._data[StoveRegisters.INDEX_STOVE_STATE]
        ):
            return "starting_3_loading"
        if StoveState.STATUS_STARTING_4 == int(
            self.client._data[StoveRegisters.INDEX_STOVE_STATE]
        ):
            return "starting_4_waiting"
        if StoveState.STATUS_STARTING_5 == int(
            self.client._data[StoveRegisters.INDEX_STOVE_STATE]
        ):
            return "starting_5_waiting"
        if StoveState.STATUS_STARTING_6 == int(
            self.client._data[StoveRegisters.INDEX_STOVE_STATE]
        ):
            return "starting_6_ignition"
        if StoveState.STATUS_STARTING_7 == int(
            self.client._data[StoveRegisters.INDEX_STOVE_STATE]
        ):
            return "starting_7_stabilization"
        if StoveState.STATUS_POWER == int(self.client._data[StoveRegisters.INDEX_STOVE_STATE]):
            return "power"
        if StoveState.STATUS_STOPPING_1 == int(
            self.client._data[StoveRegisters.INDEX_STOVE_STATE]
        ):
            return "stopping_1_wait_standby"
        if StoveState.STATUS_STOPPING_2 == int(
            self.client._data[StoveRegisters.INDEX_STOVE_STATE]
        ):
            return "stopping_2_wait_standby"
        if StoveState.STATUS_ECO_STOP_1 == int(
            self.client._data[StoveRegisters.INDEX_STOVE_STATE]
        ):
            return "eco_stop_1_standby"
        if StoveState.STATUS_ECO_STOP_2 == int(
            self.client._data[StoveRegisters.INDEX_STOVE_STATE]
        ):
            return "eco_stop_2"
        if StoveState.STATUS_ECO_STOP_3 == int(
            self.client._data[StoveRegisters.INDEX_STOVE_STATE]
        ):
            return "eco_stop_3"
        if StoveState.STATUS_LOW_PELLET == int(
            self.client._data[StoveRegisters.INDEX_STOVE_STATE]
        ):
            return "low_pellet"
        if StoveState.STATUS_END_PELLET == int(
            self.client._data[StoveRegisters.INDEX_STOVE_STATE]
        ):
            return "end_pellet"
        if StoveState.STATUS_BLACK_OUT == int(
            self.client._data[StoveRegisters.INDEX_STOVE_STATE]
        ):
            return "black_out"
        if (
            StoveState.STATUS_ANTI_FREEZE
            == self.client._data[StoveRegisters.INDEX_STOVE_STATE]
        ):
            return "anti_freeze"

    def _getStoveIsOn(self):
        if self.client._data[StoveRegisters.INDEX_STOVE_ON] == "1":
            return "on"
        else:
            return "off"

    def _getEcoMode(self):
        if self.client._data[StoveRegisters.INDEX_ECO_MODE] == "1":
            return "on"
        else:
            return "off"

    def _getChronoMode(self):
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
        return str(int(self.client._data[StoveRegisters.INDEX_AMBIENT_T1_SET_MAX]) / 10)

    def _getSetMinTemperatureRoom1(self):
        return str(int(self.client._data[StoveRegisters.INDEX_AMBIENT_T1_SET_MIN]) / 10)

    def _getTemperatureRoom2(self):
        return str(int(self.client._data[StoveRegisters.INDEX_AMBIENT_T2]) / 10)

    def _getSetTemperatureRoom2(self):
        return str(int(self.client._data[StoveRegisters.INDEX_AMBIENT_T2_SET]) / 10)

    def _getSetMaxTemperatureRoom2(self):
        return str(int(self.client._data[StoveRegisters.INDEX_AMBIENT_T2_SET_MAX]) / 10)

    def _getSetMinTemperatureRoom2(self):
        return str(int(self.client._data[StoveRegisters.INDEX_AMBIENT_T2_SET_MIN]) / 10)

    def _getTemperatureWater(self):
        return str(int(self.client._data[StoveRegisters.INDEX_WATER]) / 10)

    def _getSetTemperatureWater(self):
        return str(int(self.client._data[StoveRegisters.INDEX_WATER_SET]) / 10)

    def _getSetMaxTemperatureWater(self):
        return str(int(self.client._data[StoveRegisters.INDEX_WATER_SET_MAX]) / 10)

    def _getSetMinTemperatureWater(self):
        return str(int(self.client._data[StoveRegisters.INDEX_WATER_SET_MIN]) / 10)

    def _getSmokeTemperature(self):
        if self.client._data is not None:
            return str(int(self.client._data[StoveRegisters.INDEX_SMOKE_T]) / 10)
        return 0

    def _getPowerLevel(self):
        return self.client._data[StoveRegisters.INDEX_POWER_LEVEL]

    def _getSetPowerLevel(self):
        return self.client._data[StoveRegisters.INDEX_POWER_SET]

    def _getSetMaxPowerLevel(self):
        return self.client._data[StoveRegisters.INDEX_POWER_MAX]

    def _getSetMinPowerLevel(self):
        return self.client._data[StoveRegisters.INDEX_POWER_MIN]

    def _getSpeedFanSmoke(self):
        return self.client._data[StoveRegisters.INDEX_FAN_SMOKE]

    def _getSpeedFan1(self):
        return self.client._data[StoveRegisters.INDEX_FAN_1]

    def _getSetSpeedFan1(self):
        return self.client._data[StoveRegisters.INDEX_FAN_1_SET]

    def _getSetMaxSpeedFan1(self):
        return self.client._data[StoveRegisters.INDEX_FAN_1_SET_MAX]

    def _getSpeedFan2(self):
        return self.client._data[StoveRegisters.INDEX_FAN_2]

    def _getSetSpeedFan2(self):
        return self.client._data[StoveRegisters.INDEX_FAN_2_SET]

    def _getSetMaxSpeedFan2(self):
        return self.client._data[StoveRegisters.INDEX_FAN_2_SET_MAX]

    def _getSpeedFan3(self):
        return self.client._data[StoveRegisters.INDEX_FAN_3]

    def _getSetSpeedFan3(self):
        return self.client._data[StoveRegisters.INDEX_FAN_3_SET]

    def _getSetMaxSpeedFan3(self):
        return self.client._data[StoveRegisters.INDEX_FAN_3_SET_MAX]
