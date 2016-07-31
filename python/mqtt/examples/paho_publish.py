# -*- coding: utf-8 -*- 
import paho.mqtt.client as paho
import time
import random
 
def on_publish(client, userdata, mid):
    print("mid: "+str(mid))
 
def fake_thermometer():
    fake_thermometer.val += random.gauss(0,1)
    return fake_thermometer.val
fake_thermometer.val = 20

client = paho.Client()
client.on_publish = on_publish
client.connect("localhost", 1883)
client.loop_start()
 
while True:
    temperature = fake_thermometer()
    topic = "test/temperature"
    (rc, mid) = client.publish("test/temperature", str(temperature), qos=1) #return code, message id = 
    print temperature
    time.sleep(5)
