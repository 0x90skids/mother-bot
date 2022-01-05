import requests
import memory
import datetime

def error():
  return '''
**Options:**
$test  -  Test bot
$event {eventID}  -  Track a new event
$ls {(optional) eventID}  -  List event/events
$rm {eventID}  -  Stop tracking an event
'''

def str_to_time(str):
  return datetime.datetime.fromisoformat(str).replace(second=0, microsecond=0)

def notify():
  keys = memory.getEvent()
  if not keys:
    return
  for key in keys:
    title = memory.getEvent(key)[0]
    url = memory.getEvent(key)[4]
    now = datetime.datetime.utcnow().replace(second=0, microsecond=0)
    start = str_to_time(memory.getEvent(key)[1]).replace(tzinfo=None) - now
    finish = now - str_to_time(memory.getEvent(key)[2]).replace(tzinfo=None)
    # if start = 1 day exactly 
    if datetime.timedelta(1) == start:
      return f'@everyone **{title}** starts in 24 hours! {url}'
    # if start = 2 h exactly 
    elif datetime.timedelta(0,0,0,0,0,2) == start:
      return f'@everyone **{title}** starts in 2 hours! {url}'
    # if start = 1 h exactly 
    elif datetime.timedelta(0,0,0,0,0,1) == start:
      return f'@everyone **{title}** starts in 1 hour! {url}'
    # if start = 1min STARTING NOW
    elif datetime.timedelta(0,0,0,0,1,0) == start:
      return f'@everyone **{title}** has started! {url}'
    # if finish = -1 day exactly
    elif datetime.timedelta(-1) == finish:
      return f'@everyone **{title}** ends in 24 hours! {url}'  
    # if finish = -12h
    elif datetime.timedelta(0,0,0,0,0,-12) == finish:
      return f'@everyone **{title}** ends in 12 hours! {url}'  
    # if finish = -1h
    elif datetime.timedelta(0,0,0,0,0,-1) == finish:
      return f'@everyone **{title}** ends in 1 hour! {url}'  
    # if finish = -1min ENDING NOW and delete
    elif datetime.timedelta(0,0,0,0,-1,0) <= finish:
      memory.deleteEvent(key)
      return f'@everyone **{title}** has ended! {url}'  
  return

def answer(*args):
  try:
    if args[0] == 'test':
      return 'I am not a bot, I am your mother.'
    elif args[0] == 'event':
      headers = {'user-agent':'bot'}
      r = requests.get(f'https://ctftime.org/api/v1/events/{int(args[1])}/', headers=headers)
      if r.status_code == 200:
        r = r.json()
        memory.addEvent(args[1], r['title'], r['start'], r['finish'], r['duration'], r['url'], r['ctftime_url'], r['format'], r['description'][:200]+'...')
      else:
        return 'Could not find that CTF Time event.'
      return f'Added new event: {r["title"]}!'
    elif args[0] == 'rm':
      memory.deleteEvent(args[1])
      return f'Event {args[1]} deleted.'
    elif args[0] == 'ls':
      if len(args) > 1:
        res = memory.getEvent(args[1])
        if not res:
          return f'Could not find an entry for {args[1]}'
        return f'''
**{res[0]}**
*Start*  -  {str(str_to_time(res[1]))[:-9]} UTC
*End*  -  {str(str_to_time(res[2]))[:-9]} UTC
*Duration*  -  {str(str_to_time(res[2]) - str_to_time(res[1]))[:-9]}
*URL*  -  {res[4]}
*CTF Time*  -  {res[5]}
*Format*  -  {res[6]}
*Description*  -  {res[7]}
'''
      else:
        keys = memory.getEvent()
        if not keys:
          return 'No events planned'
        res = ''
        for key in keys:
          event = memory.getEvent(key)
          res += key+' - '+event[0]+' - '+event[5]+'\n'
        return res
    else:
      return error()
  except Exception as e:
    print(f'User input: {args}, error: {e}')
    return error()