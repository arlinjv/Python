import urllib
import urllib2
import json
import pprint
import sys
import argparse
import pickle


"""
To do:
- read queries from file
	- build queries and process through getData
- receive texts or emails and build queries
	- do in separate app? (run via cron job every n seconds and have this app check for changes in file?)
	- save in list of dicts, where user name is email or phone number 
	- start by saving in memory then pickle and save in file
- send texts or emails 
"""

#samle output from sfsd page:
#http://apps.sfgov.org/InmateInfo/ajax/searchCustomers.php?fullname=GARR%20ANDRE&inmatesfnumber=undefined&bookingnumber=undefined

# basic query format:
# {'user':'arlinjv@att.net','search_terms':{'fullname':'',inmatesfnumber:''}}


parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-f', action="store", dest="file_name") #file to load queries from 
parser.add_argument('query', action="store", nargs='*') #one arg is sfno two is last and first names
args = parser.parse_args()

url = 'http://apps.sfgov.org/InmateInfo/ajax/searchCustomers.php?'# ok, not the whole url
data = [] # pack one or more query result into here
query = {'user':'','expiration':'','search_terms':{'fullname':'','inmatesfnumber':''}}#basically using as a template

# all_queries = {'user':'','queries':[]} 
# when processing queries create new dict where key is user name and value is list of queries
# use defaultdict as in here https://docs.python.org/3/library/collections.html#defaultdict-examples

def getData ():
	query_string = urllib.urlencode(query['search_terms'])
	req = urllib2.Request(url + query_string)
	response = urllib2.urlopen(req)
	dataList = json.load(response) #returns dict as first element in single element list
	if isinstance(dataList, list):
		if len(dataList) == 1:
			print "got a hit"
			print dataList
			return dataList[0]#extract dict from list
		elif len(dataList) > 1:
			print "multiple hits. returning first"
			return dataList[0]#extract dict from list
		else:
			print "no data"
			return {}
	else:
		print "no list returned"

if isinstance(args.file_name, str): #if args.file_name has been assigned a value 
	print "loading from ", args.file_name
	query_file = open(args.file_name,'rb')
	query_list = pickle.load(query_file)
	print "Number of queries loaded: ", len(query_list)
	for q in query_list:
		query = q
		data.append(getData())																																																																																																																																																																																																																																																																																																																																																																																																													
elif len(args.query) == 1:
	print "querying by sfno: ", args.query
	query['search_terms']['inmatesfnumber'] = args.query[0]  
	data.append(getData())
elif len(args.query) == 2:
	print "querying by name: ", args.query[0], args.query[1]
	last_name = args.query[0]
	first_name = args.query[1]
	fullname = last_name + ' ' + first_name	
	query['search_terms']['fullname'] = fullname
	data.append(getData())
else:
	print "insufficient arguments: "
	
	
#full_url = req.get_full_url()
#pprint.pprint(data)
