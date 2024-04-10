from datetime import datetime, timedelta
import requests
import pytz
from time import sleep

url = "https://ntfy.sh/haizi_ufuture_alert"

# myt = pytz.timezone('Asia/Kuala_Lumpur')

# nowMYT = datetime.now(myt)

# nowUTC = nowMYT.astimezone(pytz.utc)

# print(f"Malaysia Time: {nowMYT.strftime('%Y-%m-%d %H:%M:%S')}")
# print(f"UTC Time: {nowUTC.strftime('%Y-%m-%d %H:%M:%S')}")

# nowUTCfwd = nowUTC + timedelta(seconds = 30)

# requests.post(
#   url, 
#   headers={ 
#     "Title": 'Timezone noti on ' + nowMYT.strftime('%Y-%m-%d %H:%M:%S'),  
#     "At": f"{nowUTCfwd.strftime('%I:%M:%S %p')}",
#     }, 
#   data=f'{'Malaysia Time: ' + nowMYT.strftime("%Y-%m-%d %H:%M:%S") + ' UTC Time: ' + nowUTC.strftime("%Y-%m-%d %H:%M:%S")}'.encode(encoding='utf-8'))

# for i in range(30, 0, -1):
#   print('Noti will arrive in', i)
#   sleep(1)








requests.post(
  url, 
  headers={ 
    "Title": 'Timezone noti.',  
    "At": f"5:41:00",
    }, 
  data=f'{'Malaysia Time'}'
)


# ref: https://www.utctime.net/utc-to-myt-converter







#########################
### IGNORE CODE BELOW ###
#########################



# for i in range(-12, 13):
#   a = now - timedelta(hours = i) + timedelta(minutes = 1)
#   b = a.strftime("%I:%M:%S %p").lower()
#   c = a.strftime("%d/%m/%Y").lower()
#   print(c, b)

#   requests.post(
#         url, 
#         headers={ 
#           "Title": 'Timezone noti',  
#           "At": f"{b}",
#           }, 
#         data=f'{c + ' ' + b}'.encode(encoding='utf-8'))