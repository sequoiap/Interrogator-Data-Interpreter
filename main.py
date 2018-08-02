import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from classes.Measurement import Measurement

measurements = []
path = 'files/'
selectedMeasurements = []
frequencyMode = False
speed_of_light = 299792458

def WelcomeMessage():
    print("--------------------------------------------")
    print("Welcome to the Interrogator Data Interpreter")
    print("Written by Sequoia Ploeg")

def processFiles():
    print("\nProcessing files...")
    for filename in os.listdir(path):
        measurements.append(Measurement(path + filename))

def selectMeasurements():
    print("Number of files processed: " + str(len(measurements)))
    print("Type which measurements you want processed, separated by spaces, or any non-number to terminate:\n")
    print("Index\tName\t\tPath")
    print("-----\t----\t\t----")
    for x in range(len(measurements)):
        print(str(x) + ":\t" + measurements[x].getName() + "\t\t" + measurements[x].getPath())
    print("")
    indexInput()

def setFrequencyMode():
    global frequencyMode
    while True:
        answer = input("Plot by (f)requency or (w)avelength: ")
        if answer == 'f':
            frequencyMode = True
            break
        elif answer == 'w':
            frequencyMode = False
            break
        else:
            continue

def indexInput():
    global selectedMeasurements
    valid = False
    while not valid:
        a = input("Indices (space delimited) or 'all': ")
        if a == 'all':
            selectAllMeasurements()
            break
        selectedMeasurements = a.split(' ')
        for item in selectedMeasurements:
            if not str.isnumeric(item):
                print("Goodbye!")
                exit()
        for i in range(len(selectedMeasurements)):
            selectedMeasurements[i] = int(selectedMeasurements[i])
        selectedMeasurements.sort()
        if selectedMeasurements[len(selectedMeasurements) - 1] > len(measurements) or selectedMeasurements[0] < 0:
            print("Invalid selecton. ", end='')
            selectedMeasurements = []
        else:
            break
        
def selectAllMeasurements():
    for i in range(len(measurements)):
        selectedMeasurements.append(i)

def singleFigure():
    global selectedMeasurements
    global frequencyMode
    # Set up plot
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    # Put data on plot
    for x in selectedMeasurements:
        plotMeasurement(x, ax)
    # Label the plot
    plt.ylim(ymax=0)
    if frequencyMode == False:
        plt.xlabel("Wavelength (nm)")
    else:
        plt.xlabel("Frequency (THz)")
    plt.ylabel("Power (dBm)")
    plt.title("Selected Interrogator Data")
    plt.grid()
    # Show the plot full screen and as top window
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    plt.show()
    fig.canvas.manager.window.raise_()

def plotMeasurement(index, axis):
    # Get data
    data = measurements[index].getData()
    # Get channels to plot
    channels = selectChannels(index, measurements[index].getName())
    # Add selected channels to plot
    for channel in channels:
        addPlot(axis, data, channel, measurements[index].getName())
    

def addPlot(axis, data, channel, label):
    global frequencyMode
    global speed_of_light
    # Get selected data
    wavelength = data[:,0]
    if frequencyMode == True:
        wavelength = speed_of_light / (wavelength * np.power(10, 3))
    ch1 = data[:,channel]
    legend = "CH" + str(channel) + " " + label
    # Plot
    axis.plot(wavelength, ch1, marker="o", markersize=1, label=legend)
    axis.legend()

def selectChannels(index, name):
    channels = []
    channels = input("Type channel numbers (space delimited) for file " + str(index) + ": " + name + ": ").split(' ')
    for i in range(len(channels)):
        if not str.isnumeric(channels[i]):
            del channels[i]
        else:
            channels[i] = int(channels[i])
    return channels

if __name__ == "__main__":
    WelcomeMessage()
    processFiles()
    selectMeasurements()
    setFrequencyMode()
    # if single figure:
    singleFigure()
    # else if multiple figures or plots:
