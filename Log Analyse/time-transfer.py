from datetime import datetime
import pandas as pd
time = datetime.fromtimestamp(1535955340)
#print('%r %r' % (type(time),time))

data = pd.read_csv("../coor/CXA8667.csv")
for i in range(len(data.time)):
	time = datetime.fromtimestamp(data.time[i])
	data.time[i] = time.isoformat()
data.to_csv("../coor/NEW-CXA8667.csv")