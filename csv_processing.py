import pandas as pd
import sys

filename = str(sys.argv[1])
csv = pd.read_csv(filename, names = ['timeStamp', 'rawData'])
csv.drop(csv.index[0], inplace=True)
csv.reset_index(inplace=True)
csv.drop(['index'], axis=1, inplace=True)
csv['timeStamp'] -= csv['timeStamp'][0]
csv['rawData'] = csv['rawData']-(csv['rawData'].mean())
# csv = csv.loc[csv['timeStamp'] % 8 == 0]
# print(csv)
# print(19432%8)
csv.to_csv('final_csv3.csv', sep=',', index=False)
# print(csv)
