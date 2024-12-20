#----------------------------------------------------------------
#Author: Damian Sarna, 20.12.2024
#Script using for read data from sensor BME280 connected to XBEE 3
#Prepared as part of a diploma thesis: "ZigBee standard in IoT end device communication"
#Script use library: https://github.com/robert-hh/BME280
#----------------------------------------------------------------
import sys
import sys
from binascii import hexlify
import bme280_float as bme280
from machine import I2C
import xbee
import time

# Constants
BME280_ADDR = 0x76

print(" +--------------------------------+")
print(" | XBee MicroPython I2C BME280 |")
print(" +---------------------------------\n")

# Instantiate an I2C peripheral.
i2c = I2C(1)

if BME280_ADDR not in i2c.scan():
    print("Could not find the sensor!")
    sys.exit(1)

bme = bme280.BME280(i2c=i2c)

# Constants
SLEEP_TIME_MS = 600000  # 10 minutes
AWAKE_TIME_MS = 10000  # 10 seconds.

MSG_ON = "ON"
MSG_OFF = "OFF"
MSG_SEPARATOR = "###"
MSG_AWAKE = "AWAKE"

PROTOCOL_ZB = "Zigbee"
PROTOCOL_DM = "DigiMesh"
PROTOCOL_802 = "802.15.4"

DEST_NODE_ID = "GATEWAY_COORD"


def get_destination(xb_prot):
    if xb_prot == PROTOCOL_ZB:
        return xbee.ADDR_COORDINATOR

def get_protocol():
    version = xb.atcmd("VR")

    if version >= 0x3000:
        return PROTOCOL_DM

    if version >= 0x2000:
        return PROTOCOL_802

    return PROTOCOL_ZB

def find_gateway(retries=3):
    for i in range(1, retries + 1):
        print("Searching destination %s %d/%d" % (DEST_NODE_ID, i, retries))

        try:
            devices = xbee.discover()
        except OSError:
            devices = []

        for dev in devices:
            if dev.get('node_id', None) == DEST_NODE_ID:
                gateway = dev.get('sender_eui64', None)
                return gateway if gateway else dev.get('sender_nwk', None)
        time.sleep_ms(1500)

    return None

def transmit_data(dest, msg, retries=3):
    for i in range(1, retries + 1):
        try:
            xbee.transmit(dest, msg)
            break
        except OSError as e:
            print("Could not transmit data (%d/%d): %s" % (i, retries, str(e)))
def rx_callback(data):
    if not data or data['broadcast']:
        return

    if protocol == PROTOCOL_ZB and data['sender_nwk'] != 0:
        return

    if protocol == PROTOCOL_DM and data['sender_eui64'] != destination:
        return

    if protocol == PROTOCOL_802 and data['sender_eui64'] != destination:
        return

    try:
        payload = int(data.get('payload', bytearray()).decode())
    except ValueError:
        return

    if payload < 0:
        return

    # Update the sleep time.
    global sleep_time
    sleep_time = payload * 1000
    print("Temperature/humidity service stopped.\n" if not sleep_time
          else "Changed sleep time to %d s.\n" % payload)


# Instantiate the XBee device.
xb = xbee.XBee()

sleep_time = SLEEP_TIME_MS
print("Ip i2c")
print(i2c.scan())
protocol = get_protocol()
print("Current protocol: %s\n" % protocol)

destination = get_destination(protocol)
if not destination:
    print("Unable to find destination node: %s" % DEST_NODE_ID)
    sys.exit(1)
print("Destination %s\n" % hexlify(bytearray(destination)).decode().upper())
# Register the reception data callback.
xbee.receive_callback(rx_callback)

# Configure sleep mode to be managed by MicroPython.
xb.atcmd("SM",0x06)

# Start reading temperature and humidity measures.
while True:
    # Notify the gateway that the XBee is awake.
    transmit_data(destination, MSG_AWAKE)

    # Wait during the configured time for incoming messages.
    time.sleep(AWAKE_TIME_MS / 1000)

    # Check if temperature/humidity service is disabled.
    if not sleep_time:
        continue
    data =  bme.values
    print(data)
    # # Create the message to send with the temperature and humidity.
    temp_hum_msg = "{}{}{}{}{}".format(
        data[0],
        MSG_SEPARATOR,
        data[1],
		MSG_SEPARATOR,
        data[2]
    )

    # Send values to the gateway (coordinator).
    transmit_data(destination, temp_hum_msg)

    # Sleep for the configured timeout.
    xb.sleep_now(sleep_time)

