import pandas as pd
import sys

filename = str(sys.argv[1])
csv = pd.read_csv(filename, names = ['timeStamp', 'rawData'])
# csv.drop(csv.index[0], inplace=True)
csv['timeStamp'] -= csv['timeStamp'][0]
print(csv)
