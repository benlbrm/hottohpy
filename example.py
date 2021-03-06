# importing module
import sys
  
# appending a path
sys.path.append('src')
from hottohpy import Hottoh
import time

stove = Hottoh('192.168.4.10' ,5001, "lib")

stove.connect()

attempt = 1

while True:
    print("#### Start Stove Data's ####")
    print("Info: %s", stove.client._info)
    print("Data: %s", stove.client._data)
    print("Data2: %s", stove.client._data2)
    print("_getFirmwareVersion: %s", stove._getFirmwareVersion())
    print("_getWifiSignal: %s", stove._getWifiSignal())
    print("_getPageIndex: %s", stove._getPageIndex())
    print("_getManufacturer: %s", stove._getManufacturer())
    print("_getIsBitmapVisible: %s", stove._getIsBitmapVisible())
    print("_getIsValid: %s", stove._getIsValid())
    print("_getStoveType: %s", stove._getStoveType())
    print("_getStoveState: %s", stove._getStoveState())
    print("_getStoveIsOn: %s", stove._getStoveIsOn())
    print("_getEcoMode: %s", stove._getEcoMode())
    print("_getChronoMode: %s", stove._getChronoMode())
    print("_getTemperatureRoom1: %s", stove._getTemperatureRoom1())
    print("_getSetTemperatureRoom1: %s", stove._getSetTemperatureRoom1())
    print("_getSetMaxTemperatureRoom1: %s", stove._getSetMaxTemperatureRoom1())
    print("_getSetMinTemperatureRoom1: %s", stove._getSetMinTemperatureRoom1())
    print("_getTemperatureRoom2: %s", stove._getTemperatureRoom2())
    print("_getSetTemperatureRoom2: %s", stove._getSetTemperatureRoom2())
    print("_getSetMaxTemperatureRoom2: %s", stove._getSetMaxTemperatureRoom2())
    print("_getSetMinTemperatureRoom2: %s", stove._getSetMinTemperatureRoom2())
    print("_getTemperatureRoom3: %s", stove._getTemperatureRoom3())
    print("_getSetTemperatureRoom3: %s", stove._getSetTemperatureRoom3())
    print("_getSetMaxTemperatureRoom3: %s", stove._getSetMaxTemperatureRoom3())
    print("_getSetMinTemperatureRoom3: %s", stove._getSetMinTemperatureRoom3())
    print("_getTemperatureWater: %s", stove._getTemperatureWater())
    print("_getSetTemperatureWater: %s", stove._getSetTemperatureWater())
    print("_getSetMaxTemperatureWater: %s", stove._getSetMaxTemperatureWater())
    print("_getSetMinTemperatureWater: %s", stove._getSetMinTemperatureWater())
    print("_getSmokeTemperature: %s", stove._getSmokeTemperature())
    print("_getPowerLevel: %s", stove._getPowerLevel())
    print("_getSetPowerLevel: %s", stove._getSetPowerLevel())
    print("_getSetMaxPowerLevel: %s", stove._getSetMaxPowerLevel())
    print("_getSetMinPowerLevel: %s", stove._getSetMinPowerLevel())
    print("_getSpeedFanSmoke: %s", stove._getSpeedFanSmoke())
    print("_getSpeedFan1: %s", stove._getSpeedFan1())
    print("_getSetSpeedFan1: %s", stove._getSetSpeedFan1())
    print("_getSetMaxSpeedFan1: %s", stove._getSetMaxSpeedFan1())
    print("_getSpeedFan2: %s", stove._getSpeedFan2())
    print("_getSetSpeedFan2: %s", stove._getSetSpeedFan2())
    print("_getSetMaxSpeedFan2: %s", stove._getSetMaxSpeedFan2())
    print("_getSpeedFan3: %s", stove._getSpeedFan3())
    print("_getSetSpeedFan3: %s", stove._getSetSpeedFan3())
    print("_getSetMaxSpeedFan3: %s", stove._getSetMaxSpeedFan3())
    print("_getFlowSwitch: %s", stove._getFlowSwitch())
    print("_getGenericPump: %s", stove._getGenericPump())
    print("_getAirEx1: %s", stove._getAirEx1())
    print("_getAirEx2: %s", stove._getAirEx2())
    print("_getAirEx3: %s", stove._getAirEx3())
    print("_getPuffer: %s", stove._getPuffer())
    print("_getSetPuffer: %s", stove._getSetPuffer())
    print("_getSetMinPuffer: %s", stove._getSetMinPuffer())
    print("_getSetMaxPuffer: %s", stove._getSetMaxPuffer())
    print("_getBoiler: %s", stove._getBoiler())
    print("_getSetBoiler: %s", stove._getSetBoiler())
    print("_getSetMinBoiler: %s", stove._getSetMinBoiler())
    print("_getSetMaxBoiler: %s", stove._getSetMaxBoiler())
    print("_getDhw: %s", stove._getDhw())
    print("_getSetDhw: %s", stove._getSetDhw())
    print("_getSetMinDhw: %s", stove._getSetMinDhw())
    print("_getSetMaxDhw: %s", stove._getSetMaxDhw())

    # print("Boiler Enabled: %s", stove._isBoilerEnabled())
    # print("DHW Hot Water Enabled: %s", stove._isDomesticHotWaterEnabled())
    # print("Fan number: %s", stove._getFanNumber())
    # print("Pump Enabled: %s", stove._isPumpEnabled())
    # print("Temp Room 1 Enabled: %s", stove._isTempRoom1Enabled())
    # print("Temp Room 2 Enabled: %s", stove._isTempRoom2Enabled())
    # print("Temp Room 3 Enabled: %s", stove._isTempRoom3Enabled())
    # print("Temp Water Enabled: %s", stove._isTempWaterEnabled())
    print("#### End Stove Data's ####")
    time.sleep(2)

