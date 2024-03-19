import sqlite3

db = sqlite3.connect('filter.db')

query = '''
CREATE TABLE "MRT" (
	"StationID"	TEXT NOT NULL,
	"StationName"	TEXT NOT NULL,
	PRIMARY KEY("StationID")
);
'''

db.execute(query)
db.commit()

query = '''
CREATE TABLE "Place" (
	"PlaceID"	INTEGER NOT NULL,
	"PlaceName"	TEXT NOT NULL,
	"PlaceLocation"	TEXT NOT NULL,
	"StationName"	TEXT NOT NULL,
	"PlaceType"	TEXT NOT NULL CHECK("PlaceType" = 'Bar' OR "PlaceType" = 'Cafe' OR "PlaceType" = 'CasualDining' OR "PlaceType" = 'FancyDining' OR "PlaceType" = 'FoodStall'),
	FOREIGN KEY("StationName") REFERENCES "MRT"("StationName"),
	PRIMARY KEY("PlaceID" AUTOINCREMENT)
);
'''

db.execute(query)
db.commit()
db.close()