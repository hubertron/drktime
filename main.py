import requests
import time
from datetime import datetime
import yaml

# Multi Threading for Noaa vs uptime
from threading import Thread



from noaa_sdk import noaa

# Inital setup
class bcolors:
    OKGREEN = '\33[32m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'

listUptime = []
printlistUptime = []
res1day = ""



headers = {
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'User-Agent': 'Mozilla/5.0 (Android 11; Mobile; rv:68.0) Gecko/68.0 Firefox/81.0',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
}

def get_servers():
  with open('servers.yaml') as f:
    servers = yaml.load(f, Loader=yaml.FullLoader)
    return servers

def monitor_servers(server):
  try:
    r = requests.get(server['address'], timeout=5, headers=headers )
    global status
    # How can I pass this to line 41 without using a global?
    status = r.status_code
    page_text = r.text
    status_detail = r.raise_for_status()
    search_string = server['search_string']
    if status != 200 or search_string not in page_text:
      with open('errors.txt', 'a') as file:
        print(server['name'], "with status", status, "missing search text '", search_string, "' at", datetime.now().strftime('%b %d %y %I:%M:%S %p'), file = file  )
        file.close()
      listUptime.append(server['name'] + ": " + str(status) +  bcolors.FAIL + " missing: " + search_string + bcolors.ENDC )
    else:
      listUptime.append(server['name'] + ": " + bcolors.OKGREEN + str(status) + bcolors.ENDC )
  except Exception as e:
    with open('errors.txt', 'a') as file:
      print(server['name'], "down with status", status, "at", datetime.now().strftime('%b %d %y %I:%M:%S %p'), " - ", e, file = file)
      file.close()
    listUptime.append(bcolors.FAIL + str(e) + bcolors.ENDC)

def getUptime():
  while True:
    global printlistUptime
    servers = get_servers()
    for server in servers:
        monitor_servers(server)
    #print(*listUptime, sep='\n')
    printlistUptime = listUptime
    return printlistUptime
    listUptime.clear()
    time.sleep( 60 )

def getLocation():
  with open('location.yaml') as f:
    location = yaml.load(f, Loader=yaml.FullLoader)
    zipcode = location[0]["zip"]
    country = location[0]["country"]
    return zipcode, country
      
def getWeather():
  locations = getLocation()
  global res1day
  n = noaa.NOAA()
  res = n.get_forecasts(locations[0], locations[1], False)
  res1day = res[0]["detailedForecast"]
  time.sleep( 10800 )

def displayEink():
 while True:
  time.sleep(60)
  print(res1day, '\n')
  currentDate = datetime.now().strftime('%a %b %d %-I:%M %p')
  print(currentDate, '\n')
  print(*printlistUptime, sep='\n')
  print('\n --- \n')
  
  


def main():
  Thread(target = getWeather).start()
  Thread(target = getUptime).start()
  Thread(target = displayEink).start()

if __name__ == '__main__':
    main()

# Docs
    # https://requests.readthedocs.io/en/master/user/quickstart/#response-status-codes



