#Libraries
import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
import ssl

#Certificates
rootca = r'/home/pi/certs/AmazonRootCA1.pem.txt'
certificate = r'/home/pi/certs/afbafc2d9f-certificate.pem.crt'
keyfile = r'/home/pi/certs/afbafc2d9f-private.pem.key'

#Authenticate and connect
c = mqtt.Client()
c.tls_set(rootca, certfile=certificate, keyfile=keyfile, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
c.connect('a4313d1203j11-ats.iot.us-east-1.amazonaws.com',8883, 60)

#On message and on connect
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

c.loop_start()   

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
 
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
if __name__ == '__main__':
    try:
        while True: # && connflag == True:
            if connflag == True:
                dist = distance()
                c.publish("temperature", dist, qos=1) 
                print ("Measured Distance = %.1f cm" % dist)
                time.sleep(1)
            else:
                print("waiting for connection...") 
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()