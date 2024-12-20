
  o---------------------------o
  | HTTP Get and POST Example |
  o---------------------------o

  Compatible platforms
  --------------------
  * Connect WAN 3G IA
  * ConnectCore 3G 9P 9215
  * ConnectPort WAN GPS
  * ConnectPort WAN VPN
  * ConnectPort WAN Wi
  * ConnectPort X2
  * ConnectPort X2 SE
  * ConnectPort X2B
  * ConnectPort X2D
  * ConnectPort X2e Wi-Fi ZB
  * ConnectPort X2e ZB
  * ConnectPort X2e ZB EVDO Verizon
  * ConnectPort X2e ZB HSPA
  * ConnectPort X2e ZB UMTS
  * ConnectPort X2e ZB Wi-Fi
  * ConnectPort X4
  * ConnectPort X4 4G
  * ConnectPort X4 H
  * ConnectPort X4 IA
  * ConnectPort X4 NEMA
  * ConnectPort X5
  * ConnectPort X5 F
  * ConnectPort X5 F ZB GPRS
  * ConnectPort X5 F ZB Wifi GPRS
  * ConnectPort X5 R
  * ConnectPort X5 R Wifi GPRS Iridium
  * ConnectPort X5 R ZB GPRS
  * ConnectPort X5 R ZB Wifi CDMA
  * ConnectPort X5 R ZB Wifi GPRS
  * ConnectPort X8
  * Digi Connect SP Python
  * Digi Connect Wi-SP 16M Python
  * Embedded Gateway
  * TransPort WR21
  * TransPort WR41
  * TransPort WR41v2
  * TransPort WR44
  * TransPort WR44RR
  * TransPort WR44v2
  * XBee Gateway
  * XBee Gateway EVDO Sprint
  * XBee Gateway EVDO Verizon
  * XBee Gateway HSPA
  * XBee Gateway UMTS
  * XBee Gateway Wi-Fi (current)

  Introduction
  ------------
  This application exposes an example of the HTTP POST and GET submit methods. 
  It performs a search of a text in the Yahoo portal.

  Requirements
  ------------
  To run this example you will need:
    * One Digi Python compatible device to host the application.
    
  This example requires the Connection Mode = Local Area Network/USB/Serial 
  under the Device Manager’s General Tab.

  Example setup
  -------------
  1) Make sure the hardware is set up correctly:
       a) The Digi device is powered on.
       b) The Digi device is connected directly to the PC or to the Local 
          Area Network (LAN) by the Ethernet cable. In case the device does 
          not have Ethernet interface, make sure it is connected directly to 
          the PC by the corresponding USB or serial cable.
     
  2) This demo requires the Digi device to have Internet access and a DNS 
     server configured in order to resolve the domain name used in the 
     example. If your device does not have the DNS server configured follow 
     these steps:
     
     For ConnectPort X series devices:
       a) Open an Internet browser and type the IP Address of your device.
       b) Go to the Network option in the left menu.
       c) Select the Advanced Network setting option at bottom.
       d) Fill the Static Primary DNS setting with the following Google DNS 
          server and Apply the changes:
          
            * 8.8.8.8
     
     For TransPort series devices:
       a) Open an Internet browser and type the IP Address of your device.
       b) Enter your user name and password to log in the device.
       b) Go to the Network option in the left menu.
       c) Select the "Ethernet" setting and choose "ETH 0".
       d) Fill the DNS Server setting with the following Google DNS server 
          and Apply the changes:
          
            * 8.8.8.8

  Running the example
  -------------------
  The example is already configured, so all you need to do is to build and 
  launch the project.
  
  While it is running, you will be prompted for a text to search in Yahoo. 
  Type any word or text you want to look for. Then, it will ask for the 
  submit method to use, GET or POST. Type any of them to perform a search in 
  Yahoo of the text you provided previously.
  
  Depending on the submit method selected, you will see the URL requested 
  changes: 
  
    * GET method: http://search.yahoo.com/search?p=[text]
       - The search text is included in the URL.
  
    * POST method: http://search.yahoo.com/search
       - The search text is not included in the URL.
  
  When the search finishes, the example will display the number of results 
  found for your text.

  Tested On
  ---------
  ConnectPort X2e ZB
  ConnectPort X4
  TransPort WR21
  TransPort WR44
  XBee Gateway

