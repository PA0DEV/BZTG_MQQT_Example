#
# name: Phillip Ahlers 
# created:  25.1.2022
# class: ETS2021
#
#
# use:
# 
# 
# version: 2022_1_25_XXX
# designed and tested on ESP32 TTGO whith XXX
# pin conenctions:
# 
# 
# used external libaries:
# 
# ----------------------------------------
## Initialize i2c for sensor and the sensor ##
from machine import SoftI2C, Pin
from libraries import HTU2X
try:
     import uasyncio as asyncio
except:
    import asyncio

import wifiManager

from mqtt import MQTTClient


global temp
temp = None

global humid
humid = None
# ----------------------------------------
## Initialize i2c for sensor and the sensor ##
busSens = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100000)

humidSens = HTU2X.HTU21D(busSens)

# ----------------------------------------
wlan = wifiManager.getConnection()

if wlan is None:
    print("[WifiMgr] Could not initialize the network connection.")
    while True:
        pass  # you shall not pass :D
else:
    print("[WifiMgr] ESP WiFi OK")
    ## setup mqtt client ##
    mqtt = MQTTClient("Air_Sensor", "10.50.217.155",port=1883)


# ----------------------------------------
## methods to mesure temp and humid async and smooth values ##
async def mesureTmp(num):
    global temp
    while True:
        tempList = []
        for i in range(num):
            tmp = humidSens.temperature
            tempList.append(tmp)
            await asyncio.sleep_ms(1000)

        tempList.sort()
        tempList.pop(0)
        tempList.pop()

        ret = sum(tempList) / len(tempList)

        temp = round(ret, 1)
        print("Temp: %4.1f°C" %temp)


async def mesureHumid(num):
    global humid
    while True:
        humidList = []
        for i in range(num):
            tmp = humidSens.humidity
            humidList.append(tmp)
            await asyncio.sleep_ms(1000)

        humidList.sort()
        humidList.pop(0)
        humidList.pop()

        ret = sum(humidList) / len(humidList)

        humid = round(ret, 0)
        print("Humid: %4.1f %%" %humid)



async def SendData():
    global temp
    global humid
    oldTemp = None
    oldHumid = None

    while True:
        if temp != oldTemp and humid != oldHumid:
            print("[MQTT] Connecting...")
            msg = str("{\"temperature\": \"%4.1f\", \"humid\": \"%4.0f\"}" %(temp, humid))

            mqtt.connect()
            print("[MQTT] Sending data...")
            mqtt.publish(b"Climate", msg)
            print("[MQTT] Data sent!")
            print()
            mqtt.disconnect()
            oldTemp = temp
            oldHumid = humid
        await asyncio.sleep(1)
        


    

async def run():
    #t0 = asyncio.create_task(wifiMgr())
    t2 = asyncio.create_task(mesureHumid(10))
    t1 = asyncio.create_task(mesureTmp(10))
    t3 = asyncio.create_task(SendData())
    
    await t2, t1, t3

asyncio.run(run())