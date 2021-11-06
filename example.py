# importing module
import sys
  
# appending a path
sys.path.append('src')
from hottohpy import Hottoh
import time

stove = Hottoh()

stove.connect()

attempt = 1

while True:
    print("Stove Connected: %s", stove.is_connected)
    print("Stove Temperature: %s", stove.get_temperature())
    print("Stove Target Temperature: %s", stove.get_set_temperature())
    print("Stove State: %s", stove.get_action())
    time.sleep(2)

    # if attempt == 5:
    #     stove.setTemperature(19)

    # if attempt == 25:
    #     stove.setTemperature(18)

    # attempt = attempt + 1
