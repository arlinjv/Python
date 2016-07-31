import pickle

# basic query format:
# {'user':'arlinjv@att.net','search_terms':{'fullname':fullname}}

output = open('queries.pkl','wb')

query_list = [{'user':'arlinjv@att.net','search_terms':{'fullname':'GARR ANDR','inmatesfnumber':''}},
				{'user':'arlinjv@att.net','search_terms':{'fullname':'','inmatesfnumber':'679810'}},
				{'user':'arlinjv@att.net','search_terms':{'fullname':'schmoe joe','inmatesfnumber':''}}]
				
pickle.dump(query_list, output)

output.close()
