# -*- coding: utf-8 -*-
"""
Title: PiAutoStage: An Open-Source 3D Printed Tool for the Automatic 
                    Collection of High-Resolution Microscope Imagery. 

Authors: R. Alex Steiner and Tyrone.O. Rooney

Updated by SWM for picamera2

Publications DOI: 
    
PiAutoStage Image Capture Code

"""

import serial, time, os
import picamera2 as picamera
from fractions import Fraction
from picamera2 import Preview

##############################################################################
################################ USER INPUTS #################################
##############################################################################

## HOME POSITION ##
x_home = 1500
y_home = 1800

## NUMBER OF STEPS ALONG AXES ##
num_x = 19
num_y = 15

## STAGE LIMITS ##
x_ini = 1000
x_max = 1950

y_ini = 1500
y_max = 2150
## FOCUS POSITION ##
focus_pos = '15001900'
## four photo parameter positions ##
a = '13001850' 
b = '12002000'
c = '18002000' 
d = '18001700' 

#### Set the ISO Value ####
# isx = 50

####  Set Image Capture Resolution ####
res = (2028,1550)

## USE THESE SETTINGS TO ALLOW THE CAMERA TO AUTOMATICALLY SET PHOTO PARAMETERS ##
gx = 0
qx = 0

## OPTIONAL INPUT TO MANUALLY SET PHOTO PARAMETERS ##
## These are values that you can use to control the camera ##
#gx = (Fraction(263, 128), Fraction(705, 256))
#qx = int(20694)

## STARTING FILE NAME. RESULTANT IMAGES WILL HAVE FILENAME 1000.JPG ##
## FILE NAMES WILL COUNT UP UNTIL IMAGE SEQUNECE IS COMPLETE ##
count = 1000

##############################################################################
############################ END OF USER INPUTS ##############################
##############################################################################




##############################################################################
################## SEM DEFINED FUNCTIONS FOR PICAM2 ##########################
##############################################################################

def initialize_arduino():
    ####  Initialize Serial Port and Baude Rate  ####
    ser = serial.Serial('/dev/ttyACM0', 9600)
    print('\n\nSerial port intilized: 5 second delay for Arduino\n')
    #### Gives the Arduino time to intitialize ####
    time.sleep(4)
    #### sends the GoCode to attach the Arduino Pins to the Servos ####
    go = '55551500'
    ser.write(go.encode())
    time.sleep(1)

    print('Arduino Ready for Instructions\n')
    time.sleep(1)

    return ser


def create_photo_param_file():
    ## Creates a text file that photo parameters and image locations will be writen to ##
    otp = open(os.path.join("photo parameters.txt"), "w")
    otp.write("Number of columns/X steps: " + str(num_x+1)+ "\n")
    otp.write("Number of rows/Y steps: " + str(num_y+1)+ "\n")
    otp.write("Total number of photos: " + str((num_x+1)*(num_y+1))+ "\n")


    print("Number of columns/X steps: " + str(num_x+1)+ "\n")
    time.sleep(1)
    print("Number of rows/Y steps: " + str(num_y+1)+ "\n")
    time.sleep(1)
    print("Total number of photos: " + str((num_x+1)*(num_y+1))+ "\n")
    time.sleep(1)
    return otp


def get_camera():
    _camera = picamera.Picamera2()
    return _camera


def initialize_camera_preview(camera):
    camera_config = camera.create_preview_configuration()
    camera.configure(camera_config)

def start_camera_preview(camera):
    camera.start_preview(Preview.QTGL)
    camera.start()

def stop_camera_preview(camera):
    camera.stop_preview()

def get_exposure_time(camera):
    metadata = camera.capture_metadata()
    return metadata["ExposureTime"]

def get_colourgains(camera):
    metadata = camera.capture_metadata()
    return metadata["ColourGains"]

def setup_with_preview(camera, pausetime=2):
    start_camera_preview(camera)
    time.sleep(pausetime)
    _q = get_exposure_time(camera)
    _g = get_colourgains(camera)
    stop_camera_preview(camera)
    return _q, _g

def initialize_camera_still_capture(camera, exposure_time, colour_gains):
    capture_config = camera.create_still_configuration()
    camera.configure(capture_config)
    camera.set_controls({"ExposureTime": exposure_time,
                         "ColourGains": colour_gains,
                         "AeEnable": False,
                         "AwbEnable": False})
    camera.options["quality"] = 95

def capture_image(camera, filename):
    camera.capture_file(filename, format='jpeg')


##############################################################################
####################### START RUNNING IMAGE CAPTURE ##########################
##############################################################################

ser = initialize_arduino()

## NUMBER OF STEPS AND STEP SIZE CALCUALTED ##

gridX = num_x + 1
gridY = num_y + 1

x_step = abs(int((x_max - x_ini) / num_x))
y_step = abs(int((y_max - y_ini) / num_y))

i = 0

otp = create_photo_param_file()

######## FOCUS AND IMAGE PARAMETER SEQUENCE STARTS HERE ########

print('Beginning focus and image parameter sequence. \n')
print('Moving to focus position at: ' + focus_pos + "\n")
ser.write(focus_pos.encode())


camera = get_camera()
initialize_camera_preview(camera)

q1, g = setup_with_preview(camera, 15)


# with picamera.PiCamera() as camera:
#             camera.resolution = res
#             camera.iso = isx
#             camera.start_preview()
#             time.sleep(15)
#             q1 = camera.exposure_speed
#             g = camera.awb_gains
#             camera.stop_preview()

print("Focus exposure speed: " + str(q1) + "\n")
print("Focus AWB gains: " + str(g)+ "\n")
otp.write("Focus exposure speed: " + str(q1) + "\n")
otp.write("Focus AWB gains: " + str(g)+ "\n")

ser.write(a.encode())
time.sleep(1)

q2, g1 = setup_with_preview(camera, 2)

# with picamera.PiCamera() as camera:
#             camera.resolution = res
#             print("Photo Resolution: " + str(camera.resolution)+ "\n")
#             camera.iso = isx
#             camera.start_preview()
#             time.sleep(2)
#             q2 = camera.exposure_speed
#             g1 = camera.awb_gains
#             camera.stop_preview()

print("Position 'a' exposure speed: " + str(q2)+ "\n")
print("Position 'a' AWB gains: " + str(g1)+ "\n")
otp.write("Position 'a' exposure speed: " + str(q2)+ "\n")
otp.write("Position 'a' AWB gains: " + str(g1)+ "\n")

ser.write(b.encode())
time.sleep(1)

q3, g2 = setup_with_preview(camera, 2)


# with picamera.PiCamera() as camera:
#             camera.resolution = res
#             camera.iso = isx
#             camera.start_preview()
#             time.sleep(2)
#             q3 = camera.exposure_speed
#             g2 = camera.awb_gains
#             camera.stop_preview()
            
print("Position 'b' exposure speed: " + str(q3)+ "\n")
print("Position 'b' AWB gains: " + str(g2)+ "\n")
otp.write("Position 'b' exposure speed: " + str(q3)+ "\n")
otp.write("Position 'b' AWB gains: " + str(g2)+ "\n")

ser.write(c.encode())
time.sleep(1)

q4, g3 = setup_with_preview(camera, 2)


# with picamera.PiCamera() as camera:
#             camera.resolution = res
#             camera.iso = isx
#             camera.start_preview()
#             time.sleep(2)
#             q4 = camera.exposure_speed
#             g3 = camera.awb_gains
#             camera.stop_preview()
print("Position 'c' exposure speed: " + str(q4)+ "\n")
print("Position 'c' AWB gains: " + str(g3)+ "\n")
otp.write("Position 'c' exposure speed: " + str(q4)+ "\n")
otp.write("Position 'c' AWB gains: " + str(g3)+ "\n")

ser.write(d.encode())
time.sleep(1)

q5, g4 = setup_with_preview(camera, 2)


# with picamera.PiCamera() as camera:
#             camera.resolution = res
#             camera.iso = isx
#             camera.start_preview()
#             time.sleep(2)
#             q5 = camera.exposure_speed
#             g4 = camera.awb_gains
#             camera.stop_preview()

print("Position 'd' exposure speed: " + str(q5)+ "\n")
print("Position 'd' AWB gains: " + str(g4)+ "\n")
otp.write("Position 'd' exposure speed: " + str(q5)+ "\n")
otp.write("Position 'd' AWB gains: " + str(g4)+ "\n")

qout = [q1, q2, q3, q4, q5]

qfloat = (q1+q2+q3+q4+q5)/5

q=min(qout)

print(qout)
print(q)
otp.write("Min exposure speed set: " + str(q)+ "\n")
otp.write("Camera ISO value set: " + str(isx) + "\n")
print("Min exposure speed set: " + str(q)+ "\n")
print("Camera ISO value set: " + str(isx) + "\n")


###### IMAGE CAPTURE PARAMETERS ARE AUTOMATICALLY SET HERE ######

if qx == 0:
    q = q
else:
    q = qx
    otp.write("WARNING! CAMERA SETTINGS OVERRIDE, exposure set to " + str(q)+ "\n")

if gx == 0:
    g = g
else:
    g = gx
    otp.write("WARNING! CAMERA SETTINGS OVERRIDE, gains set to " + str(g)+ "\n")


###### IMAGE CAPTURE SEQUENCE STARTS HERE #####


print('\nBegin Photo Acquision \nNumber of photos being collected: '+ str((num_x+1)*(num_y+1)))
x1 = str(x_ini)
x = x_ini
time.sleep(0.5)

while i <= num_x:
    print('\nImaging column: ' + str(i+1) + ' of ' + str(num_x+1))
    y = y_max
    j = 0
    #### The following 7 lines bring the carraige beyong the area being imaged. ####
    #### This allows for the stage to compensate for the limited slip in gears  ####
    #### depending on the print quality (degree of slip) and the limits of the  ####
    #### user's stage, the y1 value may need to be changed                      #### 
    if x < 1000:
        x1 = '0' + str(x)
    else:
        x1 = str(x)
    y1 = '1700'
    coord1 = x1 + y1
    ser.write(coord1.encode())
    
    #### This loop steps carraige along the column, capturing images            ####
    while j <= num_y:
        time.sleep(0.5)
        if x < 1000:
            x1 = '0' + str(x)
        else:
            x1 = str(x)
        if y < 1000:
            y1 = '0' + str(y)
        else:
            y1 = str(y)
        coord1 = x1 + y1
        #print(coord1)
        otp.write("Location of picture " + str(count) + " is at X= " + str(x1) + " and Y= " + str(y1)+ "\n")
        ser.write(coord1.encode())

        initialize_camera_still_capture(camera, q, g)

        time.sleep(1)
        filename = str(count) + '.jpg'
        capture_image(camera, filename)
        count = count + 1


        # with picamera.PiCamera() as camera:
        #     camera.iso = isx
        #     camera.resolution = res
        #     time.sleep(1)
        #     camera.shutter_speed = q
        #     camera.exposure_mode = 'off'
        #     camera.awb_mode = 'off'
        #     camera.awb_gains = g
        #     filename = str(count) + '.jpg'
        #     camera.capture(filename)
        #     count = count + 1

        y = y - y_step
        j = j + 1
    
    
    x = x + x_step
    i = i + 1


a = x_home
b = y_home

if a < 1000:
    a1 = '0' + str(a)
else:
    a1 = str(a)
if b < 1000:
    b1 = '0' + str(b)
else:
    b1 = str(b)
coord = a1 + b1
print(coord)
ser.write(coord.encode())

otp.close()

ser.close()

