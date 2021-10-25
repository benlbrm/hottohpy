from .const import *


class Boiler:
    def __init__(self, data):
        self._data = data

    def toJson(self):
        j = "["
        j += "{'name': 'page_index', 'unit': '', 'value:" + self.getPageIndex() + "},"
        j += "{'name': 'flow_switch', 'unit': '', 'value:" + self.getFlowSwitch() + "},"
        j += "{'name': 'pump', 'unit': '', 'value:" + self.getPumpState() + "},"
        j += (
            "{'name': 'speed_fan_1', 'unit': 'rpm', 'value:"
            + self.getSpeedFan1()
            + "},"
        )
        j += (
            "{'name': 'speed_fan_2', 'unit': 'rpm', 'value:"
            + self.getSpeedFan2()
            + "},"
        )
        j += (
            "{'name': 'speed_fan_3', 'unit': 'rpm', 'value:"
            + self.getSpeedFan3()
            + "},"
        )
        j += "{'name': 'puffer', 'unit': '', 'value:" + self.getPuffer() + "},"
        j += "{'name': 'set_puffer', 'unit': '', 'value:" + self.getSetPuffer() + "},"
        j += (
            "{'name': 'set_max_puffer', 'unit': '', 'value:"
            + self.getSetMaxPuffer()
            + "},"
        )
        j += (
            "{'name': 'set_min_puffer', 'unit': '', 'value:"
            + self.getSetMinPuffer()
            + "},"
        )
        j += "{'name': 'boiler', 'unit': '', 'value:" + self.getBoiler() + "},"
        j += "{'name': 'set_boiler', 'unit': '', 'value:" + self.getSetBoiler() + "},"
        j += (
            "{'name': 'set_max_boiler', 'unit': '', 'value:"
            + self.getSetMaxBoiler()
            + "},"
        )
        j += (
            "{'name': 'set_min_boiler', 'unit': '', 'value:"
            + self.getSetMinBoiler()
            + "},"
        )
        j += "{'name': 'dhw', 'unit': '', 'value:" + self.getDHW() + "},"
        j += "{'name': 'set_dhw', 'unit': '', 'value:" + self.getSetDHW() + "},"
        j += "{'name': 'set_max_dhw', 'unit': '', 'value:" + self.getSetMaxDHW() + "},"
        j += "{'name': 'set_min_dhw', 'unit': '', 'value:" + self.getSetMinDHW() + "},"
        j += (
            "{'name': 'temperature_room', 'unit': '°C', 'value:"
            + self.getTemperatureRoom()
            + "},"
        )
        j += (
            "{'name': 'set_temperature_room', 'unit': '°C', 'value:"
            + self.getSetTemperatureRoom()
            + "},"
        )
        j += (
            "{'name': 'set_max_temperature_room', 'unit': '°C', 'value:"
            + self.getSetMaxTemperatureRoom()
            + "},"
        )
        j += (
            "{'name': 'set_min_temperature_room', 'unit': '°C', 'value:"
            + self.getSetMinTemperatureRoom()
            + "}"
        )
        j += "]"
        return j

    def getPageIndex(self):
        return self._data[StoveRegisters.INDEX_PAGE]

    def getFlowSwitch(self):
        return self._data[StoveRegisters.INDEX_FLOW_SWITCH]

    def getPumpState(self):
        return self._data[StoveRegisters.INDEX_GENERIC_PUMP]

    def getSpeedFan1(self):
        return self._data[StoveRegisters.INDEX_AIREX_1]

    def getSpeedFan2(self):
        return self._data[StoveRegisters.INDEX_AIREX_2]

    def getSpeedFan3(self):
        return self._data[StoveRegisters.INDEX_AIREX_3]

    def getPuffer(self):
        return str(int(self._data[StoveRegisters.INDEX_PUFFER]) / 10)

    def getSetPuffer(self):
        return str(int(self._data[StoveRegisters.INDEX_PUFFER_SET]) / 10)

    def getSetMinPuffer(self):
        return str(int(self._data[StoveRegisters.INDEX_PUFFER_SET_MIN]) / 10)

    def getSetMaxPuffer(self):
        return str(int(self._data[StoveRegisters.INDEX_PUFFER_SET_MAX]) / 10)

    def getBoiler(self):
        return str(int(self._data[StoveRegisters.INDEX_BOILER]) / 10)

    def getSetBoiler(self):
        return str(int(self._data[StoveRegisters.INDEX_BOILER_SET]) / 10)

    def getSetMinBoiler(self):
        return str(int(self._data[StoveRegisters.INDEX_BOILER_SET_MIN]) / 10)

    def getSetMaxBoiler(self):
        return str(int(self._data[StoveRegisters.INDEX_BOILER_SET_MAX]) / 10)

    def getDHW(self):
        return str(int(self._data[StoveRegisters.INDEX_DHW]) / 10)

    def getSetDHW(self):
        return str(int(self._data[StoveRegisters.INDEX_DHW_SET]) / 10)

    def getSetMinDHW(self):
        return str(int(self._data[StoveRegisters.INDEX_DHW_SET_MIN]) / 10)

    def getSetMaxDHW(self):
        return str(int(self._data[StoveRegisters.INDEX_DHW_SET_MAX]) / 10)

    def getTemperatureRoom(self):
        return str(int(self._data[StoveRegisters.INDEX_ROOM_TEMP_3]) / 10)

    def getSetTemperatureRoom(self):
        return str(int(self._data[StoveRegisters.INDEX_ROOM_TEMP_3_SET]) / 10)

    def getSetMaxTemperatureRoom(self):
        return str(int(self._data[StoveRegisters.INDEX_ROOM_TEMP_3_SET_MAX]) / 10)

    def getSetMinTemperatureRoom(self):
        return str(int(self._data[StoveRegisters.INDEX_ROOM_TEMP_3_SET_MIN]) / 10)
