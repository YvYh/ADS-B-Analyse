import csv
import pandas as pd
import numpy as np

file = open('../log.txt', 'r')
line = file.readlines(1500)
title = line[-2:-1]
col = [x.strip(' ') for x in [i.split('|') for i in line[-2:-1]][0]]
col = col[1:-1]
line = file.readline()
line = [x.strip(' ') for x in line.split('|')][1:-1]
count_null = 0

while True:
	data_list=[]
	callsign = line[7]
	data = pd.DataFrame(columns=col)
	
	while ((line[7] == callsign)):
		data_list.append(line)
		line = file.readline()
		line = [x.strip(' ') for x in line.split('|')][1:-1]
		if (line==[]):
			for i in range (4):
				line = file.readline()
				if (line == ""):
					break;
				else: 
					line = [x.strip(' ') for x in line.split('|')][1:-1]
	if ("" == line):
		break
	data = pd.DataFrame(data_list,columns=col)
	for name in ['lat', 'lon','velocity','heading','vertrate','baroaltitude','geoaltitude','lastposupdate','lastcontact']:
		data[name] = pd.to_numeric(data[name], errors='coerce')
	
	coor=data.loc[:,['lat','lon','geoaltitude']]
	coor=coor.dropna(how='any')
	coor=coor.drop_duplicates()
	if (len(coor)>0):
		if (callsign=="NULL"):
			callsign = ('{}-N{}'.format(line[7], count_null))
			count_null = count_null+1
		
		coor.to_csv('../coordinate/{}.csv'.format(callsign), index=False)
		print('{} fine'.format(callsign))
	
file.close()