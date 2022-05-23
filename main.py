# Libs for Unix time
from datetime import datetime
import calendar

# Libs for "Serial"
import os

# Libs for GPIO
from gpiozero import Button

# Libs for OpenCV
import cv2
import numpy as np

# Libs for BT
import bt

# Setup for Unix Time
def unix():
	d = datetime.utcnow()
	return calendar.timegm(d.utctimetuple())

# Setup for "Serial"
def send(data):
    os.system("echo '" + str(data) + "\\n' >> /dev/ttyS0")

# Setup for GPIO
#button = Button(26)
sensor = Button(19)

# Setup for OpenCV

W = 320
H = 240

IMAGE_FLIP_VERTICALLY = False
IMAGE_FLIP_HORIZONTALLY = False
IMAGE_RESIZE = True

cap = cv2.VideoCapture(-1)

if (IMAGE_RESIZE):
    cap.set(3, int(W))
    cap.set(4, int(H))

#RED
low_acorn = np.array([161, 155, 84])
high_acorn = np.array([179, 255, 255])

W = cap.get(3)
H = cap.get(4)

acorn = False
acornX = 0
acornY = 0
acornSize = 0
acornDist = 0
gap = 2.5
minacornSize = 150

debugging = False

# Setup for BT
bt = bt.BT()

### SERVER ONLY CODE ###
#while (1):
#	if not button.is_pressed:
#		break
#bt.start()

bt.sync()

# Setup base things
import time

send(10)
time.sleep(3)

start = unix()
duration = 60

# Main Loop

while True:
	# Read image from the camera
	ret, frame = cap.read()
    
	if not ret:
		print("ERROR: CAN NOT READ IMAGE FROM THE CAMERA")
		exit()
		
	# Exit in case of overtime
	if (unix() - start > duration):
		break;
		
	# Detect objects and avoid hitting them
	if not sensor.is_pressed:
		send(30)
		time.sleep(5)
		
	# Flip the image
	if (IMAGE_FLIP_VERTICALLY):
		frame = cv2.flip(frame, 0)
	if (IMAGE_FLIP_HORIZONTALLY):
		frame = cv2.flip(frame, 1)
        
	#Create masks and find the objects
        
	hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	acorn_mask = cv2.inRange(hsv_frame, low_acorn, high_acorn)
	acorn_contours, _ = cv2.findContours(acorn_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	acorn_contours = sorted(acorn_contours, key=lambda x:cv2.contourArea(x), reverse=True)
   
	acornX = W / 2
	acornY = H / 2
	acornSize = 0
	acornDist = 0
	acorn = False
    
	for cnt in acorn_contours:
		(x, y, w, h) = cv2.boundingRect(cnt)
        
		acornX = int((x + x + w) / 2)
		acornY = int((y + y + h) / 2)
		acornSize = int((w + h) / 2)
		acornDist = int(-acornSize + w)
		acorn = True
		break
    
	key = cv2.waitKey(1)
    
	# Exit, if needed
    
	if key == 27:
		break
    
	if (acorn and acornSize > minacornSize):
		break
	else:
		send(3)
    
send(0)
send(20)

cap.release()
cv2.destroyAllWindows()
