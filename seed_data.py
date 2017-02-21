
"""
seed city info
"""
ls_cities = [{
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

"""
seed babysitter info
"""
ls_babysitters = [{
  "username": "imran",
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
  # rating: integer from 0 to 5
  "rating": {
    # username: rating given by user
    'richard': 1,
    'parent1': 1,
    'parent2': 1,
  },
  "review": {
    "richard": {
      "title": "Not Happy",
      "value": "My kids are not happy with him",
      "date": {'month': 6, 'day': 14, 'year': 2014} 
    },
    "parent1": {
      "title": "Sad",
      "value": "My kids are very sad under his care",
      "date": {'month': 5, 'day': 14, 'year': 2015} 
    },
    "parent2": {
      "title": "Dislike",
      "value": "My kid dislikes staying here",
      "date": {'month': 8, 'day': 24, 'year': 2013} 
    },
  },
  "desc": "As of January 2012, Trust Child Care is under new ownership. As an owner, parent and primary educator I would invite you to please arrange for a tour so...",
  "url": "http://www.yelp.com/biz/trust-child-care-toronto-2?adjust_creative=dWycgaunp1RGGmO0t-TQTw&utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=dWycgaunp1RGGmO0t-TQTw",
  
  "profile":{
    "basic":{
        "personal_info": {
          "display_name": "Imran",
          "gender":"male",
          "profile_pic": "http://www.polyvore.com/cgi/img-thing?.out=jpg&size=l&tid=5376248",
          "cover_pic": "http://files.fbcoverstreet.com/content/lWwjEuiW6fzLAIuYztsVqyWAb7pZLau2h8pdfRveQCoIzhDsOQrSH9kw9vIHEJLf.jpg",
          "city": {
            "city":"Toronto",
            "prov_state": "Ontario",
          },  
          "education": "University of Toronto",
          "experience": "Worked at Sickkids for 8 years",
          "languages": [
            "English",
            "Malay",
            "Japanese",
            "Arabic"
          ]
        },
        "contact_info":{
          "email":"imran123@gmail.com",
          "phone":"647-888-1234",
          "website":"www.imran.com",
        },
    },
    "service":{
      "about":"hi, i am imran. I am an experienced babysitter who has 8 years of experience",
      "general_info":{
        "sitter_status":"part-time",
        "age_range": "5 to 10 years old",
        "service_location":"babysitter's house only",
        "pickup":"yes",
      },
      "price":{
        "weekday_hourly": 30.5,
        "weekend_hourly": 35.5,
        "security_deposit": 100,
      },
      "extra":{
        "free_parking":True,
        "wireless_internet":True,
        "air_condition":True,
        "child_education":True,
        "meal":False,
      },
      "policy":"no pets allowed",
    },

  },
}, 
{
  "username": "host1",
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
  # rating integer from 0 to 5
  "rating": {
    # username: rating given by user
    'richard': 5,
    'parent1': 5,
    'parent2': 5,
  },
  "review": {
    "richard": {
      "title": "Not Happy",
      "value": "My kids are not happy with him",
      "date": {'month': 6, 'day': 14, 'year': 2014} 
    },
    "parent1": {
      "title": "Sad",
      "value": "My kids are very sad under his care",
      "date": {'month': 5, 'day': 14, 'year': 2015} 
    },
    "parent2": {
      "title": "Dislike",
      "value": "My kid dislikes staying here",
      "date": {'month': 8, 'day': 24, 'year': 2013} 
    },
  },
  "desc": "My son has been a member of Gloria's family since January 2013 and his has thrived in this home based nurturing home daycare environment. Gloria has been an...",
  "url": "http://www.yelp.com/biz/play-n-stay-daycare-toronto?adjust_creative=dWycgaunp1RGGmO0t-TQTw&utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=dWycgaunp1RGGmO0t-TQTw",
  "profile":{
    "basic":{
        "personal_info": {
          "display_name": "Host 1",
          "gender":"male",
          "profile_pic": "http://res.cloudinary.com/rrigrp/image/upload/v1483392914/gxxpnb3e7ohmbviknihj.jpg",
          "cover_pic": "http://res.cloudinary.com/rrigrp/image/upload/v1483375032/sample.jpg",
          "city": {
            "city":"Toronto",
            "prov_state": "Ontario",
          },  
          "education": "University of Toronto",
          "experience": "Worked at Sickkids for 8 years",
          "languages": [
            "French"
          ],
        },
        "contact_info":{
          "email":"imran123@gmail.com",
          "phone":"647-888-1234",
          "website":"www.imran.com",
        },
    },
    "service":{
      "about":"hi, i am imran. I am an experienced babysitter who has 8 years of experience",
      "general_info":{
        "sitter_status":"part-time",
        "age_range": "5 to 10 years old",
        "service_location":"babysitter's house only",
        "pickup":"yes",
      },
      "price":{
        "weekday_hourly": 30.5,
        "weekend_hourly": 35.5,
        "security_deposit": 100,
      },
      "extra":{
        "free_parking":True,
        "wireless_internet":True,
        "air_condition":True,
        "child_education":True,
        "meal":False,
      },
      "policy":"no pets allowed",
    },
  },
}, {
  'username': 'host2',
  'desc': 'Host with no rating',
  'host': "Host with no rating",
  'city': 'Toronto',
  "profile":{
    "basic":{
        "personal_info": {
          "display_name": "Host 2",
          "gender":"male",
          "profile_pic": "http://res.cloudinary.com/rrigrp/image/upload/v1483392914/gxxpnb3e7ohmbviknihj.jpg",
          "cover_pic": "http://res.cloudinary.com/rrigrp/image/upload/v1483375032/sample.jpg",
          "city": {
            "city":"Toronto",
            "prov_state": "Ontario",
          },  
          "education": "University of Toronto",
          "experience": "Worked at Sickkids for 8 years",
          "languages": [
            "English",
            "Mandarin"
          ]
        },
        "contact_info":{
          "email":"imran123@gmail.com",
          "phone":"647-888-1234",
          "website":"www.imran.com",
        },
    },
    "service":{
      "about":"hi, i am imran. I am an experienced babysitter who has 8 years of experience",
      "general_info":{
        "sitter_status":"part-time",
        "age_range": "5 to 10 years old",
        "service_location":"babysitter's house only",
        "pickup":"yes",
      },
      "price":{
        "weekday_hourly": 30.5,
        "weekend_hourly": 35.5,
        "security_deposit": 100,
      },
      "extra":{
        "free_parking":True,
        "wireless_internet":True,
        "air_condition":True,
        "child_education":True,
        "meal":False,
      },
      "policy":"no pets allowed",
    },
  },
}]

"""
seed user info
"""
ls_users = [{
  'username': 'imran',
  'password': 'password',
  'host': True
}, {
  'username': 'richard',
  'password': 'password',
  'host': False
}, {
  'username': 'parent1',
  'password': 'password',
  'host': False  
}, {
  'username': 'parent2',
  'password': 'password',
  'host': False  
}, {
  'username': 'host1',
  'password': 'password',
  'host': True
}, {
  'username': 'host2',
  'password': 'password',
  'host': True
}]

'''
parent seed
'''
ls_parents = [{
  'username':'parent1',
  'profile_pic':'https://v.cdn.vine.co/r/avatars/8FA8F516C61211899383466061824_pic-r-14319135186558d72e0b19d.jpg.jpg?versionId=ZAYQev_ezlElQYl00cirvmi8LUg_TJnA'
}]

'''
babysitter payment info
'''
ls_sitterpayments = [{
 'username':'dummy',
 'secret_key':'',
 'publishable_key':'' 
},
    {"username": "imran",
    "access_token": "sk_test_yBDhdmlkIJ6HlSwVNTK3veK2",
    "publishable_key": "pk_test_PC3gAzSYv5pLRjmanrIdJbRq",
    "stripe_id": "acct_19pk8mBXl5tvlOhX"}
]