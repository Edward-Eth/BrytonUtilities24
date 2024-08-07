"""
Converts GPX file to nested list of [[Lat, Long, Alt],...] for processing.
"""
import os
import unittest.case

from geopy import distance
import matplotlib.pyplot as pl


class GpxToList:
    def __init__(self, filename):
        """
        Class init, will probably end up running the conversion and assigning the list to self somehow.

        :param filename: Name of GPX file to read in.
        """
        if type(filename) is not str:
            raise ValueError("The filename must be a string value.")
        if not os.path.isfile(filename):
            raise ValueError("The given file does not exist.")

        self.gpx_lines = []
        self.dist = []
        self.ele = []

        self.readfile(filename)

        self.strip_lines()

        self.calculate_distances()

        return

    def readfile(self, filename):
        """
        Reads the gpx file to a list of lines, and removes all values before the start of the track.

        :param filename:
        :return:
        """

        with open(filename) as gpx:
            self.gpx_lines = [line.rstrip() for line in gpx]

        start_loc = self.gpx_lines.index("<trkseg>")
        end_loc = self.gpx_lines.index("</trkseg>")

        self.gpx_lines = self.gpx_lines[start_loc+1:end_loc-1]

        return

    def strip_lines(self):
        newlist = []
        for index, line in enumerate(self.gpx_lines):
            if "<trkpt" in line:
                newline = self.strip_trkpt(line)
                newline.append(self.strip_ele(self.gpx_lines[index+1]))
                newlist.append(newline)
        self.gpx_lines = newlist
        return

    @staticmethod
    def strip_trkpt(point):
        return [float(point.split('"')[1]), float(point.split('"')[3])]

    @staticmethod
    def strip_ele(point):
        return float(point.split(">")[1].split("<")[0])

    def calculate_distances(self):
        dist = []
        ele = []
        for index, point in enumerate(self.gpx_lines):
            if index == 0:
                dist.append(0.0)
                ele.append(point[2])
            else:
                dist.append(distance.distance(self.gpx_lines[index-1][:2], point[:2]).km*1000+dist[-1])
                ele.append(point[2])
        self.dist = dist

        min_ele = min(ele)
        ele = [val - min_ele for val in ele]
        self.ele = ele


if __name__ == "__main__":
    WFtoYalding = GpxToList(r"C:\Users\Edward\Desktop\WFtoYalding.gpx")
    YaldingtoWF = GpxToList(r"C:\Users\Edward\Desktop\YaldingToWF.gpx")
    HintonHill = GpxToList(r"C:\Users\Edward\Desktop\HintonHill.gpx")
    VigoHill = GpxToList(r"C:\Users\Edward\Desktop\VigoHill.gpx")
    Bristol = GpxToList(r"C:\Users\Edward\Desktop\Bristol.gpx")
    BoxHill = GpxToList(r"C:\Users\Edward\Desktop\BoxHill.gpx")
    Hardknott = GpxToList(r"C:\Users\Edward\Desktop\Hardknott.gpx")
    Biggin = GpxToList(r"C:\Users\Edward\Desktop\Biggin.gpx")
    Ditchling = GpxToList(r"C:\Users\Edward\Desktop\Ditchling2.gpx")

    pl.figure()
    pl.title("Climb comparison")
    pl.plot(WFtoYalding.dist, WFtoYalding.ele, label="West Farleigh to Yalding")
    # pl.plot(YaldingtoWF.dist, YaldingtoWF.ele, label="Yalding to West Farleigh")
    pl.plot(HintonHill.dist, HintonHill.ele, label="Hinton Hill")
    pl.plot(VigoHill.dist, VigoHill.ele, label="Vigo Hill")
    # pl.plot(Bristol.dist, Bristol.ele, label="City Centre Bristol to downs")
    # pl.plot(BoxHill.dist, BoxHill.ele, label="Box Hill")
    # pl.plot(Hardknott.dist, Hardknott.ele, label="Hardknott")
    pl.plot(Biggin.dist, Biggin.ele, label="Biggin Hill")
    pl.plot(Ditchling.dist, Ditchling.ele, label="Ditchling Hill")
    pl.xlabel("Distance, m")
    pl.ylabel("Elevation gained, m")
    pl.legend()
    pl.show()

    a = 1