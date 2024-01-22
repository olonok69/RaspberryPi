#!/usr/bin/env python

import time
import datetime
from dotenv import dotenv_values
from smbus2 import SMBus
from azure.iot.device import IoTHubDeviceClient, Message
from bme280 import BME280 

print(
    """all-values.py - Read temperature, pressure, and humidity

Press Ctrl+C to exit!

"""
)
config = dotenv_values(".env")
CONNECTION_STRING = config.get('cn')

# Initialise the BME280
bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)

MSG_SND = '{{"timestr": {timestr},"pressure": {pressure},"temperature": {temperature},"humidity": {humidity}}}'  
def iothub_client_init():  
        client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)  
        return client 
def iothub_client_telemetry_sample_run():  
    try:  
        client = iothub_client_init()  
        print ( "Sending data to IoT Hub, press Ctrl-C to exit" )
        while True:
            temperature = bme280.get_temperature()
            pressure = bme280.get_pressure()
            humidity = bme280.get_humidity()
            time1 = datetime.datetime.now()
            timestr = time1.strftime("%m/%d/%Y %H:%M:%S")
            msg_txt_formatted = MSG_SND.format(timestr=timestr,pressure=pressure,
                                               temperature=temperature, humidity=humidity)
            message = Message(msg_txt_formatted) 
            #print(f"Time {timestr}:  {temperature:05.4f}C {pressure:05.4f}hPa {humidity:05.4f}%")
            print( "Sending message: {}".format(message) )  
            client.send_message(message)  
            print ( "Message successfully sent" ) 
            time.sleep(1)
    except KeyboardInterrupt:  
        print ( "IoTHubClient stopped" )  

if __name__ == '__main__':
    print ( "Press Ctrl-C to exit" )  
    iothub_client_telemetry_sample_run()