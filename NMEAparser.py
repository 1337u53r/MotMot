# -*- coding: utf-8 -*-
#NMEA 'GPRMC' Parser
#Gavin Prue & Michael Lendvai @ University of Warwick 2019

from paramiko import SSHClient
from scp import SCPClient
import base64
import time

######################## Use this snippet for manual user input of the NMEA Sentence########################################
#nmea = input("Please enter a NMEA sentence: ")      #Input the NMEA sentence here - Currently on works for 'GPRMC' sentences
#nmeaSplitSentence = nmea.split(",")     #Splits the NMEA sentence into sections (type,time,status etc.)
#print (nmeaSplitSentence)
############################################################################################################################

def parser():

    longlat = open("/home/pi/MotMot/longlat.txt", "w+")   #creates the file in the current directory
    longlat.close()
    latlng = open("/home/pi/MotMot/latlng.txt", "w+")    #creates the file in the current directory(ensures it exists so not to throw an error when removing duplicates)
    latlng.close()
    satView = "0"
    with open("/home/pi/MotMot/data.txt", "r") as data:     #opens the file containg the captured data
        for line in data:
            nmea = line #Sets the variable equal to the string in data.txt
            nmeaSplitSentence = nmea.split(",")     #Splits the NMEA sentence into sections (type,time,status etc.)

            if "GPRMC" in nmea:
                type = "GPRMC"        #Assign each section of the NMEA sentence a variable
                time = nmeaSplitSentence[1:2]
                latitude = nmeaSplitSentence[3:4]       # Latitude: DDMM.MMMM (The first two characters are the degrees.)
                latitudeDir = nmeaSplitSentence[4:5]
                longitude = nmeaSplitSentence[5:6]      #Longitude: DDDMM.MMMM (The first three characters are the degrees.)
                longitudeDir = nmeaSplitSentence[6:7]
                date = nmeaSplitSentence[9:10]
                

                type = str(type)       #Makes object variables into string reprsentations
                time = str(time)
                latitude = str(latitude)
                latitudeDir = str(latitudeDir)
                longitude = str(longitude)
                longitudeDir = str(longitudeDir)
                date = str(date)

                removeSplitter = ["'", "[", "]"]        #Removes the brackets and hypen from the orginal sentence split to allow for string manipulation

                for splitter in removeSplitter:
                    time = time.replace(splitter, '')
                    latitude = latitude.replace(splitter, '')
                    latitudeDir = latitudeDir.replace(splitter, '')
                    longitude = longitude.replace(splitter, '')
                    longitudeDir = longitudeDir.replace(splitter, '')
                    date = date.replace(splitter, '')
                afterParse = open("/home/pi/MotMot/longlat.txt", "a+")       #use this to write to a file in the same location as this program

                #if the length of the NMEA sentence is 38 after the splitting (meaning it's a GPRMC sentence) then write the needed data into a txt file
                if len(type + " " + latitude[0:2] + "°" + latitude[2:8] + latitudeDir + " " + longitude[0:3] + "°" + longitude[3:9] + longitudeDir + " " + time[0:2] + ":" + time[2:4] + ":" + time[4:6] + "\n") == 38:
                  afterParse.write(type + " " + latitude[0:2] + "°" + latitude[2:8] + latitudeDir + " " + longitude[0:3] + "°" + longitude[3:9] + longitudeDir + " " + time[0:2] + ":" + time[2:4] + ":" + time[4:6] + " " + date[0:2] + "/" + date[2:4] + "/" + date[4:6] + "\n")       #write the long and lat to the file ready to be plotted
                  #Open another txt file. This file gets transferred to the server, holding the required coordinates and extra details we use to show stuff on the website
                  DMS = open("/home/pi/MotMot/latlng.txt", "a+")
                  #Converting the latitude (DMS) to decimal for the website to understand
                  if(latitude[0:2] not in ".0123456789"):   #Weird way to avoid processing bad input but it works
                      if("[" not in latitude[0:2]):
                              if("\\" not in latitude[0:2]) and ("x" not in latitude[0:2]) and (";" not in latitude[0:2]):
                                      degree = int(latitude[0:2])
                  if(latitude[2:] not in ".0123456789"):
                      if("]" not in latitude[2:]):
                              if("\\" not in latitude[2:]) and ("x" not in latitude[2:]) and (";" not in latitude[2:]):
                                      min = float(latitude[2:])
                  #sec = float(latitude[5:8])
                  #Writing out the decimal latitude value to latlng.txt
                  if (date[4:6] == "19"):
                      #This was the most accurate conversion method from DMS to decimal
                        MiNuTs = (min/60) #+ (sec/3600)
                        #DMS.write(latitude + " ")
                        DMS.write(str(degree) + "." + str(MiNuTs)[2:8] + " ")

                  #If first 2 characters of longitude is 00 then it's a negative number, so convert it that way.
                  if(longitude[0:2] == "00"):
                        #Convert longitude DMS to decimal (Taking 00's into consideration)
                        degree = "-" + longitude[2:3]
                  else:
                        degree = longitude[0:3]
                  if(longitude[3:5] not in ".0123456789"):
                      #Ignore string inputs that might cause problems when trying to convert to float & int
                      if ("]" not in longitude[3:5]) and ("A^" not in longitude[3:5]):
                              min = float(longitude[3:5])
                              sec = float("0." + longitude[6:9])
                              min+= sec
                  if (date[4:6] == "19"):
                        DMS.write(degree + "." + str(round((min/60),4))[2:] + " " + time[0:2] + ":" + time[2:4] + ":" + time[4:6] + " " + date[0:2] + "/" + date[2:4] + "/" + date[4:6] + " " + satView + " " + "\n")
                  DMS.close()
                    #Print out debug info in terminal
                  print ("Type: " + type)        #Displays the NMEA sentence in Human Readable form
                  print ("Time: ", time[0:2] + ":" + time[2:4] + ":" + time[4:6])
                  print ("Latitude: ", latitude[0:2] + "°" + latitude[2:9] + latitudeDir)
                  print ("Longitude: ", longitude[0:3] + "°" + longitude[3:10] + longitudeDir)
                  print ("Date: ", date[0:2] + "/" + date[2:4] + "/" + date[4:6])
                afterParse.close()      #Close the file after writing

            #GPGSV type sentence handling (for satellite numbers)
            '''elif "GPGSV" in nmea:
                type = "GPGSV"        #Assign each section of the NMEA sentence a variable
                satView = nmeaSplitSentence[3:4]
                satNum  = nmeaSplitSentence[4:5]
                satView = str(satView)
                satNum = str(satNum)
                removeSplitter = ["'", "[", "]"]

                for splitter in removeSplitter:
                    satView = satView.replace(splitter, '')
                    satNum = satNum.replace(splitter, '')
                    afterParse = open("/home/pi/MotMot/longlat.txt", "a+")       #use this to write to a file in the same location as this program

                afterParse.write(type + " " + satView + " " + satNum + " " + "\n")       #write the long and lat to the file ready to be plotted
                afterParse.close()      #Close the file after writing'''

def removeDups():
    #Remove duplicate entries (needs to have "latlng.txt" already created)
    dupCheck = open("/home/pi/MotMot/latlng.txt", "r").readlines()    #opens the file and reads each line ready to check for duplicates
    dupCheck_set = set(dupCheck)                      #Creates a set from the contents of the file ready to loop through('set' is used, as it creates a set using only unqiue lines)
    dupremoved = open("/home/pi/MotMot/latlng.txt", "w")               #opens file ready to overwrite the file

    for line in dupCheck_set:   #loop through and write lines from the set to file
        dupremoved.write(line)

def timeSorter():
    #sorts the entries into time order
    timeSort = open("/home/pi/MotMot/latlng.txt", "r").readlines()   #opens the file and reads each line
    timeSorted = sorted(timeSort, key=lambda i: (i.split(" ")[-4]), reverse=True)   #sorts the lines into order using the timestamps, change to "reverse=False" to put in ascending order
    reorderSortedTime = open("/home/pi/MotMot/latlng.txt", "w")     ##opens file ready to overwrite the file

    for line in timeSorted:     #loop through and write lines from the list to file
        reorderSortedTime.write(line)

def transfer():
    #Send the coordinates to the server
    ssh = SSHClient()
    ssh.load_host_keys('/home/pi/MotMot/known_hosts')   #looks to load the SSH key if it is saved locally
    ssh.connect("209.97.140.84", username=base64.b64decode("cm9vdA=="), password=base64.b64decode("VG9tVG9tV2FzSGVyZQ=="), look_for_keys=False)    #Connects to the server via SSH

    with SCPClient(ssh.get_transport()) as scp:
        scp.put('/home/pi/MotMot/latlng.txt', remote_path='/var/www/html')    #file that will be transfered to the server and the location it will be saved too (this will overwrite the file on the server everytime)
        scp.close()              #closes the connection

def main():
    time.sleep(10)
    while True:
        parser()
        removeDups()
        timeSorter()
        time.sleep(5)
        transfer()

main()
