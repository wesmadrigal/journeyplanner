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
import mechanize
import cookielib
from get_route import make_or_get_day2, update_data, get_data_from_future
from get_route import get_future_data2test, months
from get_route import get_locations, get_cared_about, find_times2, get_doc, get_title_locations, generate_routes2, get_future_data, mb_api, update_data2
from trip_planner import *
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import memcache
from google.appengine.api import mail

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True, extensions=['jinja2.ext.autoescape'])


#Buses = {'Des Moines, IA': '106', 'Milwaukee, WI': '121', 'Frederick, MD': '109', 'Minnesota': '23', 'Illinois': '13', 'Chattanooga, TN': '290', 'Indiana': '14', 'Louisiana': '18', 'Texas': '43', 'Giddings, TX': '401', 'Galveston, TX': '325', 'Dallas/Fort Worth, TX': '317', 'Knoxville, TN': '118', 'New Brunswick, NJ': '305', 'Connecticut': '7', 'Rochester, NY': '134', 'Atlanta, GA': '289', 'West Virginia': '48', 'Texarkana, AR': '407', 'La Grange, TX': '333', 'Ridgewood, NJ': '133', 'Kansas City, MO': '117', 'El Paso, TX': '397', 'Harrisburg, PA': '111', 'Big Spring, TX': '393', 'East Lansing, MI': '330', 'Toronto, ON': '145', 'Missouri': '25', 'South Bend, IN': '368', 'Fairhaven, MA': '316', 'Kenton, OH': '362', 'Carthage, TX': '395', 'New Jersey': '30', 'Valparaiso, IN': '376', 'Gainesville, FL': '296', 'Iowa City, IA': '116', 'Lufkin, TX': '404', 'Houston, TX': '318', 'San Antonio, TX': '321', 'Eagle Pass, TX': '327', 'Shreveport, LA': '332', 'Maryland': '20', 'Oklahoma City, OK': '323', 'Wisconsin': '49', 'Syracuse, NY': '139', 'Michigan': '22', 'Del Rio, TX': '328', 'New York': '32', 'Massachusetts': '21', 'Mobile, AL': '294', 'Richmond, IN': '371', 'Boston, MA': '94', 'Florida': '10', 'Rhode Island': '39', 'Sparks, NV': '419', 'Memphis, TN': '120', 'Livingston, TX': '402', 'Ohio': '35', 'State College, PA': '137', 'Burlington, VT': '96', 'North Carolina': '33', 'Nashville , TN': '291', 'Athens, GA': '302', 'District of Columbia': '9', 'Birmingham, AL': '292', 'Van Wert, OH': '364', 'Elkhart, IN': '367', 'Maine': '19', 'Christiansburg, VA': '101', 'Ontario': '51', 'Detroit, MI': '107', 'Norman, OK': '322', 'Oklahoma': '36', 'Delaware': '8', 'Champaign, IL': '98', 'Madison, U of Wisc, WI': '300', 'La Marque, TX': '337', 'Arkansas': '4', 'Humble, TX': '334', 'New Haven, CT': '122', 'Secaucus, NJ': '135', 'Indianapolis, IN': '115', 'Newark, DE': '389', 'Lima, OH': '363', 'Sacramento, CA': '415', 'Durham, NC': '131', 'Midland, TX': '405', 'Pittsburgh, PA': '128', 'Washington, DC': '142', 'California': '5', 'Uvalde, TX': '326', 'Providence, RI': '130', 'Georgia': '11', 'Columbia City, IN': '373', 'San Jose, CA': '412', 'Pennsylvania': '38', 'San Francisco, CA': '414', 'Toledo, OH': '140', 'Montgomery, AL': '293', 'Hampton, VA': '110', 'Philadelphia, PA': '127', 'Nacogdoches, TX': '406', 'Riverside, CA': '416', 'Louisville, KY': '298', 'Buffalo Airport, NY': '273', 'Little Rock, AR': '324', 'Ft. Wayne, IN': '365', 'Columbus, OH': '105', 'Dayton-Trotwood, OH': '370', 'Hartford, CT': '112', 'Cincinnati, OH': '102', 'Storrs, CT': '138', 'Buffalo, NY': '95', 'Brenham, TX': '335', 'Nevada': '28', 'Ann Arbor, MI': '91', 'Omaha, NE': '126', 'Cleveland, OH': '103', 'Charlotte, NC': '99', 'Madison, WI': '119', 'Princeton, NJ': '304', 'St Louis, MO': '136', 'Springfield, MO': '411', 'New York, NY': '123', 'Lubbock, TX': '403', 'San Angelo, TX': '329', 'Richmond, VA': '132', 'Baltimore, MD': '143', 'Albany, NY': '89', 'Minneapolis, MN': '144', 'Virginia': '46', 'Las Vegas, NV': '417', 'Binghamton, NY': '93', 'Oakland, CA': '413', 'Los Angeles, CA': '390', 'Austin, TX': '320', 'Vermont': '45', 'Grand Rapids, MI': '331', 'Warsaw, IN': '374', 'Columbia, MO': '104', 'Kentucky': '17', 'Morgantown, WV': '299', 'Nebraska': '27', 'New Orleans, LA': '303', 'Iowa': '15', 'Alabama': '53', 'Angola, IN': '366', 'Prairie View, TX': '336', 'Abilene, TX': '391', 'Chicago, IL': '100', 'Plymouth, IN': '375', 'Jacksonville, FL': '295', 'Tennessee': '42', 'Gary, IN': '369', 'Amherst, MA': '90', 'Portland, ME': '129', 'Muncie, IN': '372', 'Orlando, FL': '297', 'Saratoga Springs, NY': '301', 'Erie, PA': '108', 'Minneapolis/St. Paul, MN': '430'}


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
	


federated = {
    'Google'   : 'https://www.google.com/accounts/o8/id',
    'AOL'      : 'aol.com',
    'Yahoo'    : 'yahoo.com',
    'MyOpenID' : 'myopenid.com'

}




new_providers = {}
for i in federated.keys():
	new_providers[i] = users.create_login_url(federated_identity=federated[i])


class LoginPage(Handler):
        def get(self):
                user = users.get_current_user()
                self.render("loginpage.html", new_providers = new_providers)


class TripStuff(db.Model):
	ipid = db.StringProperty(required = True)
	query = db.TextProperty()
	created = db.DateTimeProperty(auto_now_add=True)


class PlanTrip(Handler):
	def get(self):
		self.render("plan_trip.html")
	
	def post(self):
		u = users.get_current_user()
		user = None
		if u:
			user = u.nickname()
		logout = users.create_logout_url(self.request.uri)
		if not self.request.get("trips"):
			xml = get_doc("new_cities.xml")
			locs = get_title_locations(xml)
			routes = generate_routes2(xml, locs)
			dep = self.request.get("start")
			end = self.request.get("end")
			date = self.request.get("date")
			if len(date) > 0:
				month = str(int(date[0:date.find('/')]))
				day = str(int(date[date.find('/')+1:date.find('/',date.find('/')+1)]))
			if dep != 'City, State' and end != 'City, State' and len(date) >= 1 and dep in routes.keys() and end in routes.keys() and dep != end:
				try:
					trip = plan_trip(dep, end, routes)
					trip_options, trip_times, trip_links = make_formatted3(trip, month, day)
					response = generate_response3(trip_options, trip_times, trip_links, dep, end)
				except:
					response = '<p style="color:red"><b>The requested route is impossible with megabus.</b></p>'
				self.render("plan_trip.html", response=response, user=user, logout=logout)		
			else:		
				error = 'You must choose a valid departure city, arrival city, and a day of departure.'
				self.render("plan_trip.html", user=user, logout=logout, error=error)
		else:
			ip = self.request.remote_addr
			query_string = self.request.get("trips")
			ts = TripStuff(ipid = ip)
			ts.query = query_string
			ts.put()
			logging.info("Posted query string to database")
			self.redirect('/mytrips')
			
			


class Basket(Handler):	
	def setup_browser(self):
		self.br = mechanize.Browser()	
		self.cj = cookielib.LWPCookieJar()
        	self.br.set_cookiejar(self.cj)
        	self.br.addheaders = [('User-Agent', 'Mozilla/5.0(X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        	self.br.set_debug_http(True)
	        self.br.set_debug_redirects(True)
	        self.br.set_debug_responses(True)
	        self.br.set_handle_robots(False)
        	self.br.set_handle_equiv(True)
        	self.br.set_handle_gzip(True)
        	self.br.set_handle_redirect(True)
	
	def get(self):
		self.setup_browser()
		ip = self.request.remote_addr
		ts = TripStuff.all().filter('ipid = ', ip).order('-created').fetch(limit=1)
		# put the string value in a list and grab it
		string = [i.query for i in ts]
		proper = string[0].encode('utf-8')	

		# generate a dictionary for the emulated browser to parse through adding trips to basket
		the_dict = decipher_query(proper)

		# return the ViewBasket.aspx page with all trips added
		#basket_response = get_trips_in_basket(the_dict)
		#br = Basket.br
		basket_response = get_trips_in_basket2(the_dict, self.br)

		# scrape all the necessary data from the returned response
		journey_dict, total_price = get_journey_info(basket_response)

		# passing a json string to the frontend containing the necessary values to make cookies with in our post
		# we need this to preserve users
		cookie_dict = self.cj._cookies
		new_dict = {}
		d = 'us.megabus.com'
		p = '/'
		for i in cookie_dict[d][p].keys():
    			new_dict[i] = [cookie_dict[d][p][i].version, cookie_dict[d][p][i].name, cookie_dict[d][p][i].value, cookie_dict[d][p][i].port, cookie_dict[d][p][i].port_specified, cookie_dict[d][p][i].domain, cookie_dict[d][p][i].domain_specified, cookie_dict[d][p][i].domain_initial_dot, cookie_dict[d][p][i].path, cookie_dict[d][p][i].path_specified, cookie_dict[d][p][i].secure, cookie_dict[d][p][i].expires, cookie_dict[d][p][i].discard, cookie_dict[d][p][i].comment, cookie_dict[d][p][i].comment_url, cookie_dict[d][p][i]._rest, cookie_dict[d][p][i].rfc2109]

		string_cookies = json.dumps(new_dict)
		self.render("mytrips.html", journey_dict = journey_dict, total_price = total_price, string_cookies = string_cookies)


	def post(self):
		self.setup_browser()

		# decipher the cookie_dict string with json and make some cookies!
		cookie_str = self.request.get("cookie_dict")		
		cookie_dict = json.loads(cookie_str)
		for key in cookie_dict.keys():
			current_cookie = cookielib.Cookie(version=cookie_dict[key][0], name=cookie_dict[key][1], value=cookie_dict[key][2], port=cookie_dict[key][3], port_specified=cookie_dict[key][4], domain=cookie_dict[key][5], domain_specified=cookie_dict[key][6], domain_initial_dot=cookie_dict[key][7], path=cookie_dict[key][8], path_specified=cookie_dict[key][9], secure=cookie_dict[key][10], expires=cookie_dict[key][11], discard=cookie_dict[key][12], comment=cookie_dict[key][13], comment_url=cookie_dict[key][14], rest=cookie_dict[key][15], rfc2109=cookie_dict[key][16])

			self.cj.set_cookie(current_cookie)		

		agree = self.request.get('agree')
		if agree:
			self.br.open('http://us.megabus.com/ViewBasket.aspx')
			self.br.select_form(nr=0)
			self.br.set_all_readonly(False)
			self.br.find_control('BasketView$cbTerms').items[0].selected = True
			self.br.form['__EVENTTARGET'] = 'BasketView$btnPay'
			self.br.submit(name='BasketView$btnPay')
			self.write(self.br.response().read())		
		else:
			self.redirect('/mytrips')

	

class AboutMe(Handler):
	def get(self):
		user = users.get_current_user()
		user_email = None
		if user:
			user_email = user.email()
		logout = users.create_logout_url(self.request.uri)
		self.render("aboutme.html", user=user, logout=logout,user_email=user_email)

	def post(self):
		user = users.get_current_user().nickname()
		logout = users.create_logout_url(self.request.uri)
		subject = self.request.get("subject")
		content = self.request.get("content")
		user_email = users.get_current_user().email()
		if len(subject) < 1 and len(content) < 1:
			error = 'Must have a subject and content'
			self.render("aboutme.html", user=user, logout=logout, user_email=user_email, error=error)
		else:
			message = mail.EmailMessage(sender = user_email, subject=subject)
			message.to = 'wesley7879@gmail.com'
			app_identifier = '\nSent from a user through Megabusfinder.\n'
			message.body = content + app_identifier
			message.send()
			message_sent = 'Your message was sent to the administrator.'
			self.render("aboutme.html", user=user, logout=logout, user_email=user_email, message_sent=message_sent)


app = webapp2.WSGIApplication([('/', PlanTrip),
			       ('/mytrips', Basket),
			       ('/login', LoginPage),
			       ('/aboutme', AboutMe)],
			       debug=True)


