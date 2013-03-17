#!/usr/bin/env python

from megabus_times_library import library
from get_route import *
from trip_planner import *
from time import strftime
import os


def main():
	xml = get_doc("new_cities.xml")
	locs = get_title_locations(xml)
	routes = generate_routes2(xml, locs)
	today = str(int(strftime('%d')))
	month = str(int(strftime('%m')))
	new_lib = library
	#os.remove("megabus_times_library.py")
	for i in new_lib.keys():
		sec_hyph = i.find('-', i.find('-')+1)
		third_hyph = i.find('-', sec_hyph + 1)
		m = i[sec_hyph+1:third_hyph]
		d = i[third_hyph+1:]
		if not m or not d:
			del new_lib[i]
		if int(m) < int(month):
			del new_lib[i]
		elif int(m) == int(month):
			if int(d) < int(today):
				del new_lib[i]
	for from_c in routes.keys():
		for to_c in routes[from_c]:
			get_future_data(mb_api, from_c, to_c, month, int(today)+1, months, new_lib)
	f = open("megabus_times_library.py", "w")
	f.write("library = %s" % new_lib)
	print 'Finished updating megabus_times_library'




if __name__ == '__main__':
	main()
		
