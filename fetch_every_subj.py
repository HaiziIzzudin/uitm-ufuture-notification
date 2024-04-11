from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import requests
import tomllib
import argparse
from datetime import datetime, timedelta
from os import name
from time import sleep
import re # regex
from colorama import just_fix_windows_console
just_fix_windows_console()
from colorama import Fore, Back, Style



####################
# SYSTEM ARGUMENTS #
####################

parser = argparse.ArgumentParser(description="This script access your Ufuture and if any notification about online class present, ntfy.sh will push it to your mobile device, granted you install ntfy.sh and configure same server name with your config.")

parser.add_argument('--test', action='store_true', help='Run this script in a test environment.')
parser.add_argument('--verbose', action='store_true', help='Run this script verbosely.')
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

def log(message: str):   
  if args.verbose: 
    print(Back.WHITE, end='')
    print(Fore.BLACK + f' LOG: ', end='')
    print(Style.RESET_ALL, end='')
    print(f' {message}')



class toml_credentials:
  def __init__(self, using_credential_file: str):

    # Load credentials from credentials.toml
    with open(using_credential_file, "rb") as a:
      self.data = tomllib.load(a)

  def login(self, website_URL: str,):
    # Open the webpage
    driver.get(website_URL)  # Replace with the URL of the login page
    
    # Find username and password fields and input your credentials
    textfield = driver.find_element(By.ID, "usernameInput")  
    textfield.send_keys(self.data["login"]["username"])
    
    textfield = driver.find_element(By.ID, "pswrdInput")  
    textfield.send_keys(self.data["login"]["password"])
    

    # Find and click the login button
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

  def redirect_to(self, url_wo_https: str):
    driver.get(f'https://{url_wo_https}')

  def ntfy_server(self):
    return self.data["ntfyServer"]["url"]



class subject_access:
  
  def open_floating_dropdown(self):
    element = driver.find_elements(By.XPATH, "//*[@data-toggle='dropdown']")
    self.ddSelection = element[0] 
    self.ddSelection.click() # open the subjects selection
  
  def get_subject_list(self):
    subjectList = self.ddSelection.find_elements(By.XPATH, 'following-sibling::*[1]/a/p')
    subjectList = [element.text for element in subjectList]
    log(subjectList)
    return subjectList
  
  def access_every_idiscuss(self):

    f = driver.find_element(By.XPATH, "//ul[@id='side-menu']/li[10]/a")
    f.click()

    g = f.find_element(By.XPATH, "following-sibling::*[1]/li/a")
    actions.move_to_element(g).click().perform()
    g.click()
    
    h = g.find_element(By.XPATH, "following-sibling::*[1]/li[3]/a")
    h.click()

    ### PAGELOAD -> academic discussions / i-Discuss main page ###

    # Check if tbody exists, means there is content in academic discussions (@ IDISCUSS PAGE)
    # you only check academic discussions since that is the only space being used by lecturers
    academicDiscussions_entry = driver.find_elements(By.XPATH, "//tbody[1]/tr")

    for x in academicDiscussions_entry:
      log(f'Now accessing academic discussions for {x.text}')
    
    # If academicDiscussions_entry exists
    if not academicDiscussions_entry:
      log(f'i-Discuss forum not found')
    else:
      for i, j in enumerate(academicDiscussions_entry):
        # access every academic forum
        academicDiscussions_entry[i].find_element(By.XPATH, "./td[1]/span[3]/a").click()

        ### PAGELOAD -> course forum ###


        # OPEN TOPIC
        ids3 = driver.find_elements(By.XPATH, "//*[@id='openTopic']/div") # get every div

        if len(ids3) == 0:
          log(f"No open topics of {j.text} found.")
        else: # if open topics found
          log(ids3)
          for i, j in enumerate(ids3):
            # go into topic (@ INSIDE THE PAGE)
            topicName = j.find_element(By.XPATH, "./div/h5/a").text
            log(topicName)
        driver.back()
          
        # LOCKED TOPIC
        ids4 = driver.find_elements(By.XPATH, "//*[@id='openTopic']/following-sibling::*[1]/div") # get every div

        if(ids4) == 0:
          log(f"No locked topics of {j.text} found.")
        else: # if locked topics found
          log(ids4)
          for i, j in enumerate(ids4):
            # go into topic (@ INSIDE THE PAGE)
            topicName = j.find_element(By.XPATH, "./div/h5/a").text
            log(topicName)


        driver.back()   ### PAGELOAD -> academic discussions / i-Discuss main page ###



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
    log(f'Number of entries: {len(j)}')

    if len(j) == 1:
      k_note = j[0].find_element(By.XPATH, "//tr[1]/td[1]").text
      if k_note == 'No data available in table':
        log('No online class entry available.')
        return
    
    a = toml_credentials("credentials.toml").ntfy_server()
    
    for k in range(len(j)):
      k_code = j[k].find_element(By.XPATH, ".//td[2]").text
      k_date = j[k].find_element(By.XPATH, ".//td[3]").text
      k_start = j[k].find_element(By.XPATH, ".//td[4]").text
      k_link = j[k].find_element(By.XPATH, ".//td[8]/a").get_attribute('href').replace("https://", "")

      print('Class', k_code, 'on', k_date, 'at', k_start, 'in', k_link)
      
      ntfyPOST(k_code, k_link, 'Meet', f'{k_date} {k_start}')



def ntfyPOST(title: str, link_wo_https: str, platform_name: str, date_occuring: str):
  a = toml_credentials("credentials.toml").ntfy_server()
  
  requests.post(
    a, 
    headers={ 
      "Title": title,  
      "Actions": 
        f'view, Open {platform_name}, https://{link_wo_https};   view, Open Ufuture, https://ufuture.uitm.edu.my'
      }, 
    data=f"on {date_occuring}"
    )






















#########################################
### ACTUAL PROGRAM STARTS HERE / MAIN ###
#########################################
tc = toml_credentials('credentials.toml')



tc.login("https://ufuture.uitm.edu.my/login")

sa = subject_access()

sa.open_floating_dropdown()

for i in (sa.get_subject_list()):
  log(f'Now accessing: {i}')
  tc.redirect_to(f'ufuture.uitm.edu.my/OnlineClasses/index/{i}')
  
  sa.fetch_timedate()
  
  sleep(1)

  subject_access().access_every_idiscuss()

  sleep(1)







# for i in range(count):
  
#   if args.test:
#     i = 3    # array numbering
  
#   sa.open_dropdown()
#   count = sa.get_subject_count()
#   print('LOG: Subject name:', sa.get_subjects(i))
  
#   # sa.access_subject(i, 'onlineclass')
#   sa.access_subject(i, 'idiscuss')
#   # sa.fetch_timedate()

#   # driver.back()
#   # driver.back()
#   # driver.back()

#   ntfyPOST('Tutorial 2', 'ufuture.uitm.edu.my/login', 'Ufuture', f"{subject_access.access_idiscuss()}. Make sure you do your discussions!")

#   if args.test:   break
  






# close
driver.close()
