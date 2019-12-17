import paho.mqtt.client as mqtt
import ssl
import time
from time import sleep
from random import uniform

rootca = r'D:\Projects\aws-iot\certs\AmazonRootCA1.pem.txt'
certificate = r'D:\Projects\aws-iot\certs\afbafc2d9f-certificate.pem.crt'
keyfile = r'D:\Projects\aws-iot\certs\afbafc2d9f-private.pem.key'

c = mqtt.Client()
c.tls_set(rootca, certfile=certificate, keyfile=keyfile, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
c.connect('a4313d1203j11-ats.iot.us-east-1.amazonaws.com',8883, keepalive=60)

connflag = False
def onc(c, userdata, flags, rc):
    global connflag
    print("connected to aws rc", rc)
    connflag = True
    c.subscribe("mytopic/iot")

def onm(c, userdata, msg):
    m = msg.payload.decode()
    print(m)
        

c.on_connect = onc
c.on_message = onm

c.loop_start()                                          # Start the loop
 
while True:
    sleep(5)
    if connflag == True:
        tempreading = uniform(20.0,25.0)                        # Generating Temperature Readings 
        c.publish("temperature", tempreading, qos=1)        # topic: temperature # Publishing Temperature values
        print("msg sent: temperature " + "%.2f" % tempreading ) # Print sent temperature msg on console
    else:
        print("waiting for connection...")   
