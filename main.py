import webapp2
import jinja2
import os
from google.appengine.ext import db
from google.appengine.api import users

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



# DOM

class BusUpdates(db.Model):
	user = db.StringProperty()
	bus = db.StringProperty(required=True)
	entry = db.StringProperty()
	created = db.DateTimeProperty(auto_now_add=True)

	def as_dict(self):
		time_format = '%c'
		d = {'user' : self.user, 'bus': self.bus, 'time': self.created.strftime(time_format) }
		return json.dumps(d)




federated = {
    'Google'   : 'https://www.google.com/accounts/o8/id',
    'Yahoo'    : 'http://www.yahoo.com',
    'Myspace'  : 'http://www.myspace.com',
    'AOL'      : 'http://www.aol.com',
    'MyOpenID' : 'http://www.myopenid.com'

}


new_providers = {}
for i in federated.keys():
	new_providers[i] = users.create_login_url(federated_identity=federated[i])


class ChoicePage(Handler):
	def get(self):
		user = users.get_current_user().nickname()
		if user:
			self.render("choicepage.html", user=user, new_providers=new_providers)
		else:
			self.render("choicepage.html", new_providers=new_providers)

update_type = None


class UpdatesPage(Handler):
	def render_all(self, update_type="", bus="", entry="", error=""):
		bus_info = BusUpdates.all().order('-created')
		self.render("update.html", update_type=update_type, bus=bus, entry=entry, error=error, bus_info=bus_info)
		
	update_type = None
	def get_update(self):
		riders = self.request.get("riding")
		waiters = self.request.get("waiting")
		if riders:
			self.update_type = riders
		if waiters:
			self.update_type = waiters
	

	def get(self):
		self.get_update()
		update_type = self.update_type
		self.render_all(update_type=update_type)

	def post(self):
		self.get_update()
		update_type = self.update_type
		user = users.get_current_user().nickname()
		if not user:
			user = "guest"
		bus = self.request.get("bus")
		entry = self.request.get("entry")
		if bus:
			b = BusUpdates(bus=bus)
			b.user = user
			b.entry = entry
			b.put()
			self.render_all(update_type=update_type)
	
		else:
			error = "We need a bus number to proceed."
			self.render_all(update_type=update_type, error=error, bus=bus, entry=entry)




app = webapp2.WSGIApplication([('/', ChoicePage), ('/updates', UpdatesPage)], debug=True)












