import webapp2
import jinja2
import os
import json
import random
import time
from time import strftime
from datetime import datetime
import urllib2
import logging
from get_route import get_locations, get_cared_about, find_times2, get_doc, get_title_locations, generate_routes2, get_future_data, mb_api
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import memcache

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)


Buses = {'Des Moines, IA': '106', 'Milwaukee, WI': '121', 'Frederick, MD': '109', 'Minnesota': '23', 'Illinois': '13', 'Chattanooga, TN': '290', 'Indiana': '14', 'Louisiana': '18', 'Texas': '43', 'Giddings, TX': '401', 'Galveston, TX': '325', 'Dallas/Fort Worth, TX': '317', 'Knoxville, TN': '118', 'New Brunswick, NJ': '305', 'Connecticut': '7', 'Rochester, NY': '134', 'Atlanta, GA': '289', 'West Virginia': '48', 'Texarkana, AR': '407', 'La Grange, TX': '333', 'Ridgewood, NJ': '133', 'Kansas City, MO': '117', 'El Paso, TX': '397', 'Harrisburg, PA': '111', 'Big Spring, TX': '393', 'East Lansing, MI': '330', 'Toronto, ON': '145', 'Missouri': '25', 'South Bend, IN': '368', 'Fairhaven, MA': '316', 'Kenton, OH': '362', 'Carthage, TX': '395', 'New Jersey': '30', 'Valparaiso, IN': '376', 'Gainesville, FL': '296', 'Iowa City, IA': '116', 'Lufkin, TX': '404', 'Houston, TX': '318', 'San Antonio, TX': '321', 'Eagle Pass, TX': '327', 'Shreveport, LA': '332', 'Maryland': '20', 'Oklahoma City, OK': '323', 'Wisconsin': '49', 'Syracuse, NY': '139', 'Michigan': '22', 'Del Rio, TX': '328', 'New York': '32', 'Massachusetts': '21', 'Mobile, AL': '294', 'Richmond, IN': '371', 'Boston, MA': '94', 'Florida': '10', 'Rhode Island': '39', 'Sparks, NV': '419', 'Nashville , TN': '291', 'Memphis, TN': '120', 'Livingston, TX': '402', 'Ohio': '35', 'State College, PA': '137', 'Burlington, VT': '96', 'North Carolina': '33', 'Athens, GA': '302', 'District of Columbia': '9', 'Birmingham, AL': '292', 'Van Wert, OH': '364', 'Elkhart, IN': '367', 'Maine': '19', 'Christiansburg, VA': '101', 'Ontario': '51', 'Detroit, MI': '107', 'Norman, OK': '322', 'Oklahoma': '36', 'Delaware': '8', 'Champaign, IL': '98', 'Madison, U of Wisc, WI': '300', 'La Marque, TX': '337', 'Arkansas': '4', 'Humble, TX': '334', 'New Haven, CT': '122', 'Secaucus, NJ': '135', 'Indianapolis, IN': '115', 'Newark, DE': '389', 'Lima, OH': '363', 'Sacramento, CA': '415', 'Durham, NC': '131', 'Midland, TX': '405', 'Pittsburgh, PA': '128', 'Washington, DC': '142', 'California': '5', 'Uvalde, TX': '326', 'Providence, RI': '130', 'Georgia': '11', 'Columbia City, IN': '373', 'San Jose, CA': '412', 'Pennsylvania': '38', 'San Francisco, CA': '414', 'Toledo, OH': '140', 'Montgomery, AL': '293', 'Hampton, VA': '110', 'Philadelphia, PA': '127', 'Nacogdoches, TX': '406', 'Riverside, CA': '416', 'Louisville, KY': '298', 'Buffalo Airport, NY': '273', 'Little Rock, AR': '324', 'Ft. Wayne, IN': '365', 'Columbus, OH': '105', 'Dayton-Trotwood, OH': '370', 'Hartford, CT': '112', 'Cincinnati, OH': '102', 'Storrs, CT': '138', 'Buffalo, NY': '95', 'Brenham, TX': '335', 'Nevada': '28', 'Ann Arbor, MI': '91', 'Omaha, NE': '126', 'Cleveland, OH': '103', 'Charlotte, NC': '99', 'Madison, WI': '119', 'Princeton, NJ': '304', 'St Louis, MO': '136', 'Springfield, MO': '411', 'New York, NY': '123', 'Lubbock, TX': '403', 'San Angelo, TX': '329', 'Richmond, VA': '132', 'Baltimore, MD': '143', 'Albany, NY': '89', 'Minneapolis, MN': '144', 'Virginia': '46', 'Las Vegas, NV': '417', 'Binghamton, NY': '93', 'Oakland, CA': '413', 'Los Angeles, CA': '390', 'Austin, TX': '320', 'Vermont': '45', 'Grand Rapids, MI': '331', 'Warsaw, IN': '374', 'Columbia, MO': '104', 'Kentucky': '17', 'Morgantown, WV': '299', 'Nebraska': '27', 'New Orleans, LA': '303', 'Iowa': '15', 'Alabama': '53', 'Angola, IN': '366', 'Prairie View, TX': '336', 'Abilene, TX': '391', 'Chicago, IL': '100', 'Plymouth, IN': '375', 'Jacksonville, FL': '295', 'Tennessee': '42', 'Gary, IN': '369', 'Amherst, MA': '90', 'Portland, ME': '129', 'Muncie, IN': '372', 'Orlando, FL': '297', 'Saratoga Springs, NY': '301'}


# this section is for running a query to megabus once a day to get the new day + 2 weeks of data

JSON_LIB = {}
month = [32, 29, 32, 31, 32, 31, 32, 32, 31, 32, 31, 32]
months = [[e for e in range(1,i)] for i in month]
url = "new_cities.xml"
xml = get_doc(url)
locations = get_title_locations(xml)
routes = generate_routes2(xml, locations)
def run_once_a_day():
	start = time.time()
	for i in routes.keys():
		for e in routes[i]:
			get_future_data(mb_api, i, e, months, JSON_LIB)
	stop = time.time()
	time.sleep(86400-(stop-start))
while True:
	run_once_a_day()




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
	#time = db.StringProperty(required=True)
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




def top_bus(update=False):
	key = 'top'
	bus_info = memcache.get(key)
	if bus_info is None or update:
		global queried
		queried = int(time.time())
		logging.error("DATABASE QUERY")
		bus_info = BusUpdates.all().order('-timestamp').fetch(limit=50)
		memcache.set(key, bus_info)
	return bus_info




class UpdatesPage(Handler):
	def render_all(self, update_type="", bus="", entry="", url="",error="", user="", bus_info="", data=""):
		#bus_info = top_bus()
		
		self.render("update.html", update_type=update_type, bus=bus, entry=entry, error=error, bus_info=bus_info, url=url, user=user, data=data)
	# new render_all for data mining implement

		
	
	def get_update(self):
		global update_type
		riders = self.request.get("riding")
		waiters = self.request.get("waiting")
		if riders:
			update_type = "riding"
		if waiters:
			update_type = "waiting"
	
	def generate_some_json(self,s):
		return json.dumps(s)



	
	def get(self):
		bus_info = top_bus()
		#data = self.generate_some_json({'St Louis, MO-Chicago, IL-2-26': ['600AM-100PM', '1200PM-530PM', '500PM-1050PM']})
		data = self.generate_some_json(JSON_LIB)
		self.get_update()
		name = users.get_current_user()
		user = None
		if name:
			user = name.nickname()
		tmp = self.request.url
		posit = tmp.find('updates')
		url = tmp[0:posit+7]+'/'
		if self.format == 'json':
			self.render_json([b.as_dict() for b in bus_info])
		else:
			self.render_all(update_type=update_type, url=url, user=user, bus_info=bus_info, data=data)
			

	def post(self):
		
		self.get_update()
		user = 'guest'
		if users.get_current_user():
			user = users.get_current_user().nickname()
		day = str(int(strftime('%d')))
		month = strftime('%m')
		departure = self.request.get("departure")
		arrival = self.request.get("arrival")
		times = self.request.get("times")
		bus = departure + '-' + arrival + '-' + month + '-' + day + '-' + times 
		entry = self.request.get("entry")
		latitude = self.request.get("latitude")
		longitude = self.request.get("longitude")
		map_api = "http://maps.googleapis.com/maps/api/staticmap?center={0},{1}&zoom=9&size={2}x{3}&maptype=roadmap&markers=color:blue%7Clabel:M%7C{0},{1}&sensor=false"
		time_api_key = '8c0af75047193432130502'
		time_api_if_coords = 'http://www.worldweatheronline.com/feed/tz.ashx?key={0}&q={1},{2}&format=xml'
		time_api_if_not_coords = 'http://www.worldweatheronline.com/feed/tz.ashx?key={0}&q={1}&format=xml'
		
		if bus[0:4] != 'City':
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
			error = "You must select some real data."
			# these three lines are necessary otherwise when a user clicks a url after getting
			# the error message we will be redirected to a nonexistent page and get a 404
			tmp = self.request.url
                	posit = tmp.find('updates')
                	url = tmp[0: posit+ 7] + '/'
			bus_info = top_bus()
			self.render_all(update_type=update_type, error=error, bus=bus, url=url, entry=entry, user=user, bus_info=bus_info)




class IndividualBus(Handler):
	def get(self):
		url_u = str(self.request.url)
		posit = url_u.find('updates')
		bus1 = url_u[posit+8:]
	        bus = bus1.replace('%20', chr(32))	
		b = BusUpdates.all()
		this_bus = b.order('-timestamp').filter('bus = ', bus).fetch(limit=10)
	
		self.render("individual_bus.html", bus=bus, this_bus=this_bus)
		#if self.format == 'html':	
		#	if this_bus:
		#		self.render("individual_bus.html", bus=bus, this_bus=this_bus)
		#	else:
		#		self.write("There is a freaking error!")		
		#else:
		#	self.render_json([j.as_dict() for j in this_bus])






app = webapp2.WSGIApplication([('/', ChoicePage),
			       ('/updates(?:.json)?', UpdatesPage),
			       ('/updates/.*', IndividualBus)], debug=True) 
			       #('/updates/([a-zA-Z]{1}[0-9]+)(?:.json)?', IndividualBus)],
			       #debug=True)












