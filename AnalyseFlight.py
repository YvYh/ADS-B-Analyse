import csv
import pandas as pd
import numpy as np

file = open('../../Thales/log.txt', 'r')
line = file.readlines(1500)
title = line[-2:-1]
col = [x.strip(' ') for x in [i.split('|') for i in line[-2:-1]][0]]
col = col[1:-1]
line = file.readline()
while line != "":
	data_list=[]
	while (line != title[0]):
		line = [x.strip(' ') for x in line.split('|')][1:-1]
		data_list.append(line)
		line = file.readline()

	data = pd.DataFrame(data_list,columns=col)
	data = data.iloc[:-2,:]

	for name in ['lat', 'lon','velocity','heading','vertrate','baroaltitude','geoaltitude','lastposupdate','lastcontact']:
		data[name] = pd.to_numeric(data[name], errors='coerce')
	
	callsign = data.iloc[-1]['callsign']

	coor=data.loc[:,['lat','lon','geoaltitude']]
	coor=coor.dropna(how='any')
	coor.to_csv('../../Thales/coordinate/{}.csv'.format(callsign), index=False)
	line = file.readline()
	line = file.readline()

file.close()