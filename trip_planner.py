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
                            trip_time += '.'
                            for l in e[e.find('hrs')+1:]:
                                    if l.isdigit():
                                            trip_time += l
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
            if hours_so_far < 15:
                formatted_apis[i] += "window.open('%s');" % mb_api.format(Buses[trip_dict[i][e]], Buses[trip_dict[i][e+1]], month, day, year)
                hours_so_far += float(find_hours(cared_about, trip_dict[i][e]))
            else:
                formatted_apis[i] += "window.open('%s');" % mb_api.format(Buses[trip_dict[i][e]], Buses[trip_dict[i][e+1]], month, str(int(day)+1), year)
                hours_so_far += float(find_hours(cared_about, trip_dict[i][e]))
    return formatted_apis






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
