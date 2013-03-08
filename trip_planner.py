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
