import paho.mqtt.client as mqtt
import ssl
import time

rootca = r'D:\Projects\aws-iot\certs\AmazonRootCA1.pem.txt'
certificate = r'D:\Projects\aws-iot\certs\afbafc2d9f-certificate.pem.crt'
keyfile = r'D:\Projects\aws-iot\certs\afbafc2d9f-private.pem.key'

c = mqtt.Client()
c.tls_set(rootca, certfile=certificate, keyfile=keyfile, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
c.connect('a4313d1203j11-ats.iot.us-east-1.amazonaws.com',8883)

def onc(c, userdata, flags, rc):
    print("connected to aws rc", rc)
    c.subscribe("mytopic/iot")

def onm(c, userdata, msg):
    m = msg.payload.decode()
    # while True:
    #     if len(result)==1:
    #         c.publish('mytopic/iot', result["temp"])
    #         time.sleep(1)
    if m == "hello":
        c.publish('mytopic/iot', "hello from python")
        

c.on_connect = onc
c.on_message = onm
c.loop_forever()

# "D:\Projects\aws-iot\certs\afbafc2d9f-certificate.pem.crt"
# "D:\Projects\aws-iot\certs\afbafc2d9f-private.pem.key"
# "D:\Projects\aws-iot\certs\afbafc2d9f-public.pem.key"
# "D:\Projects\aws-iot\certs\AmazonRootCA1.pem.txt"