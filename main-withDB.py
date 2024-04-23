import argparse
from colorama import just_fix_windows_console
just_fix_windows_console()
from colorama import Fore, Back, Style
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from tomllib import load
import requests
import re
from datetime import datetime
from datetime import timedelta
import sqlite3
from time import sleep
import os

credential = 'credentials.toml'
db_name = 'test.db'




########################
### SYSTEM ARGUMENTS ###
########################

parser = argparse.ArgumentParser(description="This script access your Ufuture and if any notification about online class present, ntfy.sh will push it to your mobile device, granted you install ntfy.sh and configure same server name with your config.")

parser.add_argument('--test', action='store_true', help='Run this script in a test environment.')
parser.add_argument('--debug', action='store_true', help='Also print DEBUG logs.')
parser.add_argument('--headful', action='store_true', help='Run selenium in headful mode.')
parser.add_argument('--idiscuss', action='store_true', help='Access i-Discuss.')
parser.add_argument('--dryrun', action='store_true', help='Disables ntfy posting.')
parser.add_argument('--donotdeletedb', action='store_true', help="Don't delete db file after keyboardInterrupt. Please remove the db file before running the script again.")

args = parser.parse_args()




###################
### DRIVER INIT ###
###################

def drivers():
  options = webdriver.FirefoxOptions()
  options.set_preference('permissions.default.image', 2)

  if not args.headful:   ### user wants headless mode
    options.add_argument("-headless")
  
  driver = webdriver.Firefox(options=options)
  actions = ActionChains(driver)

  return (driver, actions) # this is a tuple








###############################################
### LOAD AND RETURN CREDENTIALS INFORMATION ###
###############################################

def credentials(credential_filename:str, return_type:str):
  
  with open(credential_filename, "rb") as a:
    data = load(a)

  if return_type == 'username':
    return data["login"]["username"]
  elif return_type == 'password':
    return data["login"]["password"]
  elif return_type == 'ntfyserver':
    return data["ntfyServer"]["url"]
  






########################
### LOGGING FUNCTION ###
########################

def log(level:str, message:str):   
  if args.debug or level != 'debug':
    print(Back.WHITE, end='')
    print(Fore.BLACK + f' LOG ', end='')
    print(Style.RESET_ALL, end='')
  
  if level == 'debug':
    if args.debug:
      print(Back.BLUE, end='')
      print(Fore.BLACK + f' DEBUG ', end='')
      print(Style.RESET_ALL, end='')
    else: return

  elif level == 'info':
    print(Back.CYAN, end='')
    print(Fore.BLACK + f' INFO ', end='')
    print(Style.RESET_ALL, end='')

  elif level == 'print':
    print(Back.MAGENTA, end='')
    print(Fore.BLACK + f' PRINT ', end='')
    print(Style.RESET_ALL, end='')
  
  elif level == 'interrupt':
    print(Back.RED, end='')
    print(Fore.WHITE + f' INTERRUPT ', end='')
    print(Style.RESET_ALL, end='')
  
  elif level == 'warn':
    print(Back.YELLOW, end='')
    print(Fore.BLACK + f' WARN ', end='')
    print(Style.RESET_ALL, end='')
  
  print(f' {message}')
  






##################################
### NAVIGATE TO ONLINE CLASSES ###
##################################

(driverl, actionl) = drivers()  # driver declaration

def navigate(what_to_return:str):
  
  e = driverl.find_elements(By.XPATH, "//*[@data-toggle='dropdown']")
  dropdown = e[0] # select the first dropdown

  if what_to_return == 'initialFetch':
    dropdown.click()
    f = dropdown.find_element(By.XPATH, "following-sibling::*[1]")
    subjectCount = f.find_elements(By.TAG_NAME, "p")
  
    return (len(subjectCount), subjectCount)
  
  elif what_to_return == 'clickDropdown':
    dropdown.click() 






##################################
### I-DISCUSS ACCESS FUNCTION ###
##################################

def idiscuss(open_or_locked:str, course_code:str):

  if open_or_locked == 'open':
    xpath = "//*[@id='openTopic']/div"
  elif open_or_locked == 'locked':
    xpath = "//*[@id='openTopic']/following-sibling::*[1]/div"

  topics = driverl.find_elements(By.XPATH, xpath)
  if topics:
    for r in topics: # grab the information
      topicsEntry = r.find_elements(By.XPATH, './div/p')
      topicName = topicsEntry[0].text

      t = topicsEntry[1].text.strip()
      t_split = re.split(r'\n| : ', t) # using regex to split \n and :
      
      if t_split[9] == 'Active':
        status = 'always Open and Active.'
      else:
        status = f'closed {t_split[9]}.'
      
      log('info', f'Notifying i-Discuss entry title {topicName} of course code {course_code} {status} Please do it.')
      ntfyPOST(f'New i-Discuss from {course_code}', topicName, 'ufuture.uitm.edu.my/login', 'Ufuture', status)







##############################################
### TIME CHECK IF STILL VALID, RETURN BOOL ###
##############################################


def timeCheck(time_in_ddmmyy_HHMMSS_AMPM:str):
  given_time = datetime.strptime(time_in_ddmmyy_HHMMSS_AMPM, "%d/%m/%Y %I:%M %p")
  # `%d`: Day of the month (01 to 31)
  # `%m`: Month (01 to 12)
  # `%Y`: Year (4 digits)
  # `%I`: Hour (12-hour clock) (01 to 12)
  # `%M`: Minute (00 to 59)
  # `%p`: AM or PM
  current_time = datetime.now()

  log('debug', f'Current time is: {current_time}')

  if given_time > current_time:   return True
  else:                           return False









##########################
### NTFY POST FUNCTION ###
##########################

def ntfyPOST(course_code:str, link_wo_https:str, platform_name:str, date_occuring:str):
  if not args.dryrun:
    ntfysvr = credentials(credential, 'ntfyserver')
    requests.post(
      ntfysvr, 
      headers={ 
        "Title": course_code,  
        "Actions": 
          f'view, Open {platform_name}, https://{link_wo_https};   view, Open Ufuture, https://ufuture.uitm.edu.my;'
        }, 
      data=f"on {date_occuring}"
      )






######################
### DB WRITING DEF ###
######################

def writeToDB(subject_code:str, date_time:str, link:str):
  log('info', f'Saving class {subject_code} on {date_time} in {link} into database.')
  cursor.execute("INSERT INTO onlineClass (subjectCode, datetime, link) VALUES (?,?,?)", (subject_code, date_time, link))
























### Stale Element Reference Exception
### Common Cause: You have refreshed the page.
### Ref: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors/#stale-element-reference-exception

#########################################
### ACTUAL PROGRAM STARTS HERE / MAIN ###
#########################################

###############################
### LET'S INIT THE DB FIRST ###
###############################

conn = sqlite3.connect(db_name) # os.path.exists() is not necessary. Sqlite has that built-in.
cursor = conn.cursor() # important for actual interaction with the db
cursor.execute('CREATE TABLE IF NOT EXISTS onlineClass (id INTEGER PRIMARY KEY, subjectCode TEXT, datetime TEXT, link TEXT)')

###################################
### NOW RUN ALL THE SHENANIGANS ###
###################################

driverl.get('https://ufuture.uitm.edu.my/login')

username_field = driverl.find_element(By.ID, "usernameInput")
password_field = driverl.find_element(By.ID, "pswrdInput")

username_field.send_keys(credentials(credential, 'username'))
password_field.send_keys(credentials(credential, 'password'))

login_button = driverl.find_element(By.XPATH, "//button[@type='submit']")
login_button.click()

subjectCount = navigate('initialFetch')[0]
subjectElementArr = navigate('initialFetch')[1]
log('debug', 'Subject count: 10')

navigate('clickDropdown')

for i in range(subjectCount):
  subjectElement = subjectElementArr[i]
  subjectName = subjectElement.text
  log('debug', f'Now accessing {subjectName}')
  subjectElement.click()

  a = driverl.find_element(By.XPATH, "//ul[@id='side-menu']/li[9]/a")
  a.click()
  b = a.find_element(By.XPATH, "following-sibling::*[1]")
  b.click()

  c = driverl.find_element(By.NAME, "onlineclassTbl_length")
  c_selectObj = Select(c)
  c_selectObj.select_by_visible_text("100")

  d = driverl.find_elements(By.XPATH, "//tbody[1]/tr")
  log('debug', f'Number of entries: {len(d)}')

  for k in range(len(d)): # this codeblock is for every entry in the Online Class table
    k_note = d[0].find_element(By.XPATH, "//tr[1]/td[1]").text
    
    if k_note == 'No data available in table':
      log('info', f'{subjectName} has no Online Classes')
      break
    
    else:
      # k_code = d[k].find_element(By.XPATH, ".//td[2]").text
      k_date = d[k].find_element(By.XPATH, ".//td[3]").text
      k_start = d[k].find_element(By.XPATH, ".//td[4]").text
      k_link = d[k].find_element(By.XPATH, ".//td[8]/a").get_attribute('href').replace("https://", "")
      
      if timeCheck(f'{k_date} {k_start}'):
        writeToDB(subjectName, f'{k_date} {k_start}', k_link) ### DB WRITE CODE HERE

  if args.idiscuss:
    g = driverl.find_element(By.XPATH, "//ul[@id='side-menu']/li[10]/a")
    g.click() # click first dropdown

    h = g.find_element(By.XPATH, "following-sibling::*[1]/li/a")
    actionl.move_to_element(h).click().perform()
    h.click() # click 2nd dropdown

    p = h.find_element(By.XPATH, "following-sibling::*[1]/li[3]/a")
    p.click() # click i-Discuss

    ###--- PAGELOAD INTO I-DISCUSS ---###

    academicDiscuss = driverl.find_elements(By.XPATH, "//tbody[1]/tr")

    if not academicDiscuss:
      log('info', f'There is no i-Discuss entry for course code {subjectName}')
    else:
      for q in range(len(academicDiscuss)):
        eachAD = academicDiscuss[q].find_element(By.XPATH, "./td[1]/span[3]/a")
        eachAD.click()

        ###--- PAGELOAD INTO ACADEMIC DISCUSSIONS ---###

        # open topic can have many entries, or None. Therefore...
        idiscuss('open', subjectName)
        # Locked topic is locked. So you kena reda jela.
        
        driverl.back()
        academicDiscuss = driverl.find_elements(By.XPATH, "//tbody[1]/tr")
      
      driverl.back()

    driverl.back()

  driverl.back()
  driverl.back()
  
  subjectElementArr = navigate('initialFetch')[1]






driverl.close()

conn.commit() # Commit the database changes












############################################################
### LOOPING FOR AMBIENT STATE (SCRIPT RUNS INDEFINITELY) ###
############################################################

try:
  while True:
    cursor.execute("SELECT * FROM onlineClass")
    rows = cursor.fetchall()

    for row in rows:
      sleep(0.2)
      log('debug', row)
      
      time1 = datetime.strptime(row[2], "%d/%m/%Y %I:%M %p")
      timecurrent = datetime.now()

      if time1 < timecurrent + timedelta(hours=2):
        log('info', f"Class {row[1]} 2 hours left. Gosok baju sekarang.")
      elif time1 < timecurrent + timedelta(hours=1):
        log('info', f"Class {row[1]} 1 hours left. Pergi mandi sekarang.")
      else:
        log('info', f"Lama lagih. {row[1]} on {row[2]}")

except KeyboardInterrupt:
  
  conn.close() ### Close the database first!
  
  log('interrupt', f"Program stopped.")

  if not args.donotdeletedb:
    log('warn', f'Deleting {db_name} and exiting...')
    if os.path.exists('test.db'): # If test.db exists, delete it
      os.remove(db_name)
  else:
    log('warn', 'Exiting...')

