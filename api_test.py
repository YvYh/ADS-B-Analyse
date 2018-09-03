from opensky_api import OpenSkyApi

api = OpenSkyApi()
zbaa = (36.0448, 44.0448, 112.3504, 120.3504)
states = api.get_states(bbox=zbaa)
print("Time{}\n".format(states.time))
for s in states.states:
	print("(\t%r\t%r\t%r)" %(s.callsign, s.longitude, s.latitude))
