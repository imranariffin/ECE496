from pymongo import MongoClient
from seed_data import ls_cities, ls_babysitters, ls_users

def initDB():
    url = "mongodb://user1:kuncikunci@ds141108.mlab.com:41108/baby"
    client = MongoClient(url) 
    return client['baby']

def setupDB():
  handle = initDB()

  # clear db of seed data
  for city in ls_cities: 
    handle['city'].delete_many({'city': city['city']})
  for sitter in ls_babysitters: 
    handle['babysitter'].delete_many({'host': sitter['host']})
  for user in ls_users:
    handle['user'].delete_many({'username': user['username']})

  # seed default city data
  handle['city'].insert(ls_cities)

  # seed default babysitter data
  handle['babysitter'].insert(ls_babysitters)
  #add to the host list for each city
  for item in ls_babysitters:
    handle['city'].update({'city': item['city']}, {'$push': {'hoster': item}})

  # seed default user data
  handle['user'].insert(ls_users)

  return handle