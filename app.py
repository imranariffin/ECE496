from flask import Flask, url_for, json, request, send_file, jsonify, Response

from bson.json_util import dumps

#print data formating
import pprint

import dbsetup

# create random key
from os import urandom

# http status return
from flask_api import status

#hashing for token
import hashing

#for the review system
import datetime


app = Flask(__name__)

#setupDB
handle = dbsetup.setupDB()





"""
response: status: 200, 401, 404
200: success login
401: wrong password
403: forbidden 
404: user not exist
409: user is exsiting 
417: request data doesn't meet expectation
"""

# AUTHENTICATION will be handled by 
# /api/login, /api/signup and /api/logout
@app.route("/api/login", methods=['POST'])
def login():
  form = request.get_json()

  if 'username' not in form or 'password' not in form:
    response = {'error_message': 'request data should contain username and password'}
    return jsonify(response), status.HTTP_417_EXPECTATION_FAILED

  username = form['username']
  password = form['password']

  result = handle.user.find({'username': username})
  if result.count() == 0:
    response = {'error_message': 'user does not exist'}
    return jsonify(response), status.HTTP_404_NOT_FOUND
  elif list(result)[0]["password"] != password:
    response = {'error_message': 'wrong password'}
    return jsonify(response), status.HTTP_401_UNAUTHORIZED
  else:
    response = {
      'message': 'success', 
      'user': username,
      'session_token': hashing.Encrypted(username + password)
    }
    return jsonify(response), status.HTTP_200_OK


@app.route("/api/logout", methods=['POST'])
def logout():
  # response: status: 200
  #   200: success
  token1 = request.headers['Token1']
  token2 = request.headers['Token2']
  form = request.get_json()

  if hashing.Decrypted([token1, token2]) != True:
    response = {'error_message': 'HTTP_403_FORBIDDEN, cannot access'}
    return jsonify(response), status.HTTP_403_FORBIDDEN

  if form == None or len(form) == 0 or 'username' not in form:
    response = {'error_message': 'bad request, need to have username as in data'}
    return jsonify(response), status.HTTP_417_EXPECTATION_FAILED

  username = form['username']
  if handle.user.find({'username': username}).count() == 0:
    response = {'error_message': 'user not found'}
    return jsonify(response), status.HTTP_404_NOT_FOUND

  response = {'message': 'success logout'}
  return jsonify(response), status.HTTP_200_OK


@app.route("/api/signup", methods = ['POST'])
def signup():
  form = request.get_json()
  
  if 'username' not in form or 'password' not in form or 'host' not in form:
    response = {'error_message': 'request data should contain username and password'}
    return jsonify(response), status.HTTP_417_EXPECTATION_FAILED

  username = form['username']
  password = form['password']
  host = form['host']
  if handle.user.find({'username': username}).count() != 0:
    response = {'error_message': 'username has been registered'}
    return jsonify(response), status.HTTP_409_CONFLICT 
  else:
    if form['host'].lower() == "parent":
      form['host'] = False
    else:
      form['host'] = True
      
    #Insert user credentials
    user_info = {
      'username': username,
      'password': password,
      'host': host
    }
    handle.user.insert(user_info)

    response = {
      'message': 'success signup',
      'session_token': hashing.Encrypted(username+password),
    }
    return jsonify(response), status.HTTP_200_OK

@app.route("/")
def mainPage():
  return send_file("templates/index.html")

#find all the cities and host for initial map
@app.route('/api/city')
def city():
  form = request.get_json()
  token1 = request.headers['Token1']
  token2 = request.headers['Token2']
  
  if hashing.Decrypted([token1, token2]) != True:
    response = {'error_message': 'HTTP_403_FORBIDDEN, cannot access'}
    return jsonify(response), status.HTTP_403_FORBIDDEN

  cursor = handle.city.find()
  return dumps(cursor)

#return all the info or one city
@app.route('/api/find/babysitter/<name>', methods = ['GET'])
def getBabysitterInfo(name):
  token1 = request.headers['Token1']
  token2 = request.headers['Token2']

  if hashing.Decrypted([token1, token2]) != True:
    response = {'error_message': 'HTTP_403_FORBIDDEN, cannot access'}
    return jsonify(response), status.HTTP_403_FORBIDDEN

  if name == None:
    response = {'error_message': 'request data should contain city name'}
    return jsonify(response), status.HTTP_417_EXPECTATION_FAILED
  else:
    cursor = handle.babysitter.find( {"city": name} )
    return dumps(cursor)

@app.route('/api/insert/babysitter', methods=['GET', 'POST'])
def add_message():

  token1 = request.headers['Token1']
  token2 = request.headers['Token2']
  if hashing.Decrypted([token1, token2]) != True:
    response = {'error_message': 'HTTP_403_FORBIDDEN, cannot access'}
    return jsonify(response), status.HTTP_403_FORBIDDEN

  content = request.get_json()
  username, cityname = content['host'], content['city']
  
  #alternative way to do the and search
  #handle.babysitter.find({ '$and': [{ 'city': { '$eq': cityname }}, {'host': {'$eq': username}}]}).count()
  if handle.babysitter.find({'host': username}).count() != 0:
    response = {'error_message': 'username has been registered'}
    return jsonify(response), status.HTTP_409_CONFLICT 
  else:
    #insert new babysitter information in the DB
    handle['babysitter'].insert(content)

    #dynamic uploading the babysitter information into the city table
    handle['city'].update({'city': content['city']}, {'$push': {'hoster': content}})

  response = {'message': 'success insert babysitter records'}
  return jsonify(response), status.HTTP_200_OK



"""
REVIEW API: get all reviews for a babysitter
response: list of review string with respective reviewer username
error: 400, 404 with message
"""
@app.route('/api/babysitter/<sitter_username>/review', methods=['GET', 'POST'])
def get_babysitter_review_list(sitter_username):

  token1 = request.headers['Token1']
  token2 = request.headers['Token2']

  if hashing.Decrypted([token1, token2]) != True:
    response = {'error_message': 'HTTP_403_FORBIDDEN, cannot access'}
    return jsonify(response), status.HTTP_403_FORBIDDEN

  if request.method == 'GET':

    babysitter = handle['babysitter'].find_one({'username': sitter_username})

    if babysitter is None:
      response = {"err": "Error 404: No babysitter with such username %s"%sitter_username}
      return jsonify(response), status.HTTP_404_NOT_FOUND

    ls_reviews = [{
      'username': parent, 
      'value': babysitter['review'][parent]['value'],
      "date": babysitter['review'][parent]['date'],
      "title": babysitter['review'][parent]['title'],

    } for parent in babysitter['review']]

    return jsonify(ls_reviews), status.HTTP_200_OK

  # POST request
  form = request.get_json()

  if 'username' not in form:
    # error, should log first
    response = {"err": "Should log in"}
    return jsonify(response), status.HTTP_400_BAD_REQUEST

  if 'review' not in form or form['review'] == "":
    # error, review should not be empty
    response = {"err": "Review should not be empty"}
    return jsonify(response), status.HTTP_400_BAD_REQUEST

  if 'title' not in form or form['title'] == "":
    # error, review should not be empty
    response = {"err": "Review title should not be empty"}
    return jsonify(response), status.HTTP_400_BAD_REQUEST

  if handle['user'].find_one({'username': form['username']}) is None:
    # error, user should exist
    response = {"err": "user does not exist"}
    return jsonify(response), status.HTTP_400_BAD_REQUEST

  # add current user's review for babysitter
  review = form['review']
  currentuser_username = form['username']

  title = form['title']

  #storing current time
  d = datetime.datetime.now().timetuple()
  date = {"year": d[0], "month": d[1], "day": d[2]}

  # babysitter['review'][currentuser_username] = review
  res = handle['babysitter'].update_one(
      {"username": sitter_username},
      {"$set": {
        "review.%s"%currentuser_username: {"value": review, "date": date, "title": title}
      }})

  if res.matched_count == 0:
    # error, babysitter doesn't exist
    response = {"err": "babysitter %s doesn't exist"%sitter_username}
    return jsonify(response), status.HTTP_400_BAD_REQUEST

  response = {"message": "Success post review"}
  return jsonify(response), status.HTTP_200_OK

"""
REVIEW API: get all reviews for a babysitter
expected body: 
  username: the username of current user (parent)
  rating: an integer 1-5 for the babysitter
GET response: {INT} average rating of the sitter
POST response: success message
error: 400, 404 with message
"""
@app.route('/api/babysitter/<sitter_username>/rating', methods=['GET', 'POST'])
def rating(sitter_username):

  token1 = request.headers['Token1']
  token2 = request.headers['Token2']

  if hashing.Decrypted([token1, token2]) != True:
    response = {'error_message': 'HTTP_403_FORBIDDEN, cannot access'}
    return jsonify(response), status.HTTP_403_FORBIDDEN

  if handle['babysitter'].find_one({'username': sitter_username}) is None:
    response = {"err": "babysitter does not exist"}
    return jsonify(response), status.HTTP_404_NOT_FOUND

  if request.method == 'POST':

    form = request.get_json()

    if 'username' not in form:
      response = {"err": "should log in"}
      return jsonify(response), status.HTTP_400_BAD_REQUEST

    if 'rating' not in form:
      response = {"err": "must give rating"}
      return jsonify(response), status.HTTP_400_BAD_REQUEST

    currentuser_username = form['username']
    rating = int(form['rating'])

    if handle['user'].find_one({'username': currentuser_username}) is None:
      response = {"err": "no such user %s"%currentuser_username}
      return jsonify(response), status.HTTP_404_NOT_FOUND

    if rating < 1 or rating > 5:
      response = {"err": "rating should range from 1 to 5"}
      return jsonify(response), status.HTTP_400_BAD_REQUEST

    # all good, save rating in database
    handle.babysitter.update_one(
      {'username': sitter_username},
      {'$set': {'rating.%s'%currentuser_username: rating}})

    response = {"message": "success rating"}
    return jsonify(response), status.HTTP_200_OK

  # get average rating
  res = handle.babysitter.find_one(
    {'username': sitter_username}, 
    {'rating': 1, '_id': 0})

  # if no rating, respond with rating of 0
  if 'rating' not in res:
    avg_rating = 0
  else:
    ratings = res['rating']
    avg_rating = sum(ratings.values())/len(ratings)

  response = {'rating': avg_rating}
  return jsonify(response), status.HTTP_200_OK



#GET BABYSITTER PROFILE
@app.route('/api/babysitter/<sitter_username>/profile',methods=['GET'])
def profile_get(sitter_username):
  token1 = request.headers['Token1']
  token2 = request.headers['Token2']
  if hashing.Decrypted([token1, token2]) != True:
    response = {'error_message': 'HTTP_403_FORBIDDEN, cannot access'}
    return jsonify(response), status.HTTP_403_FORBIDDEN

  if sitter_username == None:
    response = {'error_message': 'request data should contain babysitter name'}
    return jsonify(response), status.HTTP_417_EXPECTATION_FAILED

  elif handle.babysitter.find_one({'username': sitter_username}) is None:
    response = {"err": "babysitter does not exist"}
    return jsonify(response), status.HTTP_404_NOT_FOUND
  else:
    cursor = handle.babysitter.find_one( {"username": sitter_username},projection={'profile':True, '_id': False})
    return dumps(cursor), status.HTTP_200_OK

#EDIT BABYSITTER PROFILE
@app.route('/api/babysitter/<sitter_username>/profile/edit',methods=['POST'])
def profile_edit(sitter_username):
  token1 = request.headers['Token1']
  token2 = request.headers['Token2']

  profile = form['profile']
  if hashing.Decrypted([token1, token2]) != True:
    response = {'error_message': 'HTTP_403_FORBIDDEN, cannot access'}
    return jsonify(response), status.HTTP_403_FORBIDDEN

  if sitter_username == None:
    response = {'error_message': 'request data should contain babysitter name'}
    return jsonify(response), status.HTTP_417_EXPECTATION_FAILED

  elif handle.babysitter.find_one({'username': sitter_username}) is None:
    response = {"err": "babysitter does not exist"}
    return jsonify(response), status.HTTP_404_NOT_FOUND
  else:
    handle.babysitter.update_one(
      {'username': sitter_username},
      {'$set': {'profile': profile}})
    cursor = handle.babysitter.find_one( {"username": sitter_username},projection={'profile':True, '_id': False})
    return dumps(cursor), status.HTTP_200_OK


#HELPER FUNCTIONS
#this function is called when first signed up as a babysitter
def profile_fillup(form):
  username = form['username']
  if 'profile' not in form:
    response = {'error_message': 'request data should contain babysitter profile'}
    return False, response
  
  if handle.babysitter.find({'username': username}).count() != 0:
    response = {'error_message': 'Babysitter already exists!'}
    return False, response
  
  profile = form['profile']
  if 'basic' not in profile or 'service' not in profile:
    response = {'error_message': 'profile should contain basic and service information'}
    return False, response
  if 'personal_info' not in profile['basic'] or 'contact_info' not in profile['basic']:
    response = {'error_message': 'basic profile should contain personal and contact information'}
    return False, response

  sitter = {
    'username':username,
    'profile':profile
  }
  handle.babysitter.insert(sitter)
  return True, "Success"


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8000)