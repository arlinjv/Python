import paho.mqtt.client as mqtt
import time

mqttpublisher = mqtt.Client()
mqttpublisher.connect("localhost", 1883, 60)
mqttpublisher.publish("Hello/World", "Starting Stream")

rc = 0
while rc == 0:
    rc = mqttpublisher.loop()
    message = "Message @" + str(time.ctime())
    mqttpublisher.publish("Hello/World", message)
    time.sleep(1)

