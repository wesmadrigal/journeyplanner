from google.appengine.api import mail
import logging


def main():
	message = mail.EmailMessage(sender='Wesley <wesley7879@gmail.com>',
			    subject='A test email')
	message.to='wesley7879@gmail.com'
	message.body = 'hello cron'
	message.send()


if __name__ == '__main__':
	main()










#def update_data2(routes, library, mb_api, months):
#    import logging
#    q = BusData.all().fetch(limit=1)
#    curr_day = str(int(strftime('%d')))
#    curr_m = str(int(strftime('%m')))
#    if len(q) < 1:
#        bd = BusData(bus_key=curr_day)
#        bd.data = json.dumps(library)
#        bd.put()
#        return json.dumps(library)
#    elif len(q) >= 1:
#        db_day = ''
#        db_data = ''
#        for i in q:
#            bd_day += i.bus_key
#            bd_data += i.data
#        if int(db_day) < int(curr_day):
#            parsable_data = json.loads(db_data)
#            for i in parsable_data.keys():
#                sec_hyph = i.find('-', i.find('-')+1)
#                third_hyph = i.find('-', sec_hyph + 1)
#                this_month = i[sec_hyph + 1: third_hyph]
#                this_day = i[third_hyph+1: ]
#                if int(this_month) < int(curr_m):
#                    del parsable_data[i]
#                elif int(this_month) == int(curr_m):
#                    if int(this_day) < int(curr_day):
#                        del parsable_data[i]
#            for title_c in routes:
#                for item_c in routes[title_c]:
#                    get_future_data(mb_api, title_c, item_c, int(curr_m), int(curr_day), months, parsable_data)
#                logging.info("route finished")
#            bd = BusData(bus_key = curr_day)
#            bd.data = json.dumps(parsable_data)
#            bd.put()
#            return json.dumps(parsable_data)
#        else:
#            return json.dumps(db_data)

