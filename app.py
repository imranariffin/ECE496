from flask import Flask, url_for, json, request, send_file, jsonify, Response,render_template, redirect

from bson.json_util import dumps

#print data formating
import pprint

import dbsetup

# create random key
import os
from os import urandom

# http status return
from flask_api import status

#hashing for token
import hashing

#for the review system
import datetime

#cloudinary
import cloudinary
from cloudinary.uploader import upload,destroy
from cloudinary.utils import cloudinary_url





cloudinary.config(
  cloud_name = 'rrigrp',
  api_key = '498192978171332',
  api_secret = "F1NecNDuIBOTu8-TlwGwXQMRxkA"
)

#Regex
import re

#Stripe Payment Credentials
import requests
import urllib
import stripe
stripe_keys = {
  'secret_key': 'sk_live_OOOPWm8PBwB830QuWilKhxAp',
  'publishable_key': 'pk_live_RtNLSTZHCgoJrN3Ne6FMC5hH',
  'client_id': 'ca_9ueSVIxaEMsjbkhuTqRVhmigZVYwruYH'
}
stripe.api_key = stripe_keys['secret_key']

#Global username for payment use
glob_username = None


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

  #save global username for payment
  global glob_username
  glob_username = username

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

  #Clear Global username
  global glob_username
  glob_username = None

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
  
  missing_something = (
    'username' not in form or 
    'password' not in form or 
    'host' not in form or 
    not (
      form['host'] == 'parent' or 
      form['host'] == 'babysitter'
    )
  )
  if missing_something:
    response = {'error_message': 'Some information is missing'}
    return jsonify(response), status.HTTP_417_EXPECTATION_FAILED

  if form['password'] != form['confirmPassword']:
    response = {'error_message': 'request data should contain username and password'}
    return jsonify(response), status.HTTP_406_NOT_ACCEPTABLE

  username = form['username']
  password = form['password']

  #save global username for payment
  global glob_username
  glob_username = username

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
      'host': form['host']
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
      response = {"error_message": "Error 404: No babysitter with such username %s"%sitter_username}
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
    response = {"error_message": "Should log in"}
    return jsonify(response), status.HTTP_400_BAD_REQUEST

  if 'review' not in form or form['review'] == "":
    # error, review should not be empty
    response = {"error_message": "Review should not be empty"}
    return jsonify(response), status.HTTP_400_BAD_REQUEST

  if 'title' not in form or form['title'] == "":
    # error, review should not be empty
    response = {"error_message": "Review title should not be empty"}
    return jsonify(response), status.HTTP_400_BAD_REQUEST

  if handle['user'].find_one({'username': form['username']}) is None:
    # error, user should exist
    response = {"error_message": "user does not exist"}
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
    response = {"error_message": "babysitter %s doesn't exist"%sitter_username}
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
    response = {"error_message": "babysitter does not exist"}
    return jsonify(response), status.HTTP_404_NOT_FOUND

  if request.method == 'POST':

    form = request.get_json()

    if 'username' not in form:
      response = {"error_message": "should log in"}
      return jsonify(response), status.HTTP_400_BAD_REQUEST

    if 'rating' not in form:
      response = {"error_message": "must give rating"}
      return jsonify(response), status.HTTP_400_BAD_REQUEST

    currentuser_username = form['username']
    rating = int(form['rating'])

    if handle['user'].find_one({'username': currentuser_username}) is None:
      response = {"error_message": "no such user %s"%currentuser_username}
      return jsonify(response), status.HTTP_404_NOT_FOUND

    if rating < 1 or rating > 5:
      response = {"error_message": "rating should range from 1 to 5"}
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

#BABYSITTER PROFILE UPLOAD/EDIT
@app.route('/api/babysitter/<sitter_username>/profile_upload',methods=['POST'])
def sitter_profile_upload(sitter_username):
  form = json.loads(request.headers['Json'])
  token1 = request.headers['Token1']
  token2 = request.headers['Token2']

  if hashing.Decrypted([token1, token2]) != True:
    response = {'error_message': 'HTTP_403_FORBIDDEN, cannot access'}
    return jsonify(response), status.HTTP_403_FORBIDDEN

  org_profile_pic = None
  org_cover_pic = None
  Edit = False  #True if this is an Edit request; otherwise it is the first time upload
  if handle.babysitter.find({'username': sitter_username}).count() != 0:
    Edit = True
    cursor = handle.babysitter.find_one({'username':sitter_username})
    org_profile_pic = cursor['profile']['basic']['personal_info']['profile_pic']
    org_cover_pic = cursor['profile']['basic']['personal_info']['cover_pic']
    handle.babysitter.delete_many({'username': sitter_username})

  #upload pictures and get pic urls
  upload_result = None
  profile_pic_url = None
  cover_pic_url = None

  print "before files"

  profile_pic = request.files['profile_pic'] if 'profile_pic' in request.files else None
  cover_pic = request.files['cover_pic'] if 'cover_pic' in request.files else None

  print profile_pic, cover_pic

  #delete existing profile/cover pictures
  if profile_pic:
    print "delete profile pic"
    if org_profile_pic != None:
      match = re.search('.*\/(\S+)\.\S+', org_profile_pic)
      if match:
        public_id = match.group(1)
        delete_res = destroy(public_id)
  if cover_pic:
    print "delete cover pic"
    if org_cover_pic != None:
      match = re.search('.*\/(\S+)\.\S+', org_cover_pic)
      if match:
        public_id = match.group(1)
        delete_res = destroy(public_id)

  print "after files"

  if profile_pic:
    upload_result = upload(profile_pic)
    profile_pic_url  = upload_result['url']
  if cover_pic:
    upload_result = upload(cover_pic)
    cover_pic_url = upload_result['url']

  if profile_pic_url != None:
    form['profile']['basic']['personal_info']['profile_pic'] = profile_pic_url
  elif not Edit:
    form['profile']['basic']['personal_info']['profile_pic'] = ""
  if cover_pic_url != None:
    form['profile']['basic']['personal_info']['cover_pic'] = cover_pic_url
  elif not Edit:
    form['profile']['basic']['personal_info']['cover_pic'] = ""
  
  #upload the profile body
  success,response=profile_fillup(form,sitter_username,Edit)
  if not success:
    return jsonify(response), status.HTTP_417_EXPECTATION_FAILED
  else:
    return jsonify(response), status.HTTP_200_OK

#PARENT PROFILE UPLOAD/EDIT
@app.route('/api/parent/<parent_username>/profile_upload',methods=['POST'])
def parent_profile_upload(parent_username):
  form = json.loads(request.headers['Json'])
  token1 = request.headers['Token1']
  token2 = request.headers['Token2']

  if hashing.Decrypted([token1, token2]) != True:
    response = {'error_message': 'HTTP_403_FORBIDDEN, cannot access'}
    return jsonify(response), status.HTTP_403_FORBIDDEN

  org_profile_pic = None
  Edit = False  #True if this is an Edit request; otherwise it is the first time upload
  if handle.parent.find({'username': parent_username}).count() != 0:
    Edit = True
    cursor = handle.parent.find_one({'username':parent_username})
    org_profile_pic = cursor['profile_pic']
    handle.parent.delete_many({'username': parent_username})

  #delete existing profile/cover pictures
  if org_profile_pic != None:
    match = re.search('.*\/(\S+)\.\S+', org_profile_pic)
    if match:
      public_id = match.group(1)
      delete_res = destroy(public_id)

  #upload pictures and get pic urls
  upload_result = None
  profile_pic_url = None
  profile_pic = request.files['profile_pic']
  if profile_pic:
    upload_result = upload(profile_pic)
    profile_pic_url  = upload_result['url']

  if profile_pic_url != None:
    form['profile_pic'] = profile_pic_url
  else:
    form['profile_pic'] = ""
  
  #upload the profile body
  parent = {
    'username':parent_username,
    'profile_pic':form['profile_pic']
  }
  handle.parent.insert(parent)
  if Edit == True:
    response={"message":"successfully updated parent profile"}
  else:
    response={"message":"successfully inserted parent profile"}
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
    response = {"error_message": "babysitter does not exist"}
    return jsonify(response), status.HTTP_404_NOT_FOUND
  else:
    cursor = handle.babysitter.find_one( {"username": sitter_username},projection={'profile':True, '_id': False})
    return dumps(cursor), status.HTTP_200_OK


#GET PROFILE PICTURE ICON
@app.route('/api/<username>/profile_pic',methods=['GET'])
def get_profile_pic(username):
  token1 = request.headers['Token1']
  token2 = request.headers['Token2']

  if hashing.Decrypted([token1, token2]) != True:
    response = {'error_message': 'HTTP_403_FORBIDDEN, cannot access'}
    return jsonify(response), status.HTTP_403_FORBIDDEN

  if handle.user.find_one({'username': username}) is None:
    response = {"error_message": "user does not exist"}
    return jsonify(response), status.HTTP_404_NOT_FOUND

  user_type = handle.user.find_one( {"username": username},projection={'host':True, '_id': False})
  host = user_type['host']
  if host == True:
    cursor = handle.babysitter.find_one( {"username": username},projection={'profile':True, '_id': False})
    profile_pic = {"profile_pic":cursor['profile']['basic']['personal_info']['profile_pic']}
    return dumps(profile_pic), status.HTTP_200_OK
  else:
    cursor = handle.parent.find_one( {"username": username},projection={'profile_pic':True, '_id': False})
    return dumps(cursor), status.HTTP_200_OK


#PASSWORD CHANGE
@app.route('/api/password_change',methods=['POST'])
def pw_change():
  token1 = request.headers['Token1']
  token2 = request.headers['Token2']

  if hashing.Decrypted([token1, token2]) != True:
    response = {'error_message': 'HTTP_403_FORBIDDEN, cannot access'}
    return jsonify(response), status.HTTP_403_FORBIDDEN

  form = request.get_json()
  if 'username' not in form or 'org_pw' not in form or 'new_pw' not in form or 'new_pw_conf' not in form:
    response = {'error_message': 'request data should contain username, the orginal password, new password and the confirmed new password'}
    return jsonify(response), status.HTTP_417_EXPECTATION_FAILED

  username = form['username']
  org_pw = form['org_pw']
  new_pw = form['new_pw']
  new_pw_conf = form['new_pw_conf']

  result = handle.user.find({'username': username})
  if result.count() == 0:
    response = {'error_message': 'user does not exist'}
    return jsonify(response), status.HTTP_404_NOT_FOUND
  elif list(result)[0]["password"] != org_pw:
    response = {'error_message': 'wrong password'}
    return jsonify(response), status.HTTP_401_UNAUTHORIZED
  elif new_pw != new_pw_conf:
    response = {'error_message': 'Confirmed new password does not match the new password'}
    return jsonify(response), status.HTTP_417_EXPECTATION_FAILED
  elif org_pw == new_pw:
    response = {'error_message': 'New password is the same as the old one'}
    return jsonify(response), status.HTTP_417_EXPECTATION_FAILED
  else:
    handle.user.update_one(
      {'username': username},
      {'$set': {'password': new_pw}})
    response = {
      'message': 'successfully changed password',
      'session_token': hashing.Encrypted(username+new_pw),
    }
    return jsonify(response), status.HTTP_200_OK

#AUTHORIZE STRIPE CONNECTION
@app.route('/api/payment_authorize')
def authorize():
  site   = "https://connect.stripe.com/oauth/authorize"
  params = {
             'response_type': 'code',
             'scope': 'read_write',
             'client_id': stripe_keys['client_id']
           }

  # Redirect to Stripe /oauth/authorize endpoint
  url = site + '?' + urllib.urlencode(params)
  return redirect(url)


#SAVE PAYMENT ACCOUNT INFO IN THE DATABASE
@app.route('/api/payment_callback')
def connect_payment_account():
  #do this after authorization
  code   = request.args.get('code')
  data   = {
             'client_secret': stripe_keys['secret_key'],
             'grant_type': 'authorization_code',
             'client_id': stripe_keys['client_id'],
             'code': code
           }

  # Make /oauth/token endpoint POST request
  url = 'https://connect.stripe.com/oauth/token'
  resp = requests.post(url, params=data)

  # Get User ID
  stripe_id = resp.json().get('stripe_user_id')
  # Get access_token
  token = resp.json().get('access_token')
  # Grap publishable_key
  p_key = resp.json().get('stripe_publishable_key')

  if glob_username == None:
    response = {'error_message': 'username not defined'}
    return jsonify(response), status.HTTP_404_NOT_FOUND
  
  #CHECK IF THE PAYMENT INFO EXIST
  if handle.payment.find({'username': glob_username}).count() != 0:
    response = {'error_message': 'username exists in DB'}
    return render_template('paymentConnectFail.html') 
  
  #Store the information into the database
  payment = {
    'username': glob_username,
    'stripe_id': stripe_id,
    'access_token': token,
    'publishable_key': p_key
  }
  handle.payment.insert(payment)

  return render_template('paymentConnectSuccess.html')

#SET UP A PAYMENT
@app.route('/api/payment/<username>/<amount>')
def payment(username,amount):
  amount_in_dollor = float(amount)/100
  return render_template('charge.html',key=stripe_keys['publishable_key'],username=username,amount=amount,amount_in_dollor=amount_in_dollor)

#CHARGE THE MONEY
@app.route('/api/charge/<username>/<amount>', methods=['POST'])
def charge(username,amount):
    payment_info=handle.payment.find_one({'username':username})
    account = payment_info['stripe_id']

    charge = stripe.Charge.create(
        source=request.form['stripeToken'],
        amount=amount,
        currency='cad',
        description='Babysitting Charge',
        stripe_account=account
    )
    return redirect('/#')


#SEARCH ACTIONS -> by filter
@app.route('/api/<parent>/SearchByFilter/<rating>/<price>/<distance>',methods=['GET'])
def search_by_filter(parent,rating,price,distance):
  token1 = request.headers['Token1']
  token2 = request.headers['Token2']

  if hashing.Decrypted([token1, token2]) != True:
    response = {'error_message': 'HTTP_403_FORBIDDEN, cannot access'}
    return jsonify(response), status.HTTP_403_FORBIDDEN

  #RATING FILTER
  all_sitters = [b for b in handle.babysitter.find()]
  avgrating = lambda ls_rating: reduce(lambda e, n: e+n, ls_rating.values())/float(len(ls_rating))
  rating_result = [b for b in all_sitters if 'rating' in b and avgrating(b['rating']) >= int(rating)]
  rating_dict = {b['username']: avgrating(b['rating']) for b in all_sitters if 'rating' in b and avgrating(b['rating']) >= int(rating)}

  #print "rating result ---------------",[rating_result[n]['username'] for n in range(len(rating_result))]
  #print "RATING DICT:-------------",rating_dict

  #PRICE FILTER
  price_range = {'1': 20,'2':30,'3':40}
  if int(price) > 0 and int(price) < 4:
    price_result = [b for b in rating_result if b['profile']['service']['price']['weekday_hourly'] <= price_range[price]]
  elif int(price) == 4:
    price_result = [b for b in rating_result if b['profile']['service']['price']['weekday_hourly'] > 40]
  else:
    price_result = rating_result
  
  #print "price result ---------------", dumps([price_result[n]['username'] for n in range(len(price_result))])
  
  #DISTANCE FILTER
  distance_range = {'1': (0,1000),'2':(1001,2000),'3':(2001,5000),'4':(5001,10000)}
  if handle.parent.find_one({"username":parent}) is None:
    response = {"error_message": "user does not exist"}
    return jsonify(response), status.HTTP_404_NOT_FOUND

  p = handle.parent.find_one({"username":parent})
  #parent address
  parent_addr = p['addr']['addr'] +' '+ p['addr']['prov_state']
  dist_result = []
  for b in price_result:
    #sitter address
    sitter_addr = b['profile']['basic']['personal_info']['addr']['addr'] + ' '+ b['profile']['basic']['personal_info']['addr']['prov_state']
    #CALCULATE DISTANCE
    googlemap_api_url = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins='+ parent_addr +'&destinations='+sitter_addr+'&mode=driving&language=en-US&key=AIzaSyD3xxYrQTk4eCQajHxacHVlcR9QXvpr1uM'
    r = requests.get(googlemap_api_url).json()
    dist = r['rows'][0]['elements'][0]['distance']['value']
    b['distance'] = dist
    
    if int(distance) > 0 and int(distance) < 5:
      if distance_range[distance][0] <= dist and dist <= distance_range[distance][1]:
        dist_result.append(b)
    elif int(distance) == 5:
      if dist > 10000:
        dist_result.append(b)
    else:
      dist_result.append(b)

  response = []
  for item in dist_result:
    newObj = { 
      "name":  item['profile']['basic']['personal_info']['display_name'],
      "username": item["username"],
      "city": item["city"],
      "address": item['profile']['basic']['personal_info']['addr']['addr']+' '+item['profile']['basic']['personal_info']['addr']['prov_state'],
      "phone": item["phone"],
      "distance": item["distance"],
      "price": item['profile']['service']['price']['weekday_hourly'],
      "rating": rating_dict[item["username"]]
    }
    response.append(newObj)

  #Sort Response by username
  response = sorted(response, key=lambda k: k['name']) 

  return jsonify(response), status.HTTP_200_OK



#HELPER FUNCTIONS
#this function is called when first signed up as a babysitter
def profile_fillup(form,username,edit):
  #username = form['username']
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
  if edit == True:
    response = {'message': 'successfully updated babysitter profile'}
  else:
    response = {'message': 'successfully inserted babysitter profile'}
  return True, response

@app.route('/api/user/<username>', methods=["GET"])
def get_user(username):
  token1 = request.headers['Token1']
  token2 = request.headers['Token2']

  if hashing.Decrypted([token1, token2]) != True:
    response = {'error_message': 'HTTP_403_FORBIDDEN, cannot access'}
    return jsonify(response), status.HTTP_403_FORBIDDEN

  user = handle['user'].find_one(
    {'username': username}, 
    projection={'_id': False})
  if user is None:
    response = {'error_message': 'user does not exist!'}
    return jsonify(response), status.HTTP_404_NOT_FOUND

  response = {'user': user}
  return jsonify(response), status.HTTP_200_OK

@app.route('/api/parent/<parent_username>/address', methods=['GET', 'POST'])
def parent_address(parent_username):
  token1 = request.headers['Token1']
  token2 = request.headers['Token2']

  if hashing.Decrypted([token1, token2]) != True:
    response = {'error_message': 'HTTP_403_FORBIDDEN, cannot access'}
    return jsonify(response), status.HTTP_403_FORBIDDEN

  if request.method == 'GET':

    parent_address = handle.parent.find_one(
      {'username': parent_username}, 
      projection={'addr':True, '_id': False}
    )

    if not parent_address:
      response = {"error_message": "parent %s doesn't exist"%parent_username}
      return jsonify(response), status.HTTP_400_BAD_REQUEST

    return jsonify(parent_address), status.HTTP_200_OK

  addr = request.get_json()['addr']
  res = handle['parent'].update_one(
    {"username": parent_username},
    {"$set": {
      "addr": addr
    }})

  if res.matched_count == 0:
    # error, babysitter doesn't exist
    response = {"error_message": "parent %s doesn't exist"%parent_username}
    return jsonify(response), status.HTTP_400_BAD_REQUEST

  response = {"message": "Success update parent address"}
  return jsonify(response), status.HTTP_200_OK

#SEARCH ACTIONS -> by name 
@app.route('/api/SearchByName/<displayName>',methods=['GET'])
def search_by_name(displayName):
  token1 = request.headers['Token1']
  token2 = request.headers['Token2']

  if hashing.Decrypted([token1, token2]) != True:
    response = {'error_message': 'HTTP_403_FORBIDDEN, cannot access'}
    return jsonify(response), status.HTTP_403_FORBIDDEN

  if handle.babysitter.find({'profile.basic.personal_info.display_name': {'$regex': re.compile(displayName, re.IGNORECASE)}}) is None:
    response = {"error_message": "user does not exist"}
    return jsonify(response), status.HTTP_404_NOT_FOUND

  result = handle.babysitter.find({'profile.basic.personal_info.display_name': {'$regex': re.compile(displayName, re.IGNORECASE)}})

  response = []
  for item in result:
    #print  displayName, item["username"], item['city']
    newObj = { 
      "name":  item['profile']['basic']['personal_info']['display_name'],
      "username": item["username"],
      "phone": item['profile']['basic']['contact_info']['phone'],
      "city": item["city"]
    }
    response.append(newObj)

  return jsonify(response), status.HTTP_200_OK

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8000)