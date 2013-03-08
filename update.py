from google.appengine.api import mail
import logging
import webapp2
#from main import BusData
from get_route import update_data2
from megabus_times_library import library
from get_route import get_doc, get_title_locations, generate_routes2, mb_api, months
from google.appengine.ext import db

class DataMain(webapp2.RequestHandler):
	def get(self):
		xml = get_doc("new_cities.xml")
		locs = get_title_locations(xml)
		routes = generate_routes2(xml, locs)
		logging.info("cron started")
		update_data2(routes, mb_api, months)
		logging.info("cron finished")

app = webapp2.WSGIApplication([('/update_bus_data', DataMain)], debug=True)

