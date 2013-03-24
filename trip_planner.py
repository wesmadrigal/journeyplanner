from get_route import *





def plan_trip(start, finish, routes):
		hops = {}
        	journey = {}
        	hops[start] = {}
        	journey[start] = {}
                open_list = []
                for i in routes[start]:
                        hops[start][i] = 1
                        journey[start][i] = {'1': [start, i]}
                        open_list.append(i)
                while len(open_list) > 0:
                        titlecity = open_list[0]
                        del open_list[0]
                        for cityitem in routes[titlecity]:
                                if cityitem not in hops[start]:
                                        hops[start][cityitem] = hops[start][titlecity] + 1
                                        keys = [int(i) for i in journey[start][titlecity].keys()]
                                        the_key = str(max(keys))
                                        journey[start][cityitem] = {'1': journey[start][titlecity][the_key] + [cityitem]}
                                        open_list.append(cityitem)
                                elif cityitem in hops[start]:
                                        if hops[start][cityitem] > hops[start][titlecity]+1:
                                                hops[start][cityitem] = hops[start][titlecity]+1
                                                keys = [int(i) for i in journey[start][titlecity].keys()]
                    #the_title_key = str(max(keys))
                                                the_new_item_key = str(max([int(i) for i in journey[start][cityitem].keys()])+1)
                                                journey[start][cityitem][the_new_item_key] = journey[start][titlecity][the_title_key] + [cityitem]
                                        elif hops[start][cityitem] == hops[start][titlecity]+1:
                                                title_key = str(max([int(i) for i in journey[start][titlecity].keys()]))
                                                new_key = str(max([int(i) for i in journey[start][cityitem].keys()])+1)
                                                journey[start][cityitem][new_key] = journey[start][titlecity][title_key] + [cityitem]
                return journey[start][finish]


# algorithm utilizing some of the get_route algorithms to figure out the time for a trip

def find_hours(cared_about, from_c):
    locs = get_locations(cared_about, from_c)
    region = cared_about[locs[0]:]
    if len(locs) > 1:
        region = cared_about[locs[0]:locs[1]]
    trip_time = ''
    for i in region:
            for e in i:
                    if 'hrs' and 'mins' in e:
                            for f in e[0: e.find('hrs')]:
                                    if f.isdigit():
                                            trip_time += f
                            #trip_time += '.'
			    sec_digs = ''
                            for l in e[e.find('hrs')+1:]:
                                    if l.isdigit():
                                            sec_digs += l
			    sec_digs2 = str(float(int(sec_digs))/float(60))
			    to_add = sec_digs2[sec_digs2.find('.'):sec_digs2.find('.')+3]
			    trip_time += to_add
    return trip_time


# To utilize the tools above, we can combine them into an even better algorithm to give us 
# all the link options for our users

def generate_proper_routes(from_c, to_c, day, routes):
    month = str(int(strftime('%m')))
    year = str(int(strftime('%Y')))
    trip_dict = plan_trip(from_c, to_c, routes)
    formatted_apis = {}
    for i in trip_dict.keys():
        hours_so_far = 0
        formatted_apis[i] = ''
        for e in range(len(trip_dict[i])-1):
            cared_about = get_cared_about(mb_api, trip_dict[i][e], trip_dict[i][e+1], day, month, year)
            if hours_so_far < 12:
                formatted_apis[i] += "window.open('%s');" % mb_api.format(Buses[trip_dict[i][e]], Buses[trip_dict[i][e+1]], month, day, year)
                hours_so_far += float(find_hours(cared_about, trip_dict[i][e]))
            else:
                formatted_apis[i] += "window.open('%s');" % mb_api.format(Buses[trip_dict[i][e]], Buses[trip_dict[i][e+1]], month, str(int(day)+1), year)
                hours_so_far += float(find_hours(cared_about, trip_dict[i][e]))
    return formatted_apis




def make_displayable_options(from_c, to_c, day, routes):
    month = str(int(strftime('%m')))
    year = str(int(strftime('%Y')))
    trip_dict = plan_trip(from_c, to_c, routes)
    link_trip_dict = {}
    for i in trip_dict.keys():
        key = ''
        hours_so_far = 0
        for e in trip_dict[i]:
            if trip_dict[i].index(e) != len(trip_dict[i])-1:
                key += e + ' -----> '
            else:
                key += e
        link_trip_dict[key] = ''
        for j in range(len(trip_dict[i])-1):
            cared_about = get_cared_about(mb_api, trip_dict[i][j], trip_dict[i][j+1], day, month, year)
            if hours_so_far < 12:
                link_trip_dict[key] += "window.open('%s');" % mb_api.format(Buses[trip_dict[i][j]], Buses[trip_dict[i][j+1]], month, day, year)
                hours_so_far += float(find_hours(cared_about, trip_dict[i][j]))
            elif hours_so_far > 20:
                link_trip_dict[key] += "window.open('%s');" % mb_api.format(Buses[trip_dict[i][j]], Buses[trip_dict[i][j+1]], month, str(int(day)+1), year)
                hours_so_far += float(find_hours(cared_about, trip_dict[i][j]))
	    else:
	   	link_trip_dict[key] += "window.open('%s');" % mb_api.format(Buses[trip_dict[i][j]], Buses[trip_dict[i][j+1]], month, str(int(day)+2), year)
		hours_so_far += float(find_hours(cared_about, trip_dict[i][j]))
    return link_trip_dict


# algorithm returning two dictionaries
# first contains trip as key and trip links as values
# second contains trips as keys and hours of trip as values

def make_displayable_options2(from_c, to_c, day, routes):
    month = str(int(strftime('%m')))
    year = str(int(strftime('%Y')))
    trip_dict = plan_trip(from_c, to_c, routes)
    link_trip_dict = {}
    trip_hours = {}
    for i in trip_dict.keys():
        key = ''
        hours_so_far = 0
        for e in trip_dict[i]:
            if trip_dict[i].index(e) != len(trip_dict[i])-1:
                key += e + ' -----> '
            else:
                key += e
        link_trip_dict[key] = ''
        for j in range(len(trip_dict[i])-1):
            cared_about = get_cared_about(mb_api, trip_dict[i][j], trip_dict[i][j+1], day, month, year)
            if hours_so_far < 12:
                link_trip_dict[key] += "window.open('%s');" % mb_api.format(Buses[trip_dict[i][j]], Buses[trip_dict[i][j+1]], month, day, year)
                hours_so_far += float(find_hours(cared_about, trip_dict[i][j]))
            elif hours_so_far > 12 and hours_so_far < 24:
                link_trip_dict[key] += "window.open('%s');" % mb_api.format(Buses[trip_dict[i][j]], Buses[trip_dict[i][j+1]], month, str(int(day)+1), year)
                hours_so_far += float(find_hours(cared_about, trip_dict[i][j]))
            elif hours_so_far > 24:
                link_trip_dict[key] += "window.open('%s');" % mb_api.format(Buses[trip_dict[i][j]], Buses[trip_dict[i][j+1]], month, str(int(day)+2), year)
                hours_so_far += float(find_hours(cared_about, trip_dict[i][j]))
        trip_hours[key] = hours_so_far
    return link_trip_dict, trip_hours



# newest algorithm addition to break up trip options into separate items
# break those items up into their respective legs
# and add a list of specific trip time options to each let
# this algorithm combines multiple previously defined algorithms
# to output three dictionaries related to our trip options


def make_formatted(trip, m, day):
    y = '2013'
    link_trip_dict = {}
    trip_dict_formatted = {}
    trip_hours = {}
    for i in trip.keys():
        trip_dict_formatted[i] = {}
        hours_so_far = 0
        link_trip_dict[i] = ''
        for e in range(len(trip[i])-1):
            leg = 'leg ' + str(e+1)
            cared_about = get_cared_about(mb_api, trip[i][e], trip[i][e+1], day, m, y)
            times = find_times_and_price(cared_about, trip[i][e])
            if hours_so_far < 12:
                link_trip_dict[i] += "window.open('%s');" % mb_api.format(Buses[trip[i][e]], Buses[trip[i][e+1]], m, day, y)
                key = trip[i][e] + '-' + trip[i][e+1] + '-' + m + '-' + day
                hours_so_far += float(find_hours(cared_about, trip[i][e]))
            elif hours_so_far > 12 and hours_so_far < 24:
                link_trip_dict[i] += "window.open('%s');" % mb_api.format(Buses[trip[i][e]], Buses[trip[i][e+1]], m, str(int(day)+1), y)
                key = trip[i][e] + '-' + trip[i][e+1] + '-' + m + '-' + str(int(day)+1)
                hours_so_far += float(find_hours(cared_about, trip[i][e]))
            elif hours_so_far > 24:
                link_trip_dict[i] += "window.open('%s');" % mb_api.format(Buses[trip[i][e]], Buses[trip[i][e+1]], m, str(int(day)+2), y)
                key = trip[i][e] + '-' + trip[i][e+1] + '-' + m + '-' + str(int(day)+2)
                hours_so_far += float(find_hours(cared_about, trip[i][e]))
            trip_dict_formatted[i][leg] = {}
            trip_dict_formatted[i][leg][key] = times
        trip_hours[i] = hours_so_far
    return trip_dict_formatted, trip_hours, link_trip_dict


# this algorithm uses the above "make_formatted" algorithm and takes all of 
# make_formatted's responses as inputs to generate a proper html response
# to render

def generate_response(trip_dict, trip_hours, link_trip_dict):
    response = ''
    response += '<div class="tripOptions">'
    #trips = sorted([int(i) for i in trip_dict.keys()])
    trip_dict_keys = sorted([int(i) for i in trip_dict.keys()])
    for trip_dict_key in trip_dict_keys:
        response += '<a class="option-button" href="http://us.megabus.com" target="_blank" onclick="{0}"><b>Option {1}</b></a>'.format(link_trip_dict[str(trip_dict_key)], str(trip_dict_key))
        response += '<p>Total on-bus hours: <b>%s</b></p>' % trip_hours[str(trip_dict_key)]
	# to sort the legs
	legs = sorted([int(i[i.find(' ')+1:]) for i in trip_dict[str(trip_dict_key)].keys()])
	for leg in legs:
	    the_leg = 'leg ' + str(leg)
            response += '<p%s</p><br>' % the_leg
            for route in trip_dict[str(trip_dict_key)][the_leg].keys():
		first = route.find('-')
		second = route.find('-', first+1)
		from_c = route[0:first]
		to_c = route[first+1:second]
		new_route = from_c + '  ----->  ' + to_c + ' on %s' % route[second+1:] 
                response += '<p><h4><b>%s</b></h4></p>' % new_route
                response += '<ul>'
                for time, price in trip_dict[str(trip_dict_key)][the_leg][route]:
                    response += '<li style="border:10px; margin:10px;"><h5>%s<p style="margin-left:10px; color:blue;">%s</p></h5></li>' % (time,price)
                response += '</ul>'
            response += '<br><br>'
        #response += '<a href="http://us.megabus.com" target="_blank" onclick="%s">Click for official site links</a><br><hr>' % link_trip_dict[str(trip_dict_key)]
    	response += '<br><hr>'
	response += '</div>'
    return response


def make_trip_buttons_dict(trip):
    trip_buttons_dict = {}
    for i in trip.keys():
        trip_buttons_dict[i] = ''
        for e in trip[i]:
            if trip[i].index(e) != len(trip[i])-1:
                trip_buttons_dict[i] += e + ' -----> '
            else:
                trip_buttons_dict[i] += e
    return trip_buttons_dict


def main():
	url = "new_cities.xml"
	xml = get_doc(url)
	locs = get_title_locations(xml)
	routes = generate_routes2(xml, locs)
	start = raw_input("Enter a departure city: ")
	finish = raw_input("Enter an arrival city: ")	

	result = plan_trip(start, finish, routes)
	for i in result.keys():
		print i, result[i]



if __name__ == '__main__':
	main()
