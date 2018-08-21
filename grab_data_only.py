import serial
import time
import csv
import sys
import pandas as pd
import matplotlib.pyplot as plt
import os
import codecs

import struct

## Read arduino data (press control+c to finish grabbing data) ##
def read_data(filename):
    ser = serial.Serial('/dev/cu.SLAB_USBtoUART', 115200) # ESP8266 port
    # ser = serial.Serial('/dev/cu.usbmodemFD121',115200) # My arduino port
    ser.flushInput()
    while True:
        ser_bytes = ser.readline()
        # print(ser_bytes)
        # decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
        new = str(ser_bytes)[4:-3]
        decoded_bytes = int(new, 16)#struct.unpack('>i', bytes.fromhex(new))
        # decoded_bytes = "{0:b}".format(decoded_bytes)
        # if decoded_bytes > 0x7FFFFFFF:
        #     decoded_bytes -= 0x100000000
        # # decoded_bytes = codecs.decode(new, "int")
        print(decoded_bytes)
        # print(new)

    # while True:
    #     try:
    #         ser_bytes = ser.readline()
    #         # print(ser_bytes)
    #         # decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
    #         decoded_bytes = codecs.decode(str(ser_bytes)[4:-3], "hex")
    #         # "707974686f6e2d666f72756d2e696f"
    #         print(decoded_bytes)
    #         # ser_bytes = str(ser_bytes)[2:-5]
    #         # print(ser_bytes)
    #         # with open(filename,"wb") as f:#a
    #             # f.write(ser_bytes)
    #             # writer = csv.writer(f,delimiter=' ',escapechar=' ', quoting=csv.QUOTE_NONE)#, quoting=csv.QUOTE_NONE,delimiter='|', quotechar='',escapechar='\'')
    #             # writer.writerow([ser_bytes])
    #     except:
    #         print("Keyboard Interrupt")
    #         break

read_data(str(sys.argv[1]))