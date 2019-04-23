"""
   Copyright 2017 Charlie Liu and Bryan Zhou

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from tools import transfunction
from tools import screenres
import time
import cv2
import os
from picamera import PiCamera
from picamera.array import PiRGBArray
import time
from tools.captureProcessFrame import *
from tools.processWhitePoints import *
from tools.filterData import *
from tools.determineDataTrends import *
from tools.recordGesture import *
from tools.recordData import *
from pynput.keyboard import Key, Controller


# Image resolution of captured frames
IMG_SIZE = 608

# Size of the surrounding region utilized when appying a Gaussian blur on frames
BLUR_REGION = 5

# Cutoff for gray intensity value of pixels when thresholding frames
PIXEL_INTENSITY_THRESHOLD = 10

# Number of elements to analyze when calculating trends in x-axis and y-axis movement
DATA_WINDOW_SIZE = 10

# Cutoff values for data points when being filtered
LOWER_OUTLIER_CUTOFF = 25
UPPER_OUTLIER_CUTOFF = 150

# Cutoff values for calculated trends to compare with when detecting gestures
X_DATA_THRESHOLD = 0.5
Y_DATA_THRESHOLD = int(0.25 * IMG_SIZE)

# Define camera settings and specify variable to store frame
camera = PiCamera()
camera.resolution = (640, 480)
rgbFrame = PiRGBArray(camera, size = camera.resolution)

keyboard = Controller()

# Fetching data from the pipe
def getCommand():
  

  fileList = os.listdir("info")

  if len(fileList) == 0:

    return "none"


  fileList.sort()
  file = fileList[-1]
  fileName = file
  
  for file in fileList:

    os.remove("info/" + file)


  gesture = fileName
        
  return gesture

# Setting full-screen property and nullifying the infamous startup bug
cv2.waitKey(1000)
time.sleep(0.1)

# Running the actual process
while True:
  keyboard.press('x')
  keyboard.release('x')
  
  #put gestture detect in this file
  # Initialize data lists
  xData = []
  xDataSample = []
  xDataFiltered = []

  yData = []
  yDataSample = []
  yDataFiltered = []
  
    
  frame1 = captureProcessFrame(camera, rgbFrame, BLUR_REGION)

  frameCount = 0

  active = 1
  gestureDetected = None
  print ("waiting...")
  while gestureDetected == None:

    # Increment the frame count each iteration
    #frameCount += 1
    #show the windows
    #camera.capture(rgbFrame, format='bgr')
    

    frame2 = captureProcessFrame(camera, rgbFrame, BLUR_REGION)
    

    # Create an image based on the differences between the two frames and then enhance the result
    diffImg = cv2.absdiff(frame1, frame2)
    threshImg = cv2.threshold(diffImg, PIXEL_INTENSITY_THRESHOLD, 255, cv2.THRESH_BINARY)[1]
    
    whitePixelsData = processWhitePoints(threshImg)

    xData.append(whitePixelsData)

    # Assign frame 1 to frame 2 for the next iteration of comparison
    frame1 = frame2
        
    
    # Analyze for trends when a full window of data points has been gathered
    if len(xData) > 20:
      keyboard.press('x')
      keyboard.release('x')
      gestureDetected = determineDataTrends(xData, yData, X_DATA_THRESHOLD, Y_DATA_THRESHOLD)
      
      xData = []
      
      
      if gestureDetected is not None:
        
        #recordGesture(gestureDetected)
        break
        print("[INFO] Gesture detected: " + gestureDetected)
      time.sleep(1)
      keyboard.press('z')
      keyboard.release('z')
        
        
  #gesture = getCommand()

  #if gesture == "none":

    #continue
  
  #press key
  print("gesture is " + gestureDetected)
  if gestureDetected == "right":
    keyboard.press(Key.right)
    keyboard.release(Key.right)
  elif gestureDetected == "left":
    keyboard.press(Key.left)
    keyboard.release(Key.left)
    
