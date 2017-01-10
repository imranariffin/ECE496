from pymongo import MongoClient
from seed_data import ls_cities, ls_babysitters, ls_users, ls_parents

def initDB():
    url = "mongodb://user1:kuncikunci@ds141108.mlab.com:41108/baby"
    client = MongoClient(url) 
    return client['baby']

def setupDB():
  handle = initDB()

  # clear db of seed data

  handle['city'].remove({})

  handle['babysitter'].remove({})

  handle['user'].remove({})

  handle['parent'].remove({})

  # seed default city data
  handle['city'].insert(ls_cities)

  # seed default babysitter data
  handle['babysitter'].insert(ls_babysitters)
  #add to the host list for each city
  for item in ls_babysitters:
    handle['city'].update({'city': item['city']}, {'$push': {'hoster': item}})

  # seed default user data
  handle['user'].insert(ls_users)

  # seed default parent data
  handle['parent'].insert(ls_parents)

  return handle