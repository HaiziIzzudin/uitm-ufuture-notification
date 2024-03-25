from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import requests
import tomllib
import argparse
# import subprocess
from datetime import datetime, timedelta
from os import name
from time import sleep





####################
# SYSTEM ARGUMENTS #
####################

parser = argparse.ArgumentParser(description="This script access your Ufuture and if any notification about online class present, ntfy.sh will push it to your mobile device, granted you install ntfy.sh and configure same server name with your config.")

parser.add_argument('-t', '--test', action='store_true', help='Run this script in a test environment.')

args = parser.parse_args()




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
  
  def access_subject(self, index: int):
    self.subjectCount[index].click()
    g = driver.find_element(By.XPATH, "//ul[@id='side-menu']/li[9]/a")
    g.click()
    h = g.find_element(By.XPATH, "following-sibling::*[1]")
    h.click()

  def fetch_timedate(self):
    i = driver.find_element(By.NAME, "onlineclassTbl_length")
    i_selectObj = Select(i)
    i_selectObj.select_by_visible_text("100")

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






















#########################################
### ACTUAL PROGRAM STARTS HERE / MAIN ###
#########################################

driver = webdriver.Firefox()

toml_credentials("credentials.toml").login("https://ufuture.uitm.edu.my/login")

sa = subject_access()
sa.open_dropdown()
count = sa.get_subject_count()
print('Subject Count:', sa.get_subject_count())
sleep(.2)
sa.open_dropdown()

for i in range(count):
  sa.open_dropdown()
  count = sa.get_subject_count()
  print('LOG: Subject name:', sa.get_subjects(i))
  
  sa.access_subject(i)
  sa.fetch_timedate()

  driver.back()
  driver.back()






# close
driver.close()