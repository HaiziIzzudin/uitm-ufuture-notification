from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import requests
import tomllib
import argparse
# import subprocess
from datetime import datetime, timedelta
from os import name
from time import sleep
# import pdb; pdb.set_trace()
import re





####################
# SYSTEM ARGUMENTS #
####################

parser = argparse.ArgumentParser(description="This script access your Ufuture and if any notification about online class present, ntfy.sh will push it to your mobile device, granted you install ntfy.sh and configure same server name with your config.")

parser.add_argument('-t', '--test', action='store_true', help='Run this script in a test environment.')
parser.add_argument('--headful', action='store_true', help='Run selenium in headful mode.')

args = parser.parse_args()






###################
### DRIVER INIT ###
###################

if (args.headful == True):
  ### headful mode
  driver = webdriver.Firefox()
else:
  ### Initialize webdriver in headless mode
  options = webdriver.FirefoxOptions()
  options.add_argument("-headless")
  driver = webdriver.Firefox(options=options)

actions = ActionChains(driver)
















#######################
### DEF AND CLASSES ###
#######################

def getSeparator():
  if name == 'nt': 
    return '\\'
  else:            
    return '/'
  

class toml_credentials:
  def __init__(self, using_credential_file: str):

    # Load credentials from credentials.toml
    with open(using_credential_file, "rb") as a:
      self.data = tomllib.load(a)

  def login(self, website_URL: str,):
    # Open the webpage
    driver.get(website_URL)  # Replace with the URL of the login page

    
    # Find username and password fields and input your credentials
    username_field = driver.find_element(By.ID, "usernameInput")  
    # Replace "username" with the actual ID of the username field
    password_field = driver.find_element(By.ID, "pswrdInput")  
    # Replace "password" with the actual ID of the password field
    
    username_field.send_keys(self.data["login"]["username"])
    password_field.send_keys(self.data["login"]["password"])

    # Find and click the login button
    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")  
    # Replace with the XPath of the login button
    login_button.click()

  def ntfy_server(self):
    return self.data["ntfyServer"]["url"]









class subject_access:
  
  def open_dropdown(self):
    self.e = driver.find_elements(By.XPATH, "//*[@data-toggle='dropdown']")
    self.e[0].click()
  
  def get_subject_count(self):
    self.f = self.e[0].find_element(By.XPATH, "following-sibling::*[1]")
    self.subjectCount = self.f.find_elements(By.TAG_NAME, "p")
    return len(self.subjectCount)
  
  def get_subjects(self, index: int):
    return self.subjectCount[index].text
  
  def access_subject(self, index: int, access_type: str):
    

    if access_type == 'onlineclass':
      self.subjectCount[index].click()
      
      g = driver.find_element(By.XPATH, "//ul[@id='side-menu']/li[9]/a")
      g.click()
      
      h = g.find_element(By.XPATH, "following-sibling::*[1]")
      h.click()
    

    elif access_type == 'idiscuss':
      self.subjectCount[index].click()
      
      g = driver.find_element(By.XPATH, "//ul[@id='side-menu']/li[10]/a")
      g.click()

      h = g.find_element(By.XPATH, "following-sibling::*[1]/li/a")
      actions.move_to_element(h).click().perform()
      h.click()
      
      p = h.find_element(By.XPATH, "following-sibling::*[1]/li[3]/a")
      p.click()





  def access_idiscuss():
    ids1 = driver.find_elements(By.XPATH, "//tbody[1]/tr")
    
    ids2 = ids1[1].find_element(By.XPATH, "./td[1]/span[3]/a")
    ids2.click()

    # open topic
    ids3 = driver.find_elements(By.XPATH, "//*[@id='openTopic']/div")
    if args.test: print(ids3)

    # locked topic
    ids4 = driver.find_elements(By.XPATH, "//*[@id='openTopic']/following-sibling::*[1]/div")
    if args.test: print(ids4)

    # go into topic
    ids5 = ids4[0].find_element(By.XPATH, "./div/h5/a")
    topicName = ids5.text
    print(topicName)

    # get date
    ids6 = ids4[0].find_elements(By.XPATH, './div/p[2]')
    
    ids7 = (ids6[0].text).strip()
    ids7_splitted = re.split(r'\n| : ', ids7)   # using regex to split \n and :

    for a in ids7_splitted:
      print(a, end="|")

    return ids7_splitted[3]
    







  def fetch_timedate(self):
    i = driver.find_element(By.NAME, "onlineclassTbl_length")
    i_selectObj = Select(i)
    i_selectObj.select_by_visible_text("100")

    # find_elements MUST also include the element name array
    j = driver.find_elements(By.XPATH, "//tbody[1]/tr")
    # print(j)
    print('LOG: Number of entries:', len(j))

    if len(j) == 1:
      k_note = j[0].find_element(By.XPATH, "//tr[1]/td[1]").text
      if k_note == 'No data available in table':
        print('LOG: No data available in table')
        return
    
    a = toml_credentials("credentials.toml").ntfy_server()
    
    for k in range(len(j)):
      k_code = j[k].find_element(By.XPATH, ".//td[2]").text
      k_date = j[k].find_element(By.XPATH, ".//td[3]").text
      k_start = j[k].find_element(By.XPATH, ".//td[4]").text
      k_link = j[k].find_element(By.XPATH, ".//td[8]/a").get_attribute('href')

      print('Class', k_code, 'on', k_date, 'at', k_start, 'in', k_link)
      
      # NTFY POST OPERATION HERE
      requests.post(
        a, 
        headers={ 
          "Title": f"{'Class ' + k_code}",  
          "Actions": f"view, Open Meet, {k_link}" 
          }, 
        data=f"{'on ' + k_date + ' at ' + k_start + ' in ' + k_link}".encode(encoding='utf-8'))










def demoTime(options: str) -> str:
  # Get the current date and time
  now = datetime.now()

  # Add 1 minute to the current time
  oneMinAfter = now + timedelta(minutes=1)
  twoMinAfter = now + timedelta(minutes=2)
  
  if options == 'notifyTime':
    return oneMinAfter.strftime("%I:%M:00%p").lower()
  elif options == 'actualTime':
    return twoMinAfter.strftime("%d/%m/%Y (%I:%M %p - %I:%M %p)")


def stripTimeStart(time_string):
  # Extract the date and time parts
  date_part = time_string.split("(")[0].strip()
  time_parts = time_string.split("(")[1].split(")")[0].strip().split(" - ")

  # Convert the extracted parts into datetime objects
  start_time = datetime.strptime(date_part + " " + time_parts[0], "%d/%m/%Y %I:%M %p")
  end_time = datetime.strptime(date_part + " " + time_parts[1], "%d/%m/%Y %I:%M %p")

  print("Start Time:", start_time)
  print("End Time:", end_time)



def ntfyPOST(title: str, link_wo_https: str, platform_name: str, date_occuring: str):
  a = toml_credentials("credentials.toml").ntfy_server()
  
  requests.post(
    a, 
    headers={ 
      "Title": title,  
      "Actions": f"view, Open {platform_name}, https://{link_wo_https}" 
      }, 
    data=f"on {date_occuring}"
    )






















#########################################
### ACTUAL PROGRAM STARTS HERE / MAIN ###
#########################################

toml_credentials("credentials.toml").login("https://ufuture.uitm.edu.my/login")

sa = subject_access()
sa.open_dropdown()
count = sa.get_subject_count()
print('Subject Count:', sa.get_subject_count())
sleep(.2)
sa.open_dropdown()

for i in range(count):
  
  if args.test:
    i = 3    # array numbering
  
  sa.open_dropdown()
  count = sa.get_subject_count()
  print('LOG: Subject name:', sa.get_subjects(i))
  
  # sa.access_subject(i, 'onlineclass')
  sa.access_subject(i, 'idiscuss')
  # sa.fetch_timedate()

  # driver.back()
  # driver.back()
  # driver.back()

  ntfyPOST('Tutorial 2', 'ufuture.uitm.edu.my/login', 'Ufuture', f"{subject_access.access_idiscuss()}. Make sure you do your discussions!")

  if args.test:   break
  






# close
driver.close()
