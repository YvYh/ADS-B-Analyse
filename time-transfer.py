from datetime import datetime
import pandas as pd
time = datetime.fromtimestamp(1535955340)
#print('%r %r' % (type(time),time))

data = pd.read_csv("../coor/CXA817.csv")
for i in range(len(data.time)):
	data.time[i] = datetime.fromtimestamp(data.time[i])
data.to_csv("../coor/NEW-CXA817.csv", index=False)