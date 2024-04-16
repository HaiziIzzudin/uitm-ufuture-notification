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

credential = 'credentials.toml'




########################
### SYSTEM ARGUMENTS ###
########################

parser = argparse.ArgumentParser(description="This script access your Ufuture and if any notification about online class present, ntfy.sh will push it to your mobile device, granted you install ntfy.sh and configure same server name with your config.")

parser.add_argument('--test', action='store_true', help='Run this script in a test environment.')
parser.add_argument('--verbose', action='store_true', help='Run this script verbosely.')
parser.add_argument('--headful', action='store_true', help='Run selenium in headful mode.')
parser.add_argument('--idiscuss', action='store_true', help='Access i-Discuss.')

args = parser.parse_args()




###################
### DRIVER INIT ###
###################

def drivers():
  if (args.headful == True):   ### headful = true
    driver = webdriver.Firefox()

  else:   ### headless mode
    options = webdriver.FirefoxOptions()
    options.add_argument("-headless")
    driver = webdriver.Firefox(options=options)
  
  actions = ActionChains(driver)

  return (driver, actions) # this is a tuple


driverl = drivers()[0]





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

def log(message: str):   
  print(Back.WHITE, end='')
  print(Fore.BLACK + f' LOG: ', end='')
  print(Style.RESET_ALL, end='')
  print(f' {message}')
  






##################################
### NAVIGATE TO ONLINE CLASSES ###
##################################

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






##########################
### NTFY POST FUNCTION ###
##########################

def ntfyPOST(title: str, link_wo_https: str, platform_name: str, date_occuring: str):
  ntfysvr = credentials(credential, 'ntfyserver')
  requests.post(
    ntfysvr, 
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

### Stale Element Reference Exception
### Common Cause:
### You have refreshed the page.
### Ref: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors/#stale-element-reference-exception





driverl.get('https://ufuture.uitm.edu.my/login')

username_field = driverl.find_element(By.ID, "usernameInput")
password_field = driverl.find_element(By.ID, "pswrdInput")

username_field.send_keys(credentials(credential, 'username'))
password_field.send_keys(credentials(credential, 'password'))

login_button = driverl.find_element(By.XPATH, "//button[@type='submit']")
login_button.click()

subjectCount = navigate('initialFetch')[0]
subjectElementArr = navigate('initialFetch')[1]
log('Subject count: 10')

navigate('clickDropdown')

for i in range(subjectCount):
  subjectElement = subjectElementArr[i]
  subjectName = subjectElement.text
  log(f'Now accessing {subjectName}')
  subjectElement.click()

  a = driverl.find_element(By.XPATH, "//ul[@id='side-menu']/li[9]/a")
  a.click()
  b = a.find_element(By.XPATH, "following-sibling::*[1]")
  b.click()

  c = driverl.find_element(By.NAME, "onlineclassTbl_length")
  c_selectObj = Select(c)
  c_selectObj.select_by_visible_text("100")

  d = driverl.find_elements(By.XPATH, "//tbody[1]/tr")
  log(f'Number of entries: {len(d)}')

  for k in range(len(d)):
    k_note = d[0].find_element(By.XPATH, "//tr[1]/td[1]").text
    if k_note == 'No data available in table':
      log(f'{subjectName} has no Online Classes')
      break
    else:
      k_code = d[k].find_element(By.XPATH, ".//td[2]").text
      k_date = d[k].find_element(By.XPATH, ".//td[3]").text
      k_start = d[k].find_element(By.XPATH, ".//td[4]").text
      k_link = d[k].find_element(By.XPATH, ".//td[8]/a").get_attribute('href').replace("https://", "")
      log(f'Notifying class {k_code} on {k_date} at {k_start} in {k_link}')
      ntfyPOST(k_code, k_link, 'Meet', f'{k_date} {k_start}')

  if args.idiscuss:
    # codeblock here
    log('idiscuss here')

  driverl.back()
  driverl.back()
  
  subjectElementArr = navigate('initialFetch')[1]






driverl.close()