CREATE TABLE "MRT" (
	"StationID"	TEXT NOT NULL,
	"StationName"	TEXT NOT NULL,
	PRIMARY KEY("StationID")
);

CREATE TABLE "Place" (
	"PlaceID"	INTEGER NOT NULL,
	"PlaceName"	TEXT NOT NULL,
	"PlaceLocation"	TEXT NOT NULL,
	"StationName"	TEXT NOT NULL,
	"PlaceType"	TEXT NOT NULL CHECK("PlaceType" = 'Bar' OR "PlaceType" = 'Cafe' OR "PlaceType" = 'CasualDining' OR "PlaceType" = 'FancyDining' OR "PlaceType" = 'FoodStall'),
	PRIMARY KEY("PlaceID" AUTOINCREMENT),
	FOREIGN KEY("StationName") REFERENCES "MRT"("StationName")
);