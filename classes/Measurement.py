from . import ChanConfig as cc
import numpy as np

class Measurement:

    # CLASS ATTRIBUTES:
    # date (string)
    # name (string)
    # description (string)
    # module_type (string)
    # mux_level (string)
    # HW_acquisition_rate (string)
    # wavelength_tracking (string)
    # normalized (bool)
    # IP_address (string)
    # port (string)
    # IDN (string)
    # Image_ID (string)
    # sn (string)
    # wavelength_start (float)
    # wavelength_delta (float)

    def __init__(self, filepath):
        # Save the filepath
        self.path = filepath
        self.channels = []
        # Open the file, get the contents, and close it
        self.readfile()
        # Initialize the metadata
        self.InitMetadata()
        # Initialize the four channels' configurations
        for _ in range(4):
            self.InitChannel()
        # Ignore blank line
        self.getline()
        # Final preparations for data reading
        self.wavelength_start = float(self.getline().replace("Wavelength Start (nm): ",""))
        self.wavelength_delta = float(self.getline().replace("Wavelength Delta (nm): ",""))
        self.getline() # blank line
        self.getline() # table headers
        self.getline() # blank line
        # Get data from table
        self.data = np.matrix(np.zeros([16000,5]))
        self.readData()
        # For testing: print data
        # self.PrintMetadata()
        # for x in range(4):
        #     self.channels[x].print()
        # print(self.wavelength_start)
        # print(self.wavelength_delta)
        # print(self.data)

    def getline(self):
        # Return the line and increment the counter
        line = self.lines[self.linenumber]
        self.linenumber += 1
        return line

    def readfile(self):
        self.file = open(self.path, 'r')
        self.lines = self.file.read().splitlines()
        self.linenumber = 0
        self.file.close()

    def InitMetadata(self):
        # Skip the blank line that begins each file
        self.getline()
        # Get the date:
        self.date = self.getline().replace("Date: ","")
        # Get the name (rename if necessary):
        self.name = self.getline().replace("Name: ","")
        if self.name == "":
            self.name = self.path.replace("files/","")
            self.name = self.name.replace(".txt","")
        # Get the description:
        self.description = self.getline().replace("Description: ","")
        # Get the module type:
        self.module_type = self.getline().replace("Module Type: ","")
        # Get the mux level:
        self.mux_level = self.getline().replace("Mux Level: ","")
        # Get the HW acquisition rate:
        self.HW_acquisition_rate = self.getline().replace("HW Acquisition Rate: ","")
        # Get the wavelength tracking:
        self.wavelength_tracking = self.getline().replace("Wavelength Tracking: ","")
        # Get the normalized bool:
        compare = self.getline().replace("Normalized: ","")
        if compare == "True":
            self.normalized = True
        else:
            self.normalized = False
        # Ignore the blank line:
        self.getline()
        # Get the IP_address:
        self.IP_address = self.getline().replace("IP Address: ","")
        # Get the port number:
        self.port = self.getline().replace("      Port: ","")
        # Ignore the blank line:
        self.getline()
        # Get the IDN
        self.IDN = self.getline().replace("IDN: ","")
        # Get the Image_ID
        self.Image_ID = self.getline().replace("Image ID: ","")
        # Get the serial number
        self.sn = self.getline().replace("S/N: ","")

    def InitChannel(self):
        # Skip the first blank line
        self.getline()
        # Get the channel number
        channel = self.getline().replace("CH ","")
        channel= channel.replace(" Configuration:","")
        channel = int(channel)
        # Get the distance compensation enabled bool
        dist_comp_enabled = self.getline().replace("\tDistance Compensation Enabled: ","")
        if dist_comp_enabled == "True":
            dist_comp_enabled = True
        else:
            dist_comp_enabled = False
        # Get the spectral advantage count
        spec_adv_count = self.getline().replace("\tSpectral Average Count: ","")
        # Get the threshold
        threshold = self.getline().replace("\tThreshold: ","")
        # Get the relative threshold
        rel_threshold = self.getline().replace("\tRel. Thresh.: ","")
        # Get the width level
        width_lvl = self.getline().replace("\tWidth Level: ","")
        # Get the wdith
        width = self.getline().replace("\tWidth: ","")
        # Get the detect valleys bool
        detect_valley = self.getline().replace("\tDetect Valley: ","")
        if detect_valley == "True":
            detect_valley = True
        else:
            detect_valley = False
        # Add all this info to a channel config in the list
        self.channels.append(cc.ChanConfig(channel,dist_comp_enabled,spec_adv_count,threshold,rel_threshold,width_lvl,width,detect_valley))

    def readData(self):
        row = 0
        while self.linenumber < len(self.lines):
            vals = self.getline().split('\t')
            for column in range(5):
                self.data[row,column] = vals[column]
            row += 1

    def getData(self):
        return self.data

    def getName(self):
        return self.name

    def getPath(self):
        return self.path

    def PrintMetadata(self):
        print(self.date)
        print(self.name)
        print(self.description)
        print(self.module_type)
        print(self.mux_level)
        print(self.HW_acquisition_rate)
        print(self.wavelength_tracking)
        print(self.normalized)
        print(self.IP_address)
        print(self.port)
        print(self.IDN)
        print(self.Image_ID)
        print(self.sn)
