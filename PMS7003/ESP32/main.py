#----------------------------------------------------------------
#Author: Damian Sarna, 20.12.2024
#Script using for read data from sensor PMS7003 connected to XBEE 3
#Prepared as part of a diploma thesis: "ZigBee standard in IoT end device communication"
#Script use library: https://github.com/pkucmus/micropython-pms7003
#----------------------------------------------------------------
from pms7003 import Pms7003
import time
from aqi import AQI
from machine import UART, Timer

# Inicjalizacja czujnika PMS7003 na UART2
pms = Pms7003(uart=2)
print("PMS initialized")

# Inicjalizacja UART1 dla wysyłania danych
uart1 = UART(1, baudrate=9600, tx=21, rx=22)

def send_pm_data(timer):
    try:
        # Odczyt danych z czujnika
        pms_data = pms.read()
        aqi = AQI.aqi(pms_data['PM2_5_ATM'], pms_data['PM10_0_ATM'])
        aqi = round(aqi, 2)
        pm1 = pms_data['PM1_0']
        pm25 = pms_data['PM2_5']
        pm10 = pms_data['PM10_0']
        print(pms_data)
        print(aqi)
        
        # Kodowanie danych w odpowiednim formacie
        encoded_data = f"{pm1}$$${pm25}$$${pm10}$$${aqi}\n" 
        
        # Wysyłanie danych przez UART1
        uart1.write(encoded_data + "\n")
        print(f"Sent data: {encoded_data}")
    except Exception as e:
        print("Error reading data:", e)

# Inicjalizacja timera do odczytu co 6 minut (360000 ms)
timer = Timer(1)
timer.init(period=360000, mode=Timer.PERIODIC, callback=send_pm_data)
