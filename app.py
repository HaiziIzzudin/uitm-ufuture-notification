from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import tomllib
import argparse
# import subprocess
from datetime import datetime, timedelta
from os import name





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


def dropdownInteract():
  # selenium get second elements that has data-toggle attribute
  elements = driver.find_elements(By.XPATH, "//*[@data-toggle='dropdown']")

  # click the second elements
  elements[0].click()

  # grab element next within the same hierarchy
  next_element = elements[1].find_element(By.XPATH, "following-sibling::*[1]")

  # grab contents from tag p
  return next_element.find_elements(By.TAG_NAME, "p")


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






# Initialize the web browser
driver = webdriver.Firefox()

# Open the webpage
driver.get("https://ufuture.uitm.edu.my/login")  # Replace with the URL of the login page

# Find username and password fields and input your credentials
username_field = driver.find_element(By.ID, "usernameInput")  
# Replace "username" with the actual ID of the username field
password_field = driver.find_element(By.ID, "pswrdInput")  
# Replace "password" with the actual ID of the password field

# Load credentials from credentials.toml
with open("credentials.toml", "rb") as a:
    data = tomllib.load(a)

username_field.send_keys(data["login"]["username"])
password_field.send_keys(data["login"]["password"])



# Find and click the login button
login_button = driver.find_element(By.XPATH, "//button[@type='submit']")  
# Replace with the XPath of the login button
login_button.click()

# user has login
noti_entries = dropdownInteract()

i = 0

while i < len(noti_entries):
  
  ### GET SUBJECT ###
  e = noti_entries[i] # set entry of i to e elements
  subject = e.text # set subject to contents of e
  click_noti = e.click() # click e element

  ### GET TIMEDATE ###
  details = driver.find_elements(By.XPATH, "//tbody[1]/tr[6]/td[2]") # navigating to 2nd td elements, xpath exp index start with 1
  timedate = details[0].text # set timedate to contents of 2nd td

  ### GO BACK ###
  driver.back()

  ### REPEAT DROPDOWN PROCESS ###
  noti_entries = dropdownInteract()

  ### TEST ENTRIES ###
  if args.test: 
    subject = 'ABC123, has Online Classes'
    timedate = f'{demoTime('actualTime')}'
  
  ### GET TIME TO NOTIFY ###
  # whenToNotify = demoTime('notifyTime')
  # whenToNotify = '3 seconds'

  ### LOGGING AND PUSH NOTIFICATION ###
  print(f'LOG: Notifying user of {subject} at {timedate}') #, notifying at', whenToNotify
  # requests.post(data["ntfyServer"]["url"], data=f"{timedate}".encode(encoding='utf-8'), headers={ "Title": f"{subject}", "At": f"{whenToNotify}" })
  requests.post(data["ntfyServer"]["url"], data=f"{timedate}".encode(encoding='utf-8'), headers={ "Title": f"{subject}" })
  
  ### INCREMENT ###
  if args.test:
    i = len(noti_entries)
  else:
    i += 1


# close
driver.close()