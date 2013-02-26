import urllib2
from HTMLParser import HTMLParser
from time import strftime



mb_api = 'http://us.megabus.com/JourneyResults.aspx?originCode={0}&destinationCode={1}&outboundDepartureDate={2}%{2}f{3}%{2}f{4}&inboundDepartureDate=&passengerCount=1&transportType=0&concessionCount=0&nusCount=0&outboundWheelchairSeated=0&outboundOtherDisabilityCount=0&inboundWheelchairSeated=0&inboundOtherDisabilityCount=0&outboundPcaCount=0&inboundPcaCount=0&promotionCode=&withReturn=0'

Buses = {'Des Moines, IA': '106', 'Milwaukee, WI': '121', 'Frederick, MD': '109', 'Minnesota': '23', 'Illinois': '13', 'Chattanooga, TN': '290', 'Indiana': '14', 'Louisiana': '18', 'Texas': '43', 'Giddings, TX': '401', 'Galveston, TX': '325', 'Dallas/Fort Worth, TX': '317', 'Knoxville, TN': '118', 'New Brunswick, NJ': '305', 'Connecticut': '7', 'Rochester, NY': '134', 'Atlanta, GA': '289', 'West Virginia': '48', 'Texarkana, AR': '407', 'La Grange, TX': '333', 'Ridgewood, NJ': '133', 'Kansas City, MO': '117', 'El Paso, TX': '397', 'Harrisburg, PA': '111', 'Big Spring, TX': '393', 'East Lansing, MI': '330', 'Toronto, ON': '145', 'Missouri': '25', 'South Bend, IN': '368', 'Fairhaven, MA': '316', 'Kenton, OH': '362', 'Carthage, TX': '395', 'New Jersey': '30', 'Valparaiso, IN': '376', 'Gainesville, FL': '296', 'Iowa City, IA': '116', 'Lufkin, TX': '404', 'Houston, TX': '318', 'San Antonio, TX': '321', 'Eagle Pass, TX': '327', 'Shreveport, LA': '332', 'Maryland': '20', 'Oklahoma City, OK': '323', 'Wisconsin': '49', 'Syracuse, NY': '139', 'Michigan': '22', 'Del Rio, TX': '328', 'New York': '32', 'Massachusetts': '21', 'Mobile, AL': '294', 'Richmond, IN': '371', 'Boston, MA': '94', 'Florida': '10', 'Rhode Island': '39', 'Sparks, NV': '419', 'Nashville , TN': '291', 'Memphis, TN': '120', 'Livingston, TX': '402', 'Ohio': '35', 'State College, PA': '137', 'Burlington, VT': '96', 'North Carolina': '33', 'Athens, GA': '302', 'District of Columbia': '9', 'Birmingham, AL': '292', 'Van Wert, OH': '364', 'Elkhart, IN': '367', 'Maine': '19', 'Christiansburg, VA': '101', 'Ontario': '51', 'Detroit, MI': '107', 'Norman, OK': '322', 'Oklahoma': '36', 'Delaware': '8', 'Champaign, IL': '98', 'Madison, U of Wisc, WI': '300', 'La Marque, TX': '337', 'Arkansas': '4', 'Humble, TX': '334', 'New Haven, CT': '122', 'Secaucus, NJ': '135', 'Indianapolis, IN': '115', 'Newark, DE': '389', 'Lima, OH': '363', 'Sacramento, CA': '415', 'Durham, NC': '131', 'Midland, TX': '405', 'Pittsburgh, PA': '128', 'Washington, DC': '142', 'California': '5', 'Uvalde, TX': '326', 'Providence, RI': '130', 'Georgia': '11', 'Columbia City, IN': '373', 'San Jose, CA': '412', 'Pennsylvania': '38', 'San Francisco, CA': '414', 'Toledo, OH': '140', 'Montgomery, AL': '293', 'Hampton, VA': '110', 'Philadelphia, PA': '127', 'Nacogdoches, TX': '406', 'Riverside, CA': '416', 'Louisville, KY': '298', 'Buffalo Airport, NY': '273', 'Little Rock, AR': '324', 'Ft. Wayne, IN': '365', 'Columbus, OH': '105', 'Dayton-Trotwood, OH': '370', 'Hartford, CT': '112', 'Cincinnati, OH': '102', 'Storrs, CT': '138', 'Buffalo, NY': '95', 'Brenham, TX': '335', 'Nevada': '28', 'Ann Arbor, MI': '91', 'Omaha, NE': '126', 'Cleveland, OH': '103', 'Charlotte, NC': '99', 'Madison, WI': '119', 'Princeton, NJ': '304', 'St Louis, MO': '136', 'Springfield, MO': '411', 'New York, NY': '123', 'Lubbock, TX': '403', 'San Angelo, TX': '329', 'Richmond, VA': '132', 'Baltimore, MD': '143', 'Albany, NY': '89', 'Minneapolis, MN': '144', 'Virginia': '46', 'Las Vegas, NV': '417', 'Binghamton, NY': '93', 'Oakland, CA': '413', 'Los Angeles, CA': '390', 'Austin, TX': '320', 'Vermont': '45', 'Grand Rapids, MI': '331', 'Warsaw, IN': '374', 'Columbia, MO': '104', 'Kentucky': '17', 'Morgantown, WV': '299', 'Nebraska': '27', 'New Orleans, LA': '303', 'Iowa': '15', 'Alabama': '53', 'Angola, IN': '366', 'Prairie View, TX': '336', 'Abilene, TX': '391', 'Chicago, IL': '100', 'Plymouth, IN': '375', 'Jacksonville, FL': '295', 'Tennessee': '42', 'Gary, IN': '369', 'Amherst, MA': '90', 'Portland, ME': '129', 'Muncie, IN': '372', 'Orlando, FL': '297', 'Saratoga Springs, NY': '301'}

# currently unused and purposeless within the scope of this program's functionality
# yet a good reference of where things started

class MyHTMLParser(HTMLParser):
	def handle_starttag(self, tag, attrs):
		print ("Start tag: ", tag)
	def handle_endtag(self, tag):
		print ("End tag: ", tag)
	def handle_data(self, data):
		print ("Data: ", data)


# function so we don't repeat any indices
def get_locations(cared_about, from_c):
    city_indices = []
    n = 0
    latest = 0
    for i in cared_about:
            for e in i:
                    if from_c in e:
                            if len(city_indices) == 0:
                                    city_indices.append(cared_about.index(i))
                            else:
                                    latest = city_indices[len(city_indices)-1]
                                    if cared_about.index(i, latest+1) not in city_indices:
                                            city_indices.append(cared_about.index(i, latest+1))	
    return city_indices



# get the cared about portion of the data
def get_cared_about(mb_api, from_city, to_city, d, m, y):
    import urllib2
    data = urllib2.urlopen(mb_api.format(Buses[from_city], Buses[to_city], m, d, y)).read().split('\n')
    new_data = [i.split('\r') for i in data]
    start = 0
    stop = 0
    for i in new_data:
            for e in i:
                    if 'Departs' in e:
                            start = new_data.index(i)
                    elif 'footer' in e:
                            stop = new_data.index(i)
    return new_data[start:stop]








# function to take cared_about and get the times

def find_times(cared_about, from_city):
    city_indices = get_locations(cared_about, from_city)
    times = {}
    iteration = 1
    dep_str = ''
    arr_str = ''
		# this lines purpose would be to compensate for re-iterating over the same data
			    #del cared_about[cared_about.index(i)]
    while len(city_indices) > 0:
	#dep_str = ''
	#arr_str = ''
    	curr = city_indices[0]
        del city_indices[0]
        for i in cared_about[curr-2][0]:
        	if i.isdigit():
                	dep_str += i
                elif i.isupper():
                        dep_str += i
        for e in cared_about[curr+7][0]:
                if e.isdigit():
                        arr_str += e
                elif e.isupper():
                        arr_str += e
        times[str(iteration)] = [dep_str, arr_str]
        iteration += 1
	dep_str = ''
	arr_str = ''
    return times
    

# What I have so far of collecting data and putting it into a database
# initialize the database


# python sqlite3 version of get_future_data

def get_future_data(mb_api, from_city, to_city, m, d, months, database):
	initial_it = [i for i in c.execute("select id from CityTripsByDate")]
	it = 1
	if initial_it:
		str_it = str(max(initial_it))
		real_it = ''
		for i in str_it:
			if i.isdigit():
				real_it += i
		it = int(real_it) + 1
	for i in range(int(d), int(d)+14):
		if m == '2':
			if i in months[1]:
				cared_about = get_cared_about(mb_api, from_city, to_city, str(i), m, y)
				times = str(find_times(cared_about, from_city))
				c.execute("insert into CityTripsByDate values(?,?,?,?,?,?)", (it, from_city, to_city, m, str(i), times))
			elif i not in months[1]:
				curr = months[int(m)][abs(i-len(months[1]))-1]
				cared_about = get_cared_about(mb_api, from_city, to_city, str(curr), str(int(m)+1), y)
				times = str(find_times(cared_about, from_city))
				c.execute("insert into CityTripsByDate values(?,?,?,?,?,?)", (it, from_city, to_city, str(int(m)+1), str(curr), times))
		elif m != '2' and i in months[int(m)-1]:
			cared_about = get_cared_about(mb_api, from_city, to_city, str(i), str(int(m)), y)
			times = str(find_times(cared_about, from_city))
			c.execute("insert into CityTripsByDate values(?,?,?,?,?,?)", (it, from_city, to_city, m, str(i), times))
		else:
			curr = months[int(m)][i%len(months[int(m)])]
			cared_about = get_cared_about(mb_api, from_city, to_city, str(curr), str(int(m)+1), y)
			times = str(find_times(cared_about, from_city))
			c.execute("insert into CityTripsByDate values(?,?,?,?,?,?)", (it, from_city, to_city, str(int(m)+1), str(curr), times))
		it += 1
	return "Two weeks of ", from_city, " to ", to_city, " have been entered into the database."
 

######################################################################################



def main():
	from_city = raw_input('City bus leaving from: ')
	to_city = raw_input('City bus going to: ')
	m = raw_input('Month of travel: ')
	d = raw_input('Day of travel: ')
	# plug in the values to the API and generate the data
	time_str = strftime('%m:%d:%Y')
	col = time_str.find(':')
	#m = time_str[col-1]
	#d = str(int(time_str[col + 1: time_str.find(':', col+1)])+1)
	y = time_str[time_str.find(':', col + 1)+1:]

	cared_about = get_cared_about(mb_api, from_city, to_city, d, m, y)
	the_times = find_times(cared_about, from_city)
	print the_times
	




if __name__ == '__main__':
	main()
