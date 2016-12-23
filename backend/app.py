
from flask import Flask, url_for, json

app = Flask(__name__)

#angular connection support 
from flask.ext.cors import CORS
CORS(app)

#return data formating
from bson.json_util import dumps

#print data formating
import pprint

#mongodb support 
from pymongo import MongoClient



def initDB():
    url = "mongodb://user1:kuncikunci@ds141108.mlab.com:41108/baby"
    client = MongoClient(url) 
    return client['baby']

def settupDB():
  handle = initDB()

  if handle['city'].count() == 0:
    cityInfor = [{
      "city": "Toronto",
      "desc": "Home of the Maple Leaf",
      "lat":43.6765211, 
      "lng":-79.4354023,
      },
      {
        "city": "New York",
        "desc": "The city that never sleeps",
        "lat":40.7142700, 
        "lng":-74.0059700,
        "hoster":[]
      }, 
      {
        "city": "San Francisco",
        "desc": "The Golden Gate City",
        "lat":37.7749300, 
        "lng":-122.4194200,
        "hoster":[]
      }, 
      {
        "city": "Vancouver",
        "desc": "The Rain City",
        "lat":49.246292, 
        "lng":-123.116226,
        "hoster":[]
    }]
    handle['city'].insert(cityInfor)
  return handle

#setupDB
handle = settupDB()


@app.route('/api/city')
def city():
  # for i in handle.city.find():
  #   pprint.pprint(i)
  # return

  cursor = handle.city.find()
  return dumps(cursor)


#return all the info or one city
@app.route('/api/babysitter/<name>', methods = ['get'])
def getBabysitterInfo():
  return "babysitter"

@app.route('/api/babysitter/<upload>', methods = ['post'])
def uploadBabysitterInfo():
  return "information"



if __name__ == '__main__':
	app.run(host='0.0.0.0')
