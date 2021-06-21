#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2021 MarsLink <marslink@126.com>

# This shows an example of an MQTT client that upload xiaomi temperature/humidity/battery into MarsLink cloud platform.

import sys
import getopt
import time
#import context  # Ensures paho is in PYTHONPATH
import paho.mqtt.client as mqtt
import xiaomi_ble_device as xm_ble
from xiaomi_ble_device import Measure

final_mid = 0
#Take for xiaomi LYWSD03MMC for example
ble_device_mac = "A4:C1:38:6C:EF:9B"

def on_connect(mqttc, userdata, flags, rc):
    if userdata == True:
        print("rc: " + str(rc))


def on_message(mqttc, userdata, msg):
    global final_mid
    if msg.retain == 0:
        pass
        # sys.exit()
    else:
        if userdata == True:
            print("Clearing topic " + msg.topic)
        (rc, final_mid) = mqttc.publish(msg.topic, None, 1, True)


def on_publish(mqttc, userdata, mid):
    global final_mid
    if mid == final_mid:
        pass
        # sys.exit()


def on_log(mqttc, userdata, level, string):
    print(string)


def print_usage():
    print(
        "mqtt_report_data.py [-d] [-h hostname] [-i clientid] [-k keepalive] [-p port] [-u username [-P password]] [-v]")

#get xiaomi themal data from ble device 
p = xm_ble.connect(ble_device_mac)
def get_temp_data():
    p.withDelegate(Measure("mijia"))
    p.waitForNotifications(2000)

def main(argv):
    debug = True
    host = ""
    client_id = None
    keepalive = 60
    port = 1883
    password = ""
    topic = None
    username = ""
    verbose = False

    try:
        opts, args = getopt.getopt(argv, "dh:i:k:p:P:t:u:v",
                                   ["debug", "id", "keepalive", "port", "password", "topic", "username", "verbose"])
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-d", "--debug"):
            debug = True
        elif opt in ("-h", "--host"):
            host = arg
        elif opt in ("-i", "--id"):
            client_id = arg
        elif opt in ("-k", "--keepalive"):
            keepalive = int(arg)
        elif opt in ("-p", "--port"):
            port = int(arg)
        elif opt in ("-P", "--password"):
            password = arg
        elif opt in ("-t", "--topic"):
            topic = arg
            print(topic)
        elif opt in ("-u", "--username"):
            username = arg
        elif opt in ("-v", "--verbose"):
            verbose = True

    if topic == None:
        print("You must provide a topic to clear.\n")
        print_usage()
        sys.exit(2)

    
    mqttc = mqtt.Client(client_id)
    mqttc._userdata = verbose
    mqttc.on_message = on_message
    mqttc.on_publish = on_publish
    mqttc.on_connect = on_connect
    if debug:
        mqttc.on_log = on_log

    if username:
        mqttc.username_pw_set(username, password)

    #Connect to MQTT server or broker.
    mqttc.connect(host, port, keepalive)
    # time.sleep(5)
    mqttc.subscribe(topic)

    mqttc.loop_start()

    for x in range (0, 100):
        get_temp_data()
        res = xm_ble.getresult()

        msgs = '{"deviceId": "LYWSD03MMC","properties": {"temperature":"' + str(res[0]) + '","humidity":"' + str(res[1]) + '","battery":"' + str(res[3]) + '"}}'
        print(msgs)
        infot = mqttc.publish("/report-property", str(msgs))
        infot.wait_for_publish()

        time.sleep(2)

    mqttc.disconnect()
if __name__ == "__main__":
    main(sys.argv[1:])

