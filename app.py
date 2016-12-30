from flask import Flask, url_for, json, request, send_file, jsonify, Response

#print data formating
import pprint

import dbsetup

# create random key
from os import urandom

# http status return
from flask_api import status

app = Flask(__name__)

#setupDB
handle = dbsetup.setupDB()

"""
response: status: 200, 401, 404
200: success login
401: wrong password
404: user not exist
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
      'user': username
    }
    return jsonify(response), status.HTTP_200_OK


@app.route("/api/logout", methods=['POST'])
def logout():
  # response: status: 200
  #   200: success
  form = request.get_json()
  if form == None or len(form) == 0 or 'username' not in form:
    response = {'error_message': 'bad request, need to have username as in data'}
    return jsonify(response), status.HTTP_417_EXPECTATION_FAILED

  username = form['username']
  if handle.user.find({'username': username}).count() == 0:
    response = {'error_message': 'user not found'}
    return jsonify(response), status.HTTP_404_NOT_FOUND

  response = {'message': 'success logout'}
  return jsonify(response), status.HTTP_200_OK

@app.route("/")
def mainPage():
  return send_file("templates/index.html")

#find all the cities and host for initial map
@app.route('/api/city')
def city():
  cursor = handle.city.find()
  return jsonify(cursor)

#return all the info or one city
@app.route('/api/find/babysitter/<name>', methods = ['GET'])
def getBabysitterInfo(name):
  if name != None:
    cursor = handle.babysitter.find( {"city": name} )
    return jsonify(cursor)
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

"""
REVIEW API: get all reviews for a babysitter
response: list of review string with respective reviewer username
error: 400, 404 with message
"""
@app.route('/api/babysitter/<sitter_username>/review', methods=['GET', 'POST'])
def get_babysitter_review_list(sitter_username):
  
  if request.method == 'GET':

    babysitter = handle['babysitter'].find_one({'username': sitter_username})

    if babysitter is None:
      response = {"err": "Error 404: No babysitter with such username %s"%sitter_username}
      return jsonify(response), status.HTTP_404_NOT_FOUND

    ls_reviews = [{
      'username': parent, 
      'value': babysitter['review'][parent]['value']
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

  if handle['user'].find_one({'username': form['username']}) is None:
    # error, user should exist
    response = {"err": "user does not exist"}
    return jsonify(response), status.HTTP_400_BAD_REQUEST

  # add current user's review for babysitter
  review = form['review']
  currentuser_username = form['username']

  # babysitter['review'][currentuser_username] = review
  res = handle['babysitter'].update_one(
      {"username": sitter_username},
      {"$set": {
        "review.%s"%currentuser_username: {"value": review}
      }})

  if res.matched_count == 0:
    # error, babysitter doesn't exist
    response = {"err": "babysitter %s doesn't exist"%sitter_username}
    return jsonify(response), status.HTTP_400_BAD_REQUEST

  response = {"message": "Success post review"}
  return jsonify(response), status.HTTP_200_OK

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8000)