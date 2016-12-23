from flask import Flask, url_for, json, request, send_file, jsonify

#return data formating
from bson.json_util import dumps

#print data formating
import pprint

#mongodb support 
from pymongo import MongoClient

# create random key
from os import urandom

# http status return
from flask_api import status

app = Flask(__name__)

def initDB():
    url = "mongodb://user1:kuncikunci@ds141108.mlab.com:41108/baby"
    client = MongoClient(url) 
    return client['baby']

def settupDB():
  handle = initDB()

  #cityDB
  if handle['city'].count() == 0:
    cityInfor = [{
      "city": "Toronto",
      "desc": "Home of the Maple Leaf",
      "lat":43.6765211, 
      "lng":-79.4354023,
      "hoster":[]
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

  #babySitterDB
  babysitterInfor = None
  if handle['babysitter'].count() == 0:
    babysitterInfor = [{
      "city": "Toronto",
      "host": "Trust Child Care",
      "phone": "+1-416-594-0100",
      "image": "https://s3-media3.fl.yelpcdn.com/bphoto/4jqa-wa-NEzajkwT83E09Q/ms.jpg",
      "display_addr": [
        "29 Birch Avenue",
        "Summer Hill",
        "Toronto, ON M4V 1E2",
        "Canada"
      ],
      "lat": 43.6809387,
      "lng": -79.3928223,
      "rating": 5.0,
      "desc": "As of January 2012, Trust Child Care is under new ownership. As an owner, parent and primary educator I would invite you to please arrange for a tour so...",
      "url": "http://www.yelp.com/biz/trust-child-care-toronto-2?adjust_creative=dWycgaunp1RGGmO0t-TQTw&utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=dWycgaunp1RGGmO0t-TQTw"
    }, 
    {
      "city": "Toronto",
      "host": "Play 'n Stay Daycare",
      "phone": "None",
      "image": "None",
      "display_addr": [
        "811 Gerrard Street E",
        "Riverdale",
        "Toronto, ON M4M 1Y7",
        "Canada"
      ],
      "lat": 43.6671308,
      "lng": -79.3449661,
      "rating": 5.0,
      "desc": "My son has been a member of Gloria's family since January 2013 and his has thrived in this home based nurturing home daycare environment. Gloria has been an...",
      "url": "http://www.yelp.com/biz/play-n-stay-daycare-toronto?adjust_creative=dWycgaunp1RGGmO0t-TQTw&utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=dWycgaunp1RGGmO0t-TQTw"
    }]
    handle['babysitter'].insert(babysitterInfor)
    #add to the host list for each city
    for item in babysitterInfor:
      handle['city'].update({'city': item['city']}, {'$push': {'hoster': item}})

  return handle

#setupDB
handle = settupDB()

# AUTHENTICATION will be handled by 
# /api/login, /api/signup and /api/logout
# send session_token to  client to maintain session

# dummy users
USERS = {
	'imranariffin': {
		'username': 'imranariffin',
		'password': 'password',
		'dum_info' : 'Imma noob programmer'
	},
	'admin': {
		'username': 'admin',
		'password': 'password',
		'dum_info' : 'Imma not a noob programmer'
	}
}

@app.route("/api/login", methods=['POST'])
def login():
	# request data: username, password
	# response: status: 200, 401, 404
	# 	200: success login
	# 	401: wrong password
	# 	404: user not exist
	# 	417: request data doesn't meet expectation

	form = request.get_json()

	if 'username' not in form or 'password' not in form:
		response = {'error_message': 'request data should contain username and password'}
		return jsonify(response), status.HTTP_417_EXPECTATION_FAILED

	username = form['username']
	password = form['password']

	if username not in USERS:
		response = {'error_message': 'user does not exist'}
		return jsonify(response), status.HTTP_404_NOT_FOUND

	if password != USERS[username]['password']:
		response = {'error_message': 'wrong password'}
		return jsonify(response), status.HTTP_401_UNAUTHORIZED

	# # create session for user
	# session[username] = username

	# dummy session_token
	session_token = {
		'admin': 'token1', 
		'imranariffin': 'token2', 
	}[username]

	# respond with succes message and status code

	response = {
		'message': 'success', 
		'session_token': session_token,
		'user': USERS[username],
	}
	return jsonify(response), status.HTTP_200_OK


@app.route("/api/logout", methods=['POST'])
def logout():
	# response: status: 200
	# 	200: success

	# form = request.get_json()

	# if form == None or len(form) == 0 or 'username' not in form:
	# 	response = {'error_message': 'bad request, need to have username as in data'}
	# 	return jsonify(response), status.HTTP_417_EXPECTATION_FAILED

	# username = form['username']

	# if username not in USERS:
	# 	response = {'error_message': 'user not found'}
	# 	return jsonify(response), status.HTTP_404_NOT_FOUND

	# # remove session
	# session.pop(username, None)

	response = {'message': 'success logout'}
	return jsonify(response), status.HTTP_200_OK

@app.route("/")
def mainPage():
  return send_file("templates/index.html")

#find all the cities and host for initial map
@app.route('/api/city')
def city():
  cursor = handle.city.find()
  return dumps(cursor)

#return all the info or one city
@app.route('/api/find/babysitter/<name>', methods = ['GET'])
def getBabysitterInfo(name):
  if name != None:
    cursor = handle.babysitter.find( {"city": name} )
    return dumps(cursor)
  return "Error"

@app.route('/api/insert/babysitter', methods=['GET', 'POST'])
def add_message():
  content = request.get_json(silent=True)
  username, cityname = content['host'], content['city']
  
  #alternative way to do the and search
  #handle.babysitter.find({ '$and': [{ 'city': { '$eq': cityname }}, {'host': {'$eq': username}}]}).count()
  if handle.babysitter.find({'city': cityname, 'host': username}).count() == 0:
    #insert new babysitter information in the DB
    handle['babysitter'].insert(content)

    #dynamic uploading the babysitter information into the city table
    handle['city'].update({'city': content['city']}, {'$push': {'hoster': content}})

  return "uploading.."

if __name__ == "__main__":
	app.secret_key = urandom(24)
	app.run(host='0.0.0.0', port=8000)





