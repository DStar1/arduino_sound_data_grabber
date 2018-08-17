import pandas as pd
import sys
import matplotlib.pyplot as plt

filename = str(sys.argv[1])
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

# plt.savefig
# csv.drop(csv.index[0], inplace=True)
# csv.reset_index(inplace=True)
# csv.drop(['index'], axis=1, inplace=True)
# csv['timeStamp'] -= csv['timeStamp'][0]

# csv.to_csv('final_csv.csv', sep=',', index=False)

