from replit import db

def addEvent(id, title, start, end, duration, url, ctftime_url, format, description):

  db[id] = [title, start, end, duration, url, ctftime_url, format, description]
  return

def deleteEvent(id):
  if id in db:
    del db[id]
    return
  return False

def getEvent(id=None):
  if not id:
    if not db.keys():
      return False
    return db.keys().copy()
  if id in db:
    return db[id].value
  return False