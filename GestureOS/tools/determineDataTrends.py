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

import numpy

# Apply a linear regression to the x data and find the range of the y data to compare those values against pre-determined values for determining a gesture
def determineDataTrends(xData, yData, xDataThreshold, yDataThreshold):

    #@leemartinc
    Axisx = []
    nonZeroxData = []

    evalx1 = 0
    evalx2 = 0
    lenCounter= 0
               
    xslope = 0            
           
    if len(xData) > 3:
        for i in range(0, len(xData)):
           Axisx.append(i)
           print(xData[i])
           
        xslope, intercept = numpy.polyfit(Axisx, xData, 1)
        print("slope: ", xslope)
    

    if xslope > 7:

        gestureDetected = "right"

    elif xslope < -7:

        gestureDetected = "left"

    else:
        gestureDetected = None
   
    
    return gestureDetected
    #####