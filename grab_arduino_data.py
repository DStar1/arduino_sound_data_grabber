import serial
import time
import csv
import sys
import pandas as pd
import matplotlib.pyplot as plt
import os

## Read arduino data (press control+c to finish grabbing data) ##
def read_data(filename):
    ser = serial.Serial('/dev/cu.SLAB_USBtoUART', 115200) # ESP8266 port
    # ser = serial.Serial('/dev/cu.usbmodemFD121',115200) # My arduino port
    ser.flushInput()

    while True:
        try:
            ser_bytes = ser.readline()
            ser_bytes = str(ser_bytes)[2:-5]
            # print(ser_bytes)
            with open(filename,"a") as f:
                writer = csv.writer(f,delimiter=' ',escapechar=' ', quoting=csv.QUOTE_NONE)#, quoting=csv.QUOTE_NONE,delimiter='|', quotechar='',escapechar='\'')
                writer.writerow([ser_bytes])
        except:
            print("Keyboard Interrupt")
            break

## Proccessing/augmenting csv file ##
def process_csv(filename, outfile):
    csv = pd.read_csv(filename, names = ['timeStamp', 'rawData'])
    csv.drop(csv.index[0], inplace=True)
    csv.reset_index(inplace=True)

    csv.drop(['index'], axis=1, inplace=True)
    csv['timeStamp'] -= csv['timeStamp'][0]
    csv['rawData'] = csv['rawData']-float((csv['rawData'].mode()))

    ## Add endTimeStamp ##
    # tmp = csv['timeStamp'].shift(-1).fillna(0)
    # csv['endTimeStamp'] = tmp
    # csv = csv[:-1]
    # csv['offset'] = csv['endTimeStamp'] - csv['timeStamp']
    csv.to_csv(outfile, sep=',', index=False)
    # print(csv)

## Plot the audio file if last flag ##
def plot(filename):
    df = pd.read_csv(filename)
    print(df)
    check = int(len(df['timeStamp'])/3)
    print(df)
    # print((df.describe()))
    x = df['timeStamp']
    y = df['rawData']
    plt.plot(x,y)
    plt.show()

## Grab data then parse then plot if 1
if __name__ == "__main__":
    if len(sys.argv) <= 3:
        print("Add arags: 1: original_data_filename, 2: finalized_data_filename, 3: 0-1(plot, no_plot)")
        exit(-1)
    filename = str(sys.argv[1])
    if os.path.isfile(filename):
        os.remove(filename)
    final_file = str(sys.argv[2])
    read_data(filename)
    process_csv(filename, final_file)
    if int(sys.argv[3]):
        plot(final_file)

