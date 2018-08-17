import serial
import time
import csv
import sys
import pandas as pd
import matplotlib.pyplot as plt
import os


def read_data(filename):
    ser = serial.Serial('/dev/cu.SLAB_USBtoUART', 115200)
    # ser.open()
    ser.flushInput()

    while True:
        # try:
        #     # print("Trying")
        #     ser_bytes = ser.readline()
        #     print(ser_bytes)
        #     # decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
        #     # print(decoded_bytes)
        #     with open("test_data.csv","a") as f:
        #         writer = csv.writer(f,delimiter=' ',escapechar=' ', quoting=csv.QUOTE_NONE)#, quoting=csv.QUOTE_NONE,delimiter='|', quotechar='',escapechar='\'')
        #         writer.writerow([ser_bytes])#[time.time(),ser_bytes])#decoded_bytes])
        #         # writer.writerow(map(int, [ser_bytes]))
        # except:
        #     print("Keyboard Interrupt")
        #     break

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

def process_csv(filename, outfile):
    # filename = str(sys.argv[1])
    csv = pd.read_csv(filename, names = ['timeStamp', 'rawData'])
    csv.drop(csv.index[0], inplace=True)
    csv.reset_index(inplace=True)
    csv.drop(['index'], axis=1, inplace=True)
    csv['timeStamp'] -= csv['timeStamp'][0]
    csv['rawData'] = csv['rawData']-(csv['rawData'].mean())
    # csv = csv.loc[csv['timeStamp'] % 10 == 0]######
    # print(csv)
    # print(19432%8)
    csv.to_csv(outfile, sep=',', index=False)
    # print(csv)

def plot(filename):
    # filename = str(sys.argv[1])
    df = pd.read_csv(filename)
    print(df)
    check = int(len(df['timeStamp'])/3)
    # df = df[check+500:-6000]
    print(df)
    # df['rawData'] = df['rawData']-(df['rawData'].mean())
    # print((df.describe()))
    x = df['timeStamp']
    y = df['rawData']
    plt.plot(x,y)
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) <= 3:
        print("Add arags: 1: filename, 2:finalized_filename, 3: 0-1(plot, no_plot), 4:")
        exit(-1)
    filename = str(sys.argv[1])
    if os.path.isfile(filename):
        os.remove(filename)
    final_file = str(sys.argv[2])
    read_data(filename)
    process_csv(filename, final_file)
    if int(sys.argv[3]):
        plot(final_file)

