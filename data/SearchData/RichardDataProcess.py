#!/usr/bin/python

from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

auth = Oauth1Authenticator(
    consumer_key="dWycgaunp1RGGmO0t-TQTw",
    consumer_secret="ACJuyFqTtPSfOE0LxJshLayHz0Q",
    token= "oh5tvvR-GdUGGOJVYCwxEpSVTSHBfpRv",
    token_secret="GdjJ69oleODdTLnmYLTvKfaCZOA"
)

client = Client(auth)

params = {
    'term': 'daycare',
    'offset': 80
    #'limit': '20'
}


response = client.search("Toronto",**params)
#test = "hello\nwo\nrld"
#test = test.replace("\n"," ")
#print test

#print response
print "total search results: ",response.total
bnum = len(response.businesses)
print "total number of businesses: ", bnum

f = open("searchdata.json","wb")
f.write('[\n')
for num in range(0,bnum):
	b = response.businesses[num]
	f.write('\t{\n')
	f.write('\t\t'+'"host": "'+ str(b.name) + '",\n')
	f.write('\t\t'+'"phone": "'+ str(b.display_phone) + '",\n')
	f.write('\t\t'+ '"image": "' + str(b.image_url)+ '",\n')
	#f.write( '"display_addr":' + b.location.display_address+ '\n')
	f.write('\t\t'+ '"display_addr": [\n')
	for addr in b.location.display_address:
		if(b.location.display_address.index(addr) != len(b.location.display_address)-1 and len(b.location.display_address) != 1):
			f.write('\t\t\t"' + str(addr) + '",\n')
		else:
			f.write('\t\t\t"' + str(addr) + '"\n')
	f.write('\t\t'+ '],\n')	
	f.write( '\t\t'+'"lat":'+ str(b.location.coordinate.latitude)+',\n')
	f.write( '\t\t'+'"lng":' + str(b.location.coordinate.longitude)+',\n')
	f.write( '\t\t'+'"rating":' + str(b.rating) + ',\n')
	text=str(b.snippet_text)
	text=text.replace("\n"," ")
	f.write( '\t\t'+'"desc": "' +text+ '",\n')
	f.write('\t\t'+ '"url": "' +str(b.url)+ '"\n')
	if(response.businesses.index(b) != len(response.businesses)-1 and len(response.businesses) != 1):
		f.write("\t},\n")
	else:
		f.write("\t}\n")

f.write(']\n')
f.close()
