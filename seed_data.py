
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
      "value": "My kids are not happy with him",
    },
    "parent1": {
      "value": "My kids are very sad under his care",
    },
    "parent2": {
      "value": "My kid dislikes staying here",
    },
  },
  "desc": "As of January 2012, Trust Child Care is under new ownership. As an owner, parent and primary educator I would invite you to please arrange for a tour so...",
  "url": "http://www.yelp.com/biz/trust-child-care-toronto-2?adjust_creative=dWycgaunp1RGGmO0t-TQTw&utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=dWycgaunp1RGGmO0t-TQTw"
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
      "value": "My kids are happy with him",
    },
    "parent1": {
      "value": "My kids are very happy under his care",
    },
    "parent2": {
      "value": "My kid likes so staying here so much",
    },
  },
  "desc": "My son has been a member of Gloria's family since January 2013 and his has thrived in this home based nurturing home daycare environment. Gloria has been an...",
  "url": "http://www.yelp.com/biz/play-n-stay-daycare-toronto?adjust_creative=dWycgaunp1RGGmO0t-TQTw&utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=dWycgaunp1RGGmO0t-TQTw"
}, {
  'username': 'host2',
  'desc': 'Host with no rating',
  'host': "Host with no rating",
  'city': 'Toronto'
}]

"""
seed user info
"""
ls_users = [{
  'username': 'imran',
  'password': 'password',
  'Host': True
}, {
  'username': 'richard',
  'password': 'password',
  'Host': False
}, {
  'username': 'parent1',
  'password': 'password',
  'Host': False  
}, {
  'username': 'parent2',
  'password': 'password',
  'Host': False  
}, {
  'username': 'host1',
  'password': 'password',
  'Host': True
}, {
  'username': 'host2',
  'password': 'password',
  'Host': True
}]