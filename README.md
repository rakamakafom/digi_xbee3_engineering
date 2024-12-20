# digi_xbee3_engineering
Scripts prepared as part of a engineering thesis: "ZigBee standard in IoT end device communication"
Author: Damian Sarna, 20.12.2024
Version 1.0
Repository contains micropython scripts using for read data from sensor BME280, SHT35 and PMS7003 connected to XBEE 3. XBEE module was configured in Zigbee network, there was used as DIGI gateway(main cordinator). In case SHT35 and BME280 data was collected by I2C protocol directly by XBEE module using micropython, then wireless transmission to the coordinator(module also had a role gateway)
In case PMS7003 data was collected with the help of ESP32 (PMS7003 using UART protocol), than ESP32 transmitted by UART2 to the XBEE module connected in the mesh network ZigBee. Data was sending to the cloud by gateway DIGI(http, urlib library) and collected on the https://thingspeak.mathworks.com
Prepared as part of a diploma thesis: "ZigBee standard in IoT end device communication"
Used libraries:
BME280:  https://github.com/robert-hh/BME280
SHT35:   https://github.com/dvsu/Sensirion-SHT3X-MicroPython/tree/main
PMS7003: https://github.com/pkucmus/micropython-pms7003
