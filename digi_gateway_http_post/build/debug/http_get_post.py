############################################################################
#                                                                          #
# Copyright (c)2009, Digi International (Digi). All Rights Reserved.       #
#                                                                          #
# Permission to use, copy, modify, and distribute this software and its    #
# documentation, without fee and without a signed licensing agreement, is  #
# hereby granted, provided that the software is used on Digi products only #
# and that the software contain this copyright notice,  and the following  #
# two paragraphs appear in all copies, modifications, and distributions as #
# well. Contact Product Management, Digi International, Inc., 11001 Bren   #
# Road East, Minnetonka, MN, +1 952-912-3444, for commercial licensing     #
# opportunities for non-Digi products.                                     #
#                                                                          #
# DIGI SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED   #
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A          #
# PARTICULAR PURPOSE. THE SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF ANY, #
# PROVIDED HEREUNDER IS PROVIDED "AS IS" AND WITHOUT WARRANTY OF ANY KIND. #
# DIGI HAS NO OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT, UPDATES,         #
# ENHANCEMENTS, OR MODIFICATIONS.                                          #
#                                                                          #
# IN NO EVENT SHALL DIGI BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT,      #
# SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS,   #
# ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF   #
# DIGI HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.                #
#                                                                          #
############################################################################

"""\
    XBee Non-Blocking Echo demo for Digi devices
    
    This example gives a simple demonstration of how to set and use ZigBee 
    sockets configured for non-blocking I/O with select. This application echos
    packets back to the originator.

    The socket is marked for reading only if the payload buffer is empty; if 
    the buffer is non-empty then the socket is marked for writing. Select is 
    used to arbitrate when a socket is ready to be read or written.

    This example could be easily extended to operate on multiple sockets.
    
"""

import sys, os 
import xbee
from socket import *
from select import *
import urllib
import urllib2
import json
import ssl

def parse_data(data_str):
    # Slownik dla przetworzonych danych
    data = {}

    # Sprawdzamy, czy dane zawieraja separator '@@@' (czujnik SHT35)
    if '@@@' in data_str:
        parts = data_str.split('@@@')
        if len(parts) == 2:
            try:
                # Parsujemy dane i zaokraglamy do 2 miejsc po przecinku
                humidity = round(float(parts[0]), 2)
                temperature = round(float(parts[1]), 2)
                data['field1'] = temperature
                data['field2'] = humidity
                data['type'] = "CUSTOM"
            except ValueError:
                print("Blad: Niepoprawny format danych dla SHT35. Pomijam te dane.")
                return None  # Pomijamy dalsze przetwarzanie

    elif '###' in data_str:
        parts = data_str.split('###')
        if len(parts) == 3:
            try:
                data['field3'] = round(float(parts[0]), 2)
                data['field4'] = round(float(parts[1]), 2)
                data['field5'] = round(float(parts[2]), 2)
                data['type'] = "CUSTOM"
            except ValueError:
                print("Blad: Niepoprawny format danych dla BMP280. Pomijam te dane.")
                return None  # Pomijamy dalsze przetwarzanie

    elif '$' in data_str:
        parts = data_str.split('$$$')
        if len(parts) == 4:
            try:
                data['field1'] = round(float(parts[0]), 2)
                data['field2'] = round(float(parts[1]), 2)
                data['field3'] = round(float(parts[2]), 2)
                data['field4'] = round(float(parts[3]), 2)
                data['type'] = "AQI"
            except ValueError:
                print("Blad: Niepoprawny format danych dla PMS7003. Pomijam te dane.")
                return None  # Pomijamy dalsze przetwarzanie

    else:
        print("Blad: Nieznany separator w danych. Pomijam te dane.")
        return None  # Pomijamy dalsze przetwarzanie

    print(data)
    return data
    

def send_data_to_thingspeak(data, api_key):
    # Walidacja parametrow
    if data is None or not isinstance(data, dict):
        print("Blad: Niepoprawne dane do wyslania.")
        return  # Pomijamy wysylanie danych

    # URL do Thingspeak z uzyciem metody format
    url = 'https://api.thingspeak.com/update?api_key={}'.format(api_key)

    # Budowanie danych query string na podstawie przekazanego slownika
    query_string = '&'.join(['{}={}'.format(field, value) for field, value in data.items()])
    full_url = '{}&{}'.format(url, query_string)

    # Utworzenie zadania HTTP GET do Thingspeak
    context = ssl._create_unverified_context()
    request = urllib2.Request(full_url)

    try:
        response = urllib2.urlopen(request, context=context)
        print("Odpowiedz:", response.read())
    except urllib2.HTTPError as e:
        print("Blad HTTP:", e.code)
    except urllib2.URLError as e:
        print("Blad URL:", e.reason)

#########################################MAIN#####################################################
api_key_XBEE_CUSTOM = 'PT4AFHEC82ZNCINW'
api_key_XBEE_AQI = 'KLBB23ZQL1LHGC29'

# Create the socket, datagram mode, proprietary transport:
sd = socket(AF_XBEE, SOCK_DGRAM, XBS_PROT_TRANSPORT)
# Bind to endpoint 0xe8 (232):
sd.bind(("", 0xe8, 0, 0))
# Configure the socket for non-blocking operation:
sd.setblocking(0)
while 1:
    try:
        # Initialize state variables:
        payload = ""
        src_addr = ()
    
        # Forever:
        while 1:
            # Reset the ready lists:
            rlist, wlist = ([], [])
            if len(payload) == 0:
                # If the payload buffer is empty,
                # add socket to read list:
                rlist = [sd]
            else:
                # Otherwise, add the socket to the
                # write list:
                wlist = [sd]
        
            # Block on select:
            rlist, wlist, xlist = select(rlist, wlist, [])
        
            # Is the socket readable?
            if sd in rlist:
                # Receive from the socket:
                payload, src_addr = sd.recvfrom(8192)
                print(payload)
                if payload != "AWAKE":
                    data = parse_data(payload)
                    if data != None and data['type']=="CUSTOM":
                        send_data_to_thingspeak(data, api_key_XBEE_CUSTOM)
                    elif data != None and data['type']=="AQI":
                        send_data_to_thingspeak(data, api_key_XBEE_AQI)                  
                # If the packet was "quit", then quit:
                if payload == "quit":
                    raise Exception, "Quit received"
            # Is the socket writable?
            if sd in wlist:
                # Send to the socket:
                count = sd.sendto(payload, 0, src_addr)
                # Slice off count bytes from the buffer,
                # useful for if this was a partial write:
                payload = payload[count:]
    
    except Exception, e:
        raise Exception, e
        # upon an exception, close the socket:
        sd.close()


