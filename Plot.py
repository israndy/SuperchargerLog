#
#   Plot.py
#   script to read the .csv output files of the script SuperchargerLog.py
#   and plot the data on a graph
#


import sys
import datetime
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg') # Change the default to work on my Mac

def readdate(date):
    idate = date.split()[0].split('-')
    idate.append(date.split()[1].split(':')[0])
    idate.append(date.split()[1].split(':')[1])
    return(idate)

timestamp = []
apoints = []
bpoints = []
cpoints = []
dpoints = []

LogFile = "/Users/israndy/Desktop/Superchargers.csv"
file = open(LogFile, "rt")
line = file.readline() # Pop the header line off the file

line = file.readline()
i = readdate(line.split(',')[0])
start=datetime.datetime(int(i[0]),int(i[1]),int(i[2]),int(i[3]),int(i[4]))

while line:
    i = readdate(line.split(',')[0])
    end = datetime.datetime(int(i[0]),int(i[1]),int(i[2]),int(i[3]),int(i[4]))
    timestamp.append(end)
    splitline = line.split(',')
    apoints.append(int(splitline[3]) - int(splitline[2]))
    bpoints.append(int(splitline[6]) - int(splitline[5]))
    cpoints.append(int(splitline[9]) - int(splitline[8]))
    dpoints.append(int(splitline[12]) - int(splitline[11]))
    line = file.readline()
file.close()

plt.title("Local Supercharger Avaiability")
plt.xlabel(start.strftime("%a %I:%M %p")+" to "+end.strftime("%a %I:%M %p"))
plt.ylabel("chargers in use")
plt.plot(timestamp, apoints, label=splitline[1]+"   "+splitline[3])
plt.plot(timestamp, bpoints, label=splitline[4]+"    "+splitline[6])
plt.plot(timestamp, cpoints, label=splitline[7]+"    "+splitline[9])
plt.plot(timestamp, dpoints, label=splitline[10]+" "+splitline[12])
plt.legend()
plt.show()
