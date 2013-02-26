# this file contains the data models used, specifically

class BusUpdates(db.Model):
	user = db.StringProperty()
	departure = db.StringProperty()
	arrival = db.StringProperty()
	trip_time = db.StringProperty()
	entry = db.StringProperty()
	latitude = db.StringProperty()
	longitude = db.StringProperty()
	user_map_small = db.LinkProperty()
	user_map_big = db.LinkProperty()
	created = db.StringProperty() # using the api I found
	timestamp = db.DateTimeProperty()


class Route(db.Model):
	departure = db.StringProperty()
	arrival = db.StringProperty()


class SpecificTimes(db.Model):
	route_id = db.ReferenceProperty(Route, collection_name = 'times')
	month = db.IntegerProperty()
	day = db.IntegerProperty()
	time = db.StringProperty()



