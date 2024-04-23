# Acknowledgement

Thank you to these father projects that make this child project possible:

1. [ntfy](https://ntfy.sh/)
1. [selenium](https://www.selenium.dev/)
1. [toml](https://toml.io/en/)

*Go support them!*

# What's this?

Written in Python and powered by Selenium, Ntfy, SQLite DB and TOML, uitm-ufuture-notification is a Python script that accesses your Ufuture and if any notification about online class and discussions present, *ntfy* will push it to your mobile device, granted you install Ntfy and configure same server name with your config. 

# Running this script

## Preface
This script has 2 types:
1. `app.py`: This one iterate through recent notifications (on the top right) of Ufuture.
2. `main-notifyOnce.py`: This one iterate through every subject in the myCourses dropdown (on the top right) of Ufuture. This one only run once, and notify as a bunch. If you want a more stay alive/ ambient functionality;
2. `main-withDB.py`: This one is the latest in development. It iterate through every subject in the myCourses dropdown (on the top right) of Ufuture. This one has a database, and will loop through all the saved time in database, and if time of the online class is 2 hours left and 1 hours left, ntfy will send notification to you.

Please note that `main-...` script requires you to agree to subject pledge. Please do so if you haven't already.<br>
By default, script is running in headless (selenium webdriver headless) mode. To override this, please add flags `--headful`.<br>
By default, script is running without having i-Discuss check functionality. To override this, please add flags `--idiscuss`.<br>
By default, script is running with ntfy functionality. To turn ntfy noti function off (or dry running), please add flags `--dryrun`.

## How to run

1. Install **Python 3.12** (make sure Python is accessible in PATH)
<details>
  <summary><i>Why Python 3.12?</i></summary>

  > 3.12.2 Added functionality of parsing toml file, under class name `tomllib`, and updated to sqlite3. We are leveraging that functionality to ease your experience using this script.

</details>

1. Install ntfy - PUT/POST to your phone | 
[Android](https://play.google.com/store/apps/details?id=io.heckel.ntfy) | 
[iOS](https://apps.apple.com/us/app/ntfy/id1625396347) | 
[F-Droid](https://f-droid.org/en/packages/io.heckel.ntfy/) |
2. Setup Ntfy on your phone, and provide a globally unique Topic.
2. Now on your computer or server, run: 
```
pip install selenium
```
2. Next, run: 
```
git clone https://github.com/HaiziIzzudin/uitm-ufuture-notification.git
```
3. Configure `credentials.toml`. Please refer [configuration](#credentialstoml-configuration) for how to configure `credential.toml`
3. Finally, run by invoking:
```
python main-notifyOnce.py
``` 
OR
```
python main-withDB.py
```
## `credentials.toml` Configuration
Make a new file named it `credentials.toml` in same folder with the script. Copy and paste the configuration below:
```
[login]
username = your_username
password = "your_password"

[ntfyServer]
url = "https://ntfy.sh/your_ntfy_server"
```
Given that:<br>
`your_username` is your username. For UiTM students, this will be your Student ID.<br>
`your_password` is your iStudent/ Ufuture password. Remember to encase it in a double quote, failing to do so will result in script fail to run.<br>
`your_ntfy_server` is your own Ntfy globally unique topic. This usually got initialized on your mobile phone.

# Known Issues
1. Ntfy have known issues regarding ntfy on iOS. Please refer [here](https://github.com/binwiederhier/ntfy/issues/880) for more details.
3. `main-withDB.py` has some issues where if you interrupt the program, program will not save state. Means if notification has been pushed, if script runs again, notification will get pushed again.
4. My fren has a Macintosh operating system and has problems doing `pip install selenium`. Will examine soon, and will update instructions here for MacOS.


Have other problems I didn't catch during development? Write it in [issues](https://github.com/HaiziIzzudin/uitm-ufuture-notification/issues).

# Changelog
**26/3/2024**: Just learned how to use python classes and getters (yay!). I have implement it in my code. 

**10/4/2024**: Selenium now running headless. Added new functionality to check for i-Discuss created date. <br>~~**ATTENTION:** This update make breaking changes on the original code that the script is unusable. Please wait for next commit to fix the thing.~~

**16/4/2024**: New code refactor/ rewrite. Expect more rollout of new code later on.

**23/4/2024 Pagi buta**: (1) Logs now has labels either debug or info (with colours). (2) Webdriver now will NOT load images, either in headful or headless mode. This to make sure webpage loads faster on slow internet connection. (3) Added def of check time validity of online class, and if has passed current time, program will not notify.

**23/4/2024 Tghari**: (1) Script has been renamed from `main.py` to `main-notifyOnce.py`. Script has been duplicated, and added database functionality, with filename `main-withDB.py`. (2) `main-withDB.py` file has functionality of saving the course code and datetime in database, iterate contents from the database indefinitely, and nicer stdout of `DEBUG`, `INFO`, `WARN`, `PRINT`, and `INTERRUPT`.

**23/4/2024 Petang**: Script now has a loop functionality that checks if there is 1 hour left before class, and will notify user.

**24/4/2024 Pagi Buta**: Script loop has improved more, where ufuture rechecks can be made for every 1 minute interval. You can change this in the script (`line 20`).

# Support my software development on [Ko-Fi](https://ko-fi.com/haiziizzudin)
#### *Thank you from the bottom of my heart ❤️*


###### Disclaimer: uitm-ufuture-notification is nowhere affliated or associated with Universiti Teknologi MARA, UiTM, or it's subsidiaries. This tool is just an experimental by student in their free time to see if we can improve the well being of students who uses Ufuture. This is not a direct attack to UiTM's system, it is an QOL tool for the better. Universiti Teknologi MARA, UiTM, Ufuture, Purple square and circle shape with four books and keris is Copyright © of Universiti Teknologi MARA (UiTM). ALL RIGHTS RESERVED.