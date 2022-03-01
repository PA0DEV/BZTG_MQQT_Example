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
from libraries import HTU2X, bh1750
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

global luminance
luminance = None
# ----------------------------------------
## Initialize i2c for sensor and the sensors ##
busSens = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100000)

humidSens = HTU2X.HTU21D(busSens)
lightSens = bh1750.BH1750(busSens)

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
## methods to mesure temp, humid and light density async and smooth values ##
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

async def mesureLuminance(num):
    global luminance
    while True:
        lumiList = []
        for i in range(num):
            lum = lightSens.luminance(bh1750.BH1750.ONCE_HIRES_1)
            lumiList.append(lum)
            await asyncio.sleep_ms(1000)

        lumiList.sort()
        lumiList.pop(0)
        lumiList.pop()

        ret = sum(lumiList) / len(lumiList)

        luminance = round(ret, 0)
        print("Luminance: %4.1f Lux" %luminance)

async def SendData():
    global temp
    global humid
    global luminance
    oldTemp = None
    oldHumid = None
    oldLum = None

    while True:
        if temp != oldTemp or humid != oldHumid or luminance != oldLum:
            try:
                print("[MQTT] Connecting...")
                msg = str("{\"temperature\": \"%4.1f\", \"humid\": \"%4.0f\", \"luminance\": %4.1f}" %(temp, humid, luminance))

                mqtt.connect()
                print("[MQTT] Sending data...")
                mqtt.publish(b"Climate", msg)
                print("[MQTT] Data sent!")
                print()
                mqtt.disconnect()
                oldTemp = temp
                oldHumid = humid
                oldLum = luminance

            except:
                print("[MQTT] Could not reach server...")
                print("[MQTT] No data sent!")
        await asyncio.sleep(1)
    

async def run():
    t2 = asyncio.create_task(mesureHumid(10))
    t1 = asyncio.create_task(mesureTmp(10))
    t4 = asyncio.create_task(mesureLuminance(10))
    t3 = asyncio.create_task(SendData())
    
    await t1, t2, t3, t4

asyncio.run(run())