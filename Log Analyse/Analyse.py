import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def transferData(filename):
    # get column name
    file = open(filename, 'r')
    line = file.readlines(1500)
    file.close()
    col = [x.strip(' ') for x in [i.split('|') for i in line[-2:-1]][0]]
    col = col[:-1]
    sub_data = pd.read_csv(filename, sep= '|',
                       names=col, 
                       skiprows=11, 
                       index_col=False, 
                       skipinitialspace=True,  
                       na_values=['NULL','NULL     ','spi   ','alert ','onground '], 
                       false_values=['false    ','false ','false ','false    '],
                       true_values=['true  ','true     ','true  '],
                       iterator=True,
                       chunksize=1000
                      )
    data=pd.concat(sub_data)
    data = data.iloc[:-6,1:]
    for name in ['lat', 'lon','velocity','heading','vertrate','baroaltitude','geoaltitude','lastposupdate','lastcontact']:
        data[name] = pd.to_numeric(data[name], errors='coerce')
    return data
	
def itinerary(data):
    fig = plt.figure()
    ax = Axes3D(fig)
    data = data.dropna(how='any')
    ax.plot(data.lat, data.lon, data.geoaltitude, c='r')
    ax.bar3d(data.lat, data.lon, data.geoaltitude, 0.01, 0.01,data.vertrate*110, shade=False, label='vertrate')
    ax.set_xlabel('latitude')
    ax.set_ylabel('longitude')
    ax.set_zlabel('altitude')
    plt.savefig('itinerary.jpg')
	
def write_coor(data):
	coor=data.loc[:,['lat','lon','geoaltitude']]
	coor=coor.dropna(how='any')
	coor.to_csv('../../Thales/coor.csv', index=False)
	
data=transferData('../../Thales/log.txt')
#itinerary(data)
write_coor(data)