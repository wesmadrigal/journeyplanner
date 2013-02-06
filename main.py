import webapp2
import jinja2
import os
import json
import random
import time
from datetime import datetime
import Cookie
import urllib2
import logging
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import memcache

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)




class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))


	def render_json(self, d):
		json_text = json.dumps(d)
		self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
		self.write(json_text)

	def initialize(self, *a, **kw):
		webapp2.RequestHandler.initialize(self, *a, **kw)
		if self.request.url.endswith('.json'):
			self.format = 'json'
		else:
			self.format = 'html'





class BusUpdates(db.Model):
	user = db.StringProperty()
	bus = db.StringProperty(required=True)
	entry = db.TextProperty()
	latitude = db.StringProperty()
	longitude = db.StringProperty()
	user_map = db.LinkProperty()
	user_api_link = db.LinkProperty()
	created = db.StringProperty()
	timestamp = db.DateTimeProperty(auto_now_add=True)	

	def as_dict(self):
		time_format = '%c'
		d = {'user' : self.user, 'bus': self.bus, 'entry': self.entry, 'lat': self.latitude, 'long': self.longitude, 'time': self.created.strftime(time_format) }
		return json.dumps(d)




federated = {
    'Google'   : 'https://www.google.com/accounts/o8/id',
    'AOL'      : 'aol.com',
    'Yahoo'    : 'yahoo.com',
    'MyOpenID' : 'myopenid.com'

}


new_providers = {}
for i in federated.keys():
	new_providers[i] = users.create_login_url(federated_identity=federated[i])


class ChoicePage(Handler):
	def get(self):
		user = users.get_current_user()
		logout_url = users.create_logout_url(self.request.uri)
		try:
			self.render("choicepage.html", user=user, new_providers=new_providers, logout_url=logout_url)
		except:
			logging.error("Home page render error")
	

update_type = None



# caching the database queries

def top_bus(update=False):
	key = 'top'
	bus_info = memcache.get(key)
	if bus_info is None or update:
		global queried
		queried = int(time.time())
		logging.error("DATABASE QUERY")
		bus_info = BusUpdates.all().order('-timestamp').fetch(limit=10)
		memcache.set(key, bus_info)
	return bus_info




class UpdatesPage(Handler):
	def render_all(self, update_type="", bus="", entry="", url="",error="", user="", bus_info=""):
		#bus_info = top_bus()
		
		self.render("update.html", update_type=update_type, bus=bus, entry=entry, error=error, bus_info=bus_info, url=url, user=user)
		
	
	def get_update(self):
		global update_type
		riders = self.request.get("riding")
		waiters = self.request.get("waiting")
		if riders:
			update_type = "riding"
		if waiters:
			update_type = "waiting"
	

	def get(self):
		# elminiate db query and call cache
		bus_info = top_bus()
		self.get_update()
		name = users.get_current_user()
		user = None
		if name:
			user = name.nickname()
		tmp = self.request.url
		posit = tmp.find('updates')
		url = tmp[0: posit+ 7] + '/'
		if self.format == 'json':
			self.render_json([b.as_dict() for b in buses])
		else:
			self.render_all(update_type=update_type, url=url, user=user, bus_info=bus_info)
	

	def post(self):
		
		self.get_update()
		user = 'guest'
		if users.get_current_user():
			user = users.get_current_user().nickname()

		bus = self.request.get("bus")
		entry = self.request.get("entry")
		latitude = self.request.get("latitude")
		longitude = self.request.get("longitude")
		map_api = "http://maps.googleapis.com/maps/api/staticmap?center={0},{1}&zoom=9&size={2}x{3}&maptype=roadmap&markers=color:blue%7Clabel:M%7C{0},{1}&sensor=false"
		time_api_key = '8c0af75047193432130502'
		time_api_if_coords = 'http://www.worldweatheronline.com/feed/tz.ashx?key={0}&q={1},{2}&format=xml'
		time_api_if_not_coords = 'http://www.worldweatheronline.com/feed/tz.ashx?key={0}&q={1}&format=xml'
		
		if bus:
			b = BusUpdates(bus=bus)
			b.user = user
			b.entry = entry
			if latitude and longitude:
				b.latitude = latitude
				b.longitude = longitude
				b.user_map = map_api.format(latitude, longitude, '300', '300')
				b.user_api_link = map_api.format(latitude,longitude, '900', '900')
				time_url = urllib2.urlopen(time_api_if_coords.format(time_api_key, latitude, longitude)).read()
				start = time_url.find('<localtime>') + 11
				end = time_url.find('</localtime>')
				b.created = time_url[start:end]
				# generate the map_api image
				#map_url = map_api.format(latitude,longitude)
				#posit = map_url.find('size')
				#b.user_api_link = map_url[0: (posit + 4)] + '900x900' + map_url[(posit + 12): ]

			else:
				def assign():
					f = urllib2.urlopen(time_api_if_not_coords.format(time_api_key, self.request.remote_addr)).read()
					start = f.find('<localtime>') + 11
					end = f.find('</localtime>')
					if start:
						return f[start:end]
					else:
						return '0:0:0:0'
				b.latitude = None
				b.longitude = None
				b.created = assign()

			b.put()
			top_bus(True)		
	
			self.redirect('/updates/%s' % str(b.bus))
	
		else:
			error = "We need a bus number to proceed."
			# these three lines are necessary otherwise when a user clicks a url after getting
			# the error message we will be redirected to a nonexistent page and get a 404
			tmp = self.request.url
                	posit = tmp.find('updates')
                	url = tmp[0: posit+ 7] + '/'

			self.render_all(update_type=update_type, error=error, bus=bus, url=url, entry=entry, user=user)




class IndividualBus(Handler):
	def get(self, bus_id):
		url_u = str(self.request.url)
		length = len(url_u)
		posit = url_u.find('updates')
		bus = url_u[posit+8:]
		
		b = BusUpdates.all()
		this_bus = b.order('-timestamp').filter('bus = ', bus).fetch(limit=10)
	

		if self.format == 'html':	
			if this_bus:
				self.render("individual_bus.html", bus=bus, this_bus=this_bus)
			else:
				self.write("There is a freaking error!")		
		else:
			self.render_json([j.as_dict() for j in this_bus])






app = webapp2.WSGIApplication([('/', ChoicePage),
			       ('/updates(?:.json)?', UpdatesPage), 
			       ('/updates/([a-zA-Z]{1}[0-9]+)(?:.json)?', IndividualBus)],
			       debug=True)












