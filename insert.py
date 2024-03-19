import sqlite3

db = sqlite3.connect('filter.db')

#read file and data for mrt
file = open('mrt.txt')
data = file.readlines()
station = []
file.close()

for i in data:
    station.append(i.strip().split(','))

#insert data
query = '''
INSERT INTO MRT(StationID, StationName)
VALUES(?,?)
'''

for i in station:
    db.execute(query,(i[0],i[1]))
    db.commit()

#read file and data for places
file = open('places.txt', encoding="utf8")
data = file.readlines()
places = []
file.close()

for i in data:
    places.append(i.strip().split(','))

#insert data
query = '''
INSERT INTO Place(PlaceName, PlaceLocation, StationName, PlaceType)
VALUES(?,?,?,?)
'''

for i in places:
    db.execute(query,(i[0],i[1],i[2],i[3]))
    db.commit()

db.close()