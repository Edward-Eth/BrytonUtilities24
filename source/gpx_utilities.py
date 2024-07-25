# Library to work with .gpx files
# gpxpy needs to be installed
# geopy needs to be installed
import gpxpy
from datetime import datetime
# from geopy import distance

from sys import argv
from os.path import splitext
from struct import pack
import re

from gpxpy.gpx import GPX

orst2brt = {
0: 3,
1: 2,
2: 7,
3: 6,
4: 5,
5: 4,
6: 1,
7: 10,
8: 8,
9: 12,
10: 1,
11: 1,
12: 9,
13: 8,
14: 1
    }

def decode_gpx_ors(gpx_path):
    gpx_file = open(gpx_path,'r')
    gpx_file = gpx_file.read()
    # breaks single line file in multiple files
    gpx_file = gpx_file.split('<')

    latitude = []
    longitude = []
    altitude = []
    instruction = []
    name = []
    number_items = 0
    for line in gpx_file:
        line = '<'+line
        if line.find('lat=') != -1:
            lat = line.split('"')[1]
            latitude.append(lat)
            lon = line.split('"')[3]
            longitude.append(lon)
            ins = 15
            instruction.append(ins)
            alt = 0
            altitude.append(alt)
            nam = 'none'
            name.append(nam)
            number_items +=1
        elif line.find('<type>') != -1 and number_items>0:
            ins = int(line.lstrip().removeprefix('<type>'))
            instruction.pop()
            instruction.append(ins)
        elif line.find('<name>') != -1 and number_items>0:
            nam = line.strip().removeprefix('<name>')
            name.pop()
            name.append(nam)
        elif line.find('<ele>') != -1 and number_items>0:
            alt = line.lstrip().removeprefix('<ele>')
            altitude.pop()
            altitude.append(alt)

    for i in range(0,len(name)-1):
        if name[i] == name[i+1]:
            instruction[i+1] = 15
    decoded_gpx = {"latitude": latitude,
                   "longitude": longitude,
                   "altitude": altitude,
                   "instruction": instruction,
                   "name": name}
    return decoded_gpx

def decode_gpx_plotaroute(gpx_path):
    gpx_file = open(gpx_path,'r')
    gpx_file = gpx_file.read()
    # breaks single line file in multiple files
    gpx_file = gpx_file.split('\n')

    latitude = []
    longitude = []
    altitude = []
    instruction = []
    name = []
    time = []
    number_items = 0
    for line in gpx_file:
        if line.find('lat=') != -1:
            lat = line.split('"')[1]
            latitude.append(lat)
            lon = line.split('"')[3]
            longitude.append(lon)
            instruction.append('none')
            altitude.append(0)
            name.append('none')
            time.append('none')
            number_items +=1
        elif line.find('<sym>') != -1 and number_items>0:
            ins = line.lstrip().removeprefix('<sym>').removesuffix('</sym>')
            instruction.pop()
            instruction.append(ins)
        elif line.find('<desc>') != -1 and number_items>0:
            nam = line.strip().removeprefix('<desc>').removesuffix('</desc>')
            name.pop()
            name.append(nam)
        elif line.find('<ele>') != -1 and number_items>0:
            alt = line.lstrip().removeprefix('<ele>').removesuffix('</ele>')
            altitude.pop()
            altitude.append(alt)
        elif line.find('<time>') != -1 and number_items>0:
            tim = datetime.fromisoformat(line.lstrip().removeprefix('<time>').removesuffix('</trkpt>').removesuffix('</time>')).timestamp()
            time.pop()
            time.append(tim)

    # After extraction, we need to slot in the waypoints where needed by sorting the lists according to the time values extracted
    sortedZip = sorted(zip(time, latitude, longitude, instruction, name, altitude))
    strippedTime = []
    strippedLatitude = []
    strippedLongitude = []
    strippedInstruction = []
    strippedName = []
    strippedAltitude = []

    for i, point in enumerate(sortedZip):
        if (point[3] != 'none' or point[4] != 'none') or (i == 0 and (point[0] != sortedZip[i+1][0])) or (point[0] != sortedZip[i-1][0] and point[0] != sortedZip[i+1][0]): ## If the point has an instruction, keep it
            strippedTime.append(point[0])
            strippedLatitude.append(point[1])
            strippedLongitude.append(point[2])
            strippedInstruction.append(point[3])
            strippedName.append(point[4])
            strippedAltitude.append(point[5])

    for i in range(0,len(name)-1):
        if name[i] == name[i+1]:
            instruction[i+1] = 15

    decoded_gpx = {"latitude": strippedLatitude,
                   "longitude": strippedLongitude,
                   "altitude": strippedAltitude,
                   "instruction":strippedInstruction,
                   "name": strippedName}
    return decoded_gpx

def decode_gpx_gmaps(gpx_path): ## this one seems to be wrong altogether
    gpx_file = open(gpx_path, 'r')
    latitude = []
    longitude = []
    altitude = []
    instruction = []
    name = []
    for line in gpx_file:
        ins = 'null'
        if line.find('lat=') != -1: # If the line contains a latitude value
            lat = line.split('"')[1]
            latitude.append(lat) ## Store latitude
            lon = line.split('"')[3]
            longitude.append(lon) ## Store longitude
            ins = 'none'
            instruction.append(ins) ## Store no instruction
            alt = 0
            altitude.append(alt)
            nam = ''
            name.append(nam)
        if line.find('<cmt>') !=-1:
            ins = line.lstrip().removeprefix('<cmt>').removesuffix('</cmt>\n')
            instruction.pop()
            instruction.append(ins)
        if line.find('<ele>') != -1:
            alt = line.lstrip().removeprefix('<ele>').removesuffix('</ele>\n')
            altitude.pop()
            altitude.append(alt)

    decoded_gpx = {"latitude": latitude,
                   "longitude": longitude,
                   "altitude": altitude,
                   "instruction":instruction,
                   "name": name}

    return decoded_gpx
        #if line.find()

def decode_gpx(gpx_path):
    gpx_file=open(gpx_path, 'r')
    line = gpx_file.read()
    if '<name>openrouteservice</name>' in line:
        decoded_gpx = decode_gpx_ors(gpx_path), 'ors'
    elif '<desc>Route created on plotaroute.com</desc>' in line:
        decoded_gpx = decode_gpx_plotaroute(gpx_path), 'par'
    else:
        decoded_gpx = decode_gpx_gmaps(gpx_path), 'gmp'


  #  l=0
   # for track in gpx.tracks:
    #    for segment in track.segments:
     #       for i in range (0,len(segment.points)-1):
      #          if segment.points[i].comment is not None:
       #             if l is 1:
        #                pass
         #               #print(distance.distance((segment.points[i].latitude, segment.points[i].longitude),(lat,lon)))
          #          lat = segment.points[i].latitude
           #         lon = segment.points[i].longitude
            #        l = 1
             #   #print(distance.distance((segment.points[i].latitude, segment.points[i].longitude), (segment.points[i+1].latitude, segment.points[i+1].longitude)).km)


    return decoded_gpx