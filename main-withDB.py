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
interval_in_min:str = 3

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

  if os.path.exists(os.path.expanduser("~") + '/.termux'):
    service = webdriver.FirefoxService(executable_path="/data/data/com.termux/files/usr/bin/geckodriver")

  driver = webdriver.Firefox(service=service, options=options)
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
      print(Back.BLUE + Fore.BLACK + f' DEBUG ', end='')
    else: return
  elif level == 'info':
    print(Back.CYAN + Fore.BLACK + f' INFO ', end='')
  elif level == 'print':
    print(Back.MAGENTA + Fore.BLACK + f' PRINT ', end='')
  elif level == 'interrupt':
    print(Back.RED + Fore.WHITE + f' INTERRUPT ', end='')
  elif level == 'warn':
    print(Back.YELLOW + Fore.BLACK + f' WARN ', end='')
  elif level == 'done':
    print(Back.GREEN + Fore.BLACK + f' DONE ', end='')
  
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

def timeCheck(time1:str):
  current_time = datetime.now()

  log('debug', f'Current time is: {current_time}')

  if time1 > current_time:   return True
  else:                      return False



##########################
### NTFY POST FUNCTION ###
##########################

def ntfyPOST(course_code:str, link_wo_https:str, platform_name:str, date_occuring:str):
  if not args.dryrun:
    ntfysvr = credentials(credential, 'ntfyserver')
    requests.post(
      ntfysvr, 
      headers={ 
        "Title": f'Class {course_code} in 1 Hour ⏱️'.encode(encoding='utf-8'),
        "Actions": 
          f'view, Open {platform_name}, {link_wo_https};   view, Open Ufuture, https://ufuture.uitm.edu.my/login;'
        }, 
      data=f"on {date_occuring}. Mandi dan bersiap sekarang 🚿".encode(encoding='utf-8')
      )



######################
### DB WRITING DEF ###
######################

def writeToDB(subject_code:str, date_time:str, link:str):
  log('info', f'Saving class {subject_code} on {date_time} in {link} into database.')
  cursor.execute("INSERT INTO onlineClass (subjectCode, dateNtime, link, hasNotified) VALUES (?,?,?,?)", (subject_code, date_time, link, 0))



##########################
### DEF FETCH TIME NOW ###
##########################

def timenow():
  return datetime.now()





























#########################################
### ACTUAL PROGRAM STARTS HERE / MAIN ###
#########################################

try:
  
  ### Stale Element Reference Exception
  ### Common Cause: You have refreshed the page.
  ### Ref: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors/#stale-element-reference-exception

  ### LOGIN SCREEN ###
  driverl.get('https://ufuture.uitm.edu.my/login')

  username_field = driverl.find_element(By.ID, "usernameInput")
  password_field = driverl.find_element(By.ID, "pswrdInput")

  username_field.send_keys(credentials(credential, 'username'))
  password_field.send_keys(credentials(credential, 'password'))

  login_button = driverl.find_element(By.XPATH, "//button[@type='submit']")
  login_button.click()
  
  while True: ### NOW RUN ALL THE SHENANIGANS ###
    
    conn = sqlite3.connect(db_name) # os.path.exists() is not necessary. Sqlite has that built-in.
    cursor = conn.cursor() # important for actual interaction with the db
    cursor.execute('''CREATE TABLE IF NOT EXISTS onlineClass
    (id INTEGER PRIMARY KEY, subjectCode TEXT, dateNtime TEXT, link TEXT, hasNotified INTEGER)''')

    driverl.get('https://ufuture.uitm.edu.my/courses/list_course')
    
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
          k_date = d[k].find_element(By.XPATH, ".//td[3]").text
          k_start = d[k].find_element(By.XPATH, ".//td[4]").text
          k_link = d[k].find_element(By.XPATH, ".//td[8]/a").get_attribute('href')
          
          time1 = datetime.strptime(f'{k_date} {k_start}', "%d/%m/%Y %I:%M %p")

          if timeCheck(time1):
            writeToDB(subjectName, time1 - timedelta(hours=1), k_link) ### 1 HOUR BEFORE CLASS
            # writeToDB(subjectName, time1, k_link) ### DB WRITE CODE HERE



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

    # driverl.close()



    ########################
    ### TEST ENVIRONMENT ###
    ########################

    timecurrent = datetime.now()
    
    if args.test:
      timeartificial = timecurrent - timedelta(minutes=1)
      writeToDB('XYZ123', datetime.strftime(timeartificial, '%Y-%m-%d %H:%M:%S'), 'https://www.google.com')

    conn.commit() # Commit the database changes

    ### GET 10 MIN FORWARD TIME ###
    time10min = timecurrent + timedelta(minutes=interval_in_min)

    check = True
    while check:
    
      ### FETCH ALL DATA FROM THE DATABASE ###
      cursor.execute("SELECT * FROM onlineClass")
      rows = cursor.fetchall()
    
      for row in rows:
        sleep(0.2)
        log('debug', row)
        
        time2 = datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S')
        timecurrent = datetime.now()

        if (time2 < timecurrent) and (row[4] == 0):
          log('info', f"Class {row[1]} 1 hours left. Pergi mandi sekarang.")
          ntfyPOST(row[1], row[3], 'Meet', time2.strftime("%d/%m/%Y %I:%M %p")) ### ntfy notification function
          cursor.execute(f"UPDATE onlineClass SET hasNotified = 1 WHERE id = ?", (row[0],)) # comma indicates that it is tuple, without that sqlite will error.
          conn.commit()
        elif (row[4] == 1):
          log('done', f"SUDAH NOTIFY. {row[1]} on {row[2]}")
        else:
          log('info', f"Lama lagih. {row[1]} on {row[2]}")

        log('debug', f'Time left before recheck: {time10min - timecurrent}')
        if (timecurrent > time10min):   
          log('print', 'Timeout has finished. Running ufuture check again...')
          conn.close() ### Close the database first!
          if os.path.exists(db_name):   os.remove(db_name)   # If test.db exists, delete it
          check = False
          break


except KeyboardInterrupt:
  
  conn.close() ### Close the database first!
  
  log('interrupt', f"Program stopped.")

  if not args.donotdeletedb:
    log('warn', f'Deleting {db_name} and exiting...')
    if os.path.exists(db_name): # If test.db exists, delete it
      os.remove(db_name)
  else:
    log('warn', 'Exiting...')

