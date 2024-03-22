from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from time import sleep
import tomllib

def dropdownInteract():
  # selenium get second elements that has data-toggle attribute
  elements = driver.find_elements(By.XPATH, "//*[@data-toggle='dropdown']")

  # click the second elements
  elements[1].click()

  # grab element next within the same hierarchy
  next_element = elements[1].find_element(By.XPATH, "following-sibling::*[1]")

  # grab contents from tag p
  return next_element.find_elements(By.TAG_NAME, "p")


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

messageArray = []
i = 0

while i < len(noti_entries):
  
  e = noti_entries[i]
  
  subject = e.text

  click_noti = e.click()

  details = driver.find_elements(By.XPATH, "//tbody[1]/tr[6]/td[2]") # xpath expressions index starts with 1

  timedate = details[0].text
  
  k = subject + '\n' + timedate

  driver.back()

  noti_entries = dropdownInteract()

  print('LOG: Notifying user of', k)
  requests.post(data["ntfyServer"]["url"], data=f"{k}".encode(encoding='utf-8'))
  
  i += 1


# close
driver.close()





