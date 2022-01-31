# -*- coding: utf-8 -*-
#NMEA 'GPRMC' Parser
#Gavin Prue 08/03/2019
#Added encoding declaration at the top to avoid encoding errors with python 2. 08/03/2019 by ML.

data = open("data.txt", "r")        #Opens the file data.txt to read the NMEA GPRMC sentence
nmea = (data.read())        #Sets the variable equal to the string in data.txt
nmeaSplitSentence = nmea.split(",")     #Splits the NMEA sentence into sections (type,time,status etc.)

######################## Use this snippet for manual user input of the NMEA Sentence########################################
#nmea = input("Please enter a NMEA sentence: ")      #Input the NMEA sentence here - Currently on works for 'GPRMC' sentences
#nmeaSplitSentence = nmea.split(",")     #Splits the NMEA sentence into sections (type,time,status etc.)
#print (nmeaSplitSentence)
############################################################################################################################

type = nmeaSplitSentence[:1]        #Assign each section of the NMEA sentence a variable
time = nmeaSplitSentence[1:2]
status = nmeaSplitSentence[2:3]
latitude = nmeaSplitSentence[3:4]       # Latitude: DDMM.MMMM (The first two characters are the degrees.)
latitudeDir = nmeaSplitSentence[4:5]
longitude = nmeaSplitSentence[5:6]      #Longitude: DDDMM.MMMM (The first three characters are the degrees.)
longitudeDir = nmeaSplitSentence[6:7]
speed = nmeaSplitSentence[7:8]
trackAngle = nmeaSplitSentence[8:9]
date = nmeaSplitSentence[9:10]

type = str(type)       #Makes object variables into string reprsentations
time = str(time)
status = str(status)
latitude = str(latitude)
latitudeDir = str(latitudeDir)
longitude = str(longitude)
longitudeDir = str(longitudeDir)
speed = str(speed)
trackAngle = str(trackAngle)
date = str(date)

removeSplitter = ["'", "[", "]"]        #Removes the brackets and hypen from the orginal sentence split to allow for string manipulation
for splitter in removeSplitter:
    type = type.replace(splitter, '')
    time = time.replace(splitter, '')
    status = status.replace(splitter, '')
    latitude = latitude.replace(splitter, '')
    latitudeDir = latitudeDir.replace(splitter, '')
    longitude = longitude.replace(splitter, '')
    longitudeDir = longitudeDir.replace(splitter, '')
    speed = speed.replace(splitter, '')
    trackAngle = trackAngle.replace(splitter, '')
    date = date.replace(splitter, '')

afterParse = open("longlat.txt", "w")       #use this to write to a file in the same location as this program
afterParse.write(latitude[0:2] + "°" + latitude[2:8] + latitudeDir + " " + longitude[0:3] + "°" + longitude[3:9] + longitudeDir )       #write the long and lat to the file ready to be plotted
afterParse.close()      #Close the file after writing

print "\nType: ", type        #Displays the NMEA sentence in Human Readable form
print "Time: ", time[0:2] + ":" + time[2:4] + ":" + time[4:6]
print "Status: ", status
print "Latitude: ", latitude[0:2] + "°" + latitude[2:9] + latitudeDir
print "Longitude: ", longitude[0:3] + "°" + longitude[3:10] + longitudeDir
print "Speed: ", speed + " Knots"
print "Track Angle: ", trackAngle + " Degrees"
print "Date: ", date[0:2] + "/" + date[2:4] + "/" + date[4:6]
