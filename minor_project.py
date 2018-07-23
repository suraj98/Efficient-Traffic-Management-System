import urllib
import cv2
import numpy as np
import time

# Replace the URL with your own IPwebcam shot.jpg IP:port
url='http://192.168.2.35:8080/shot.jpg'

while True:

    # Use urllib to get the image and convert into a cv2 usable format
    imgResp=urllib.urlopen(url)
    imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
    ref_img=cv2.imdecode(imgNp,-1)

    # put the image on screen
    cv2.imshow('IPWebcam',img)

    #To give the processor some less stress
    #time.sleep(0.1) 



def match_percent(path_ref, img,i):
    ref_img = cv2.imread(path_ref, 0)
    ref_img = cv2.resize(ref_img, (400,300))
    #cv2.imshow('resize_IPWebcam1',ref_img)
    ref_edges = cv2.Canny(ref_img, 100, 200)

    #img = cv2.imread(path_img, 0)
    img = cv2.resize(img, (400, 300))
    #cv2.imshow('resize_IPWebcam2',img)
    edges = cv2.Canny(img, 100, 200)

    #cv2.imwrite("IP1.jpg",img)   #To  CAlibrate
    #cv2.imwrite("IP2.jpg",ref_img) #To Calibrate
    
    height, width = ref_edges.shape
    print("ctr",i,"height",height,"width",width)
    whites = 0
    matches = 0

    for i in range(0, height):
        for j in range(0, width):
            if ref_edges[i, j] == 255:
                whites = whites + 1
            if (ref_edges[i, j] != 255) and edges[i, j] == 255:
                matches = matches + 1
           
    print("match",matches)
    print("whites",whites)
    a= (float(matches)/(float(matches)+float(whites)+50.0))
    print("a",a)
    a*=100.0
    match_percent = a
    print(match_percent)
    
    return match_percent 




import time
def operate_led():
    
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    
    def setupgpio(LED_RED, LED_AMBER, LED_GREEN):
        GPIO.setup(LED_RED, GPIO.OUT)
        GPIO.setup(LED_AMBER, GPIO.OUT)
        GPIO.setup(LED_GREEN, GPIO.OUT)
    
    def red (LED_RED, LED_AMBER, LED_GREEN):
            GPIO.output (LED_RED, LEDON)
            GPIO.output (LED_AMBER, LEDOFF)
            GPIO.output (LED_GREEN, LEDOFF)

    def amber (LED_RED, LED_AMBER, LED_GREEN):
        GPIO.output (LED_RED, LEDOFF)
        GPIO.output (LED_AMBER, LEDON)
        GPIO.output (LED_GREEN, LEDOFF)

    def green (LED_RED, LED_AMBER, LED_GREEN):
            GPIO.output (LED_RED, LEDOFF)
            GPIO.output (LED_AMBER, LEDOFF)
            GPIO.output (LED_GREEN, LEDON)
            
    def alloff (LED_RED, LED_AMBER, LED_GREEN, val):
            GPIO.output (LED_RED, LEDOFF)
            GPIO.output (LED_AMBER, LEDOFF)
            GPIO.output (LED_GREEN, LEDOFF)
            time.sleep(val)
    
    def basicSequence (val):
            red ()
            time.sleep(val)
            if turns[t_no] != 1:
                print(t_no)
                amber()
                time.sleep(1)
                green()
                time.sleep(5)
                turns[t_no] = 1
                lock.release()

    RED = [7, 15, 26, 40]
    AMBER = [5, 13, 24, 38]
    GREEN = [3, 11, 22, 36]
    
    LEDOFF = 0
    LEDON = 1

    setupgpio(RED[0],AMBER[0],GREEN[0])
    setupgpio(RED[1],AMBER[1],GREEN[1])
    setupgpio(RED[2],AMBER[2],GREEN[2])
    setupgpio(RED[3],AMBER[3],GREEN[3])
    for i in range(0,4):
        for j in range(0,4):
            for k in range(0,4):
                alloff(RED[i],AMBER[j],GREEN[k],0)
                red(RED[i],AMBER[j],GREEN[k])
    
    val = [0, 0, 0, 0]
    cam = cv2.VideoCapture(0)
    ret_val, img = cam.read()
    while True:
        for i in range(0,4):
            if i < 2:
                val[i] = match_percent('reference1.jpg', 'sample'+str(i+5)+'.jpg')
            else:
                val[i] = match_percent('reference2.jpg', 'sample'+str(i+5)+'.jpg')

        values = val[:]
        for j in range(0,4):
            cur = val.index(min(val))
            amber(RED[cur], AMBER[cur], GREEN[cur])
            time.sleep(1)
            green(RED[cur], AMBER[cur], GREEN[cur])
            time.sleep(4-j)
            val[cur] = 100
            amber(RED[cur], AMBER[cur], GREEN[cur])
            red(RED[cur], AMBER[cur], GREEN[cur])
        val = [0, 0, 0, 0]
        transmit_data(values)

def get_images():
    ''' '''

import http.client as httplib
import urllib
def transmit_data(values):
    #setup_modem()
    key = 'C2JR3L7ILWRZLHQL'
    params = urllib.parse.urlencode({'field1': values[0], 'field2': values[1],'field3': values[2],'field4': values[3],'field5': 12.93496,'field6': 79.14688,'key':key }) 
    headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = httplib.HTTPConnection("api.thingspeak.com:80")
    try:
        conn.request("POST", "/update", params, headers)
        response = conn.getresponse()
        print(response.status, response.reason)
        data = response.read()
        conn.close()
    except:
        print("Connection failed")

def receive_data():
    ''' '''

import serial
import os, time
def setup_modem():
    port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1) 
    port.flush()
    port.write(b'AT'+b'\r')
    rcv = port.readline()
    return rcv

#setup_modem()
import RPi.GPIO as GPIO
RED = [7, 15, 40, 26]
AMBER = [5, 13, 38, 24]
GREEN = [3, 11, 36, 22]
turns = [0, 0, 0, 0]
try:
    operate_led()
except KeyboardInterrupt:
    GPIO.cleanup()
