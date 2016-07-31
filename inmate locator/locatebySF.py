import urllib
import urllib2
import json
import pprint
import sys

#input scheme:
#last_name first_name unless or sfno only

#sample get queries from sfsd page:
#http://apps.sfgov.org/InmateInfo/ajax/searchCustomers.php?fullname=GARR%20ANDRE&inmatesfnumber=undefined&bookingnumber=undefined
#http://apps.sfgov.org/InmateInfo/ajax/searchCustomers.php?inmatesfnumber=638346

url = 'http://apps.sfgov.org/InmateInfo/ajax/searchCustomers.php?'

sfno = '638346'
values = {'fullname':'','inmatesfnumber':sfno}
data = {}

query = urllib.urlencode(values)
req = urllib2.Request(url + query)

full_url = req.get_full_url()
print full_url

response = urllib2.urlopen(req)
dataList = json.load(response) #returns dict as first element in single element list
data = dataList[0]#extract dict from list


pprint.pprint(data)
