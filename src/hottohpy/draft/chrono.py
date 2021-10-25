from .const import *


class Chrono:
    def __init__(self, data):
        self._data = data

    def toJson(self):
        j = "["
        j += "{'name': 'page_index', 'unit': '', 'value':" + self._getPageIndex() + "},"
        j += "{'name': 'state', 'unit': '', 'value:" + self._getState() + "},"
        j += (
            "{'name': 'set_temperature_1', 'unit': '°C', 'value:"
            + self._getSetTemperature1()
            + "},"
        )
        j += (
            "{'name': 'set_max_temperature_1', 'unit': '°C', 'value:"
            + self._getSetMaxTemperature1()
            + "},"
        )
        j += (
            "{'name': 'set_min_temperature_1', 'unit': '°C', 'value:"
            + self._getSetMinTemperature1()
            + "},"
        )
        j += (
            "{'name': 'set_temperature_2', 'unit': '°C', 'value:"
            + self._getSetTemperature2()
            + "},"
        )
        j += (
            "{'name': 'set_max_temperature_2', 'unit': '°C', 'value:"
            + self._getSetMaxTemperature2()
            + "},"
        )
        j += (
            "{'name': 'set_min_temperature_2', 'unit': '°C', 'value:"
            + self._getSetMinTemperature2()
            + "},"
        )
        j += (
            "{'name': 'set_temperature_1', 'unit': '°C', 'value:"
            + self._getSetTemperature3()
            + "},"
        )
        j += (
            "{'name': 'set_max_temperature_1', 'unit': '°C', 'value:"
            + self._getSetMaxTemperature3()
            + "},"
        )
        j += (
            "{'name': 'set_min_temperature_1', 'unit': '°C', 'value:"
            + self._getSetMinTemperature3()
            + "}"
        )
        j += "]"
        return j

    def _getPageIndex(self):
        return self._data[StoveRegisters.INDEX_PAGE]

    def _getState(self):
        return self._data[StoveRegisters.INDEX_STATE]

    def _getSetTemperature1(self):
        return str(int(self._data[StoveRegisters.INDEX_TEMPERATURE_1]) / 10)

    def _getSetMaxTemperature1(self):
        return str(int(self._data[StoveRegisters.INDEX_TEMPERATURE_1_MAX]) / 10)

    def _getSetMinTemperature1(self):
        return str(int(self._data[StoveRegisters.INDEX_TEMPERATURE_1_MIN]) / 10)

    def _getSetTemperature2(self):
        return str(int(self._data[StoveRegisters.INDEX_TEMPERATURE_2]) / 10)

    def _getSetMaxTemperature2(self):
        return str(int(self._data[StoveRegisters.INDEX_TEMPERATURE_2_MAX]) / 10)

    def _getSetMinTemperature2(self):
        return str(int(self._data[StoveRegisters.INDEX_TEMPERATURE_2_MIN]) / 10)

    def _getSetTemperature3(self):
        return str(int(self._data[StoveRegisters.INDEX_TEMPERATURE_3]) / 10)

    def _getSetMaxTemperature3(self):
        return str(int(self._data[StoveRegisters.INDEX_TEMPERATURE_3_MAX]) / 10)

    def _getSetMinTemperature3(self):
        return str(int(self._data[StoveRegisters.INDEX_TEMPERATURE_3_MIN]) / 10)
