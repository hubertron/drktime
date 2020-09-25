import requests
import time
from datetime import datetime
import yaml



def get_servers():
  with open('servers.yaml') as f:
    servers = yaml.load(f, Loader=yaml.FullLoader)
    return servers

def monitor_servers(server):
  try:
    r = requests.get(server['address'], timeout=5)
    status = r.status_code
    page_text = r.text
    status_detail = r.raise_for_status()
    search_string = server['search_string']
    if status != 200 or search_string not in page_text:
       with open('errors.txt', 'a') as file:
        print(server['name'], "with status", status, "missing search text '", search_string, "' at", datetime.now().strftime('%b %d %y %I:%M:%S %p'), file = file  )
        file.close()
  except Exception as e:
    with open('errors.txt', 'a') as file:
      print(server['name'], "down with status", status, "at", datetime.now().strftime('%b %d %y %I:%M:%S %p'), " - ", e, file = file)
      file.close()


try:
    servers = get_servers()
except Exception as e:
    print(e)
except KeyboardInterrupt:
  pass
else:
    while True:
      for server in servers:
          monitor_servers(server)
      print("Sleeping")
      time.sleep( 60 )





# Docs
    # https://requests.readthedocs.io/en/master/user/quickstart/#response-status-codes



