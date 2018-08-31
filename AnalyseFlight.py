import csv
import pandas as pd
import numpy as np


count_null = 0
filename = '../log.txt'
def write_coor_file(coor, callsign):
	global count_null
	if (callsign=="NULL"):
		callsign = ('N{}'.format(count_null))
		count_null = count_null+1
	coor.to_csv('../coor/{}.csv'.format(callsign), index=False)
	print('{} fine'.format(callsign))

file = open(filename, 'r')
line = file.readlines(1500)
title = line[-2:-1]
col = [x.strip(' ') for x in [i.split('|') for i in line[-2:-1]][0]]
col = col[1:-1]
line = file.readline()
line = [x.strip(' ') for x in line.split('|')][1:-1]
previous_data = pd.DataFrame(np.zeros((1,17)), columns=col)
previous_callsign="NULL"

while True:
	data_list=[]
	callsign = line[7]
	
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
	data = data.dropna(subset=['lat','lon'])
	for name in ['lat', 'lon','velocity','heading','vertrate','baroaltitude','geoaltitude','lastposupdate','lastcontact']:
		data[name] = pd.to_numeric(data[name], errors='coerce')
	data = data.drop_duplicates(subset=['lat','lon'])
	'''
	if(len(data)>0):
		#this callsign == null
		if (callsign == 'NULL'):
			#connected with previous path
			if (abs(data.iloc[0]['lat']-previous_data.iloc[-1]['lat'])<0.01) & (abs(data.iloc[0]['lon']-previous_data.iloc[-1]['lon'])<0.01):
				previous_data = previous_data.append(data, ignore_index=True)
				
			#not connected
			else:
				#save previous path
				if(len(previous_data)>0):
					write_coor_file(previous_data, previous_data.iloc[0]['callsign'])
				#put this path into previous_data
				previous_data = data
		#this callsigh != null and previous callsigh == null
		elif(previous_data.iloc[0]['callsign']=='NULL'):
			#connected with previous path
			if (abs(data.iloc[0]['lat']-previous_data.iloc[-1]['lat'])<0.01) & (abs(data.iloc[0]['lon']-previous_data.iloc[-1]['lon'])<0.01):
				previous_data = previous_data.append(data, ignore_index=True)
				
			#not connected with previous path
			else:
				write_coor_file(previous_data, 'NULL')
				previous_data = data
		else:
			write_coor_file(previous_data, previous_data.iloc[0]['callsign'])
			previous_data = data
	'''
	if(len(data)>0):
		#connected with previous path
		if (abs(data.iloc[0]['lat']-previous_data.iloc[-1]['lat'])<0.01) & (abs(data.iloc[0]['lon']-previous_data.iloc[-1]['lon'])<0.01):
			previous_data = previous_data.append(data, ignore_index=True)
			if (callsign!='NULL'):
				previous_callsign = callsign
		#not connected
		else:
			#save previous path
			if(len(previous_data)>0):
				write_coor_file(previous_data, previous_callsign)
			#put this path into previous_data
			previous_data = data
			previous_callsign = callsign
	
	'''
	coor=data.loc[:,['lat','lon','geoaltitude']]
	coor=coor.dropna(how='any')
	coor=coor.drop_duplicates()
	
	if (len(coor)>0):
		write_coor_file(coor, callsign)
	'''
file.close()