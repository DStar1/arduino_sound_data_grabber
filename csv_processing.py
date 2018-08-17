import pandas as pd
import sys

filename = str(sys.argv[1])
csv = pd.read_csv(filename, names = ['timeStamp', 'rawData'])
csv.drop(csv.index[0], inplace=True)
csv.reset_index(inplace=True)
csv.drop(['index'], axis=1, inplace=True)
csv['timeStamp'] -= csv['timeStamp'][0]
# csv['second'] = 0
# tmp = csv['timeStamp'].shift(-1).fillna(0)
# csv['second'] = tmp
# csv = csv[:-1]
# csv['offset'] = csv['second'] - csv['timeStamp']
print(csv['rawData'].mode())
print(csv['rawData'].describe())
csv['rawData'] = csv['rawData']-float((csv['rawData'].mode()))
print(csv)
# csv = csv.loc[csv['timeStamp'] % 8 == 0]
# print(csv)
# print(19432%8)


# csv.to_csv('final_csv5.csv', sep=',', index=False)
# print(csv)
