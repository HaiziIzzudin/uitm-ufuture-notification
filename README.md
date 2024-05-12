# Important notice
*uitm-ufuture-notification* is now compatible with Python version 3.11.0 and above, not only 3.12 anymore!

***NEW!*** Project can now run on Android. Read further.

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
This script has 3 types:
1. `app.py`: **DEPRECATED** - This one iterate through recent notifications (on the top right) of Ufuture.
2. `main-notifyOnce.py`: **DEPRECATED** - This one iterate through every subject in the myCourses dropdown (on the top right) of Ufuture. This one only run once, and notify as a bunch. If you want a more stay alive/ ambient functionality;
2. `main-withDB.py`: This one is the latest in development. It iterate through every subject in the myCourses dropdown (on the top right) of Ufuture. This one has a database, and will loop through all the saved time in database. If time of the online class is 1 hours left, and if class time has arrived, ntfy will notify you to get ready, or tick your attendance in Ufuture.

Please note that `main-...` script requires you to agree to subject pledge. Please do so if you haven't already.<br>
By default, script is running in headless (selenium webdriver headless) mode. To override this, please add flags `--headful`.<br>
By default, script is running without having i-Discuss check functionality. To override this, please add flags `--idiscuss`.<br>
By default, script is running with ntfy functionality. To turn ntfy noti function off (or dry running), please add flags `--dryrun`.

## How to run

1. Choose which Operating System best suites your use case:

|Windows, MacOS, Linux (not Termux)|Android (with Termux)|
|-|-|
|Please have Python 3.12 installed (either standalone from [Python.org](https://www.python.org/downloads/) website, or my favourite, use projects like [pyenv](https://github.com/pyenv/pyenv) project, [pyenv-win](https://github.com/pyenv-win/pyenv-win) if you are on Windows.)<br><br>Please have Git installed, either from [Git official website](https://git-scm.com/downloads), or install via package manager:<br><br>**Windows**<pre>winget install --id Git.Git -e --source winget</pre><br>**MacOS** - *Make sure [brew](https://brew.sh/) installed.*<pre>brew install git</pre><br>**Linux** - Please refer [here](https://git-scm.com/download/linux).|1. Download and install [termux](https://termux.dev/en/").<br><br>2. Copy, paste and run these commands:<pre>pkg update && pkg upgrade -y && pkg install x11-repo -y && pkg update && pkg install git python firefox geckodriver -y</pre>|



2. Install ntfy - PUT/POST to your phone | 
[Android](https://play.google.com/store/apps/details?id=io.heckel.ntfy) | 
[iOS](https://apps.apple.com/us/app/ntfy/id1625396347) | 
[F-Droid](https://f-droid.org/en/packages/io.heckel.ntfy/) |
2. Setup Ntfy on your phone, and provide a globally unique Topic.
2. Now on your computer or server, run: 
```
pip install selenium colorama requests pandas
```
2. Next, run: 
```
git clone https://github.com/HaiziIzzudin/uitm-ufuture-notification.git && cd uitm-ufuture-notification
```
3. Configure `credentials.toml`. Please refer [configuration](#credentialstoml-configuration) for how to configure `credential.toml`
3. Finally, run by invoking:
```
python main-withDB.py
```
## `credentials.toml` Configuration
Make a new file named it `credentials.toml` in same folder with the script. Copy and paste the configuration below:


```toml
# YOUR UFUTURE CREDENTIALS

[login]
username = your_username
password = "your_password"

[ntfyServer]
url = "https://ntfy.sh/your_ntfy_topic"


# PERSISTENT TIMETABLE

[timetable.monday]
classcode1 = ['time', 'place']
classcode2 = ['time', 'place']
classcode3 = ['time', 'place']

[timetable.tuesday]
classcode4 = ['time', 'place']

[timetable.wednesday]
classcode5 = ['time', 'place']
classcode6 = ['time', 'place']

[timetable.thursday]

[timetable.friday]
classcode7 = ['time', 'place']
classcode8 = ['time', 'place']


# OTHER INFORMATION REQUIRED
[academicInfo]
tarikh_tamat_semester_semasa = YYYY-MM-DD 
# Example: 2024-07-24
```


Given that:<br>
`your_username` is your username. For UiTM students, this will be your Student ID.<br>
`your_password` is your iStudent/ Ufuture password. Remember to encase it in a double quote, failing to do so will result in script fail to run.<br>
`your_ntfy_topic` is your own Ntfy globally unique topic. This usually got initialized on your mobile phone.<br>
`classcode` is your Course Code. Example: *'IRA543'*<br>
`time` is time of that class starts. Example: *'12:00PM'*<br>
`place` is place of the class will be held. You can put free text here. Example: *'Bilik Seminar'*
`YYYY-MM-DD` is your date of finish your current semester. Example: *2024-07-24*

***ATTENTION:*** **Any place that has single quote '...' MUST be followed. In `time` and `YYYY-MM-DD` format DO NOT add any extra characters or spaces.**

*What if I have multiple classes or no classes for that day?*<br>
Do not fret. The `classcode` entry can be added or removed to your liking. Any `[timetable]` entry can be empty.

*Still can't catch it?* You may want to look my example [here](https://github.com/HaiziIzzudin/uitm-ufuture-notification/blob/main/credentials-example.toml).




# Known Issues
1. Ntfy have known issues regarding ntfy on iOS. Please refer [here](https://github.com/binwiederhier/ntfy/issues/880) for more details.
3. `main-withDB.py` has some issues where if you interrupt the program, program will not save state. Means if notification has been pushed, if script runs again, notification will get pushed again.


Have other problems I didn't catch during development? Write it in [issues](https://github.com/HaiziIzzudin/uitm-ufuture-notification/issues).





<details>
<summary><h1>Changelog</h1></summary>

  **16/4/2024**: New code refactor/ rewrite.

  **23/4/2024 Pagi buta**: (1) Logs now has labels either debug or info (with colours). (2) Webdriver now will NOT load images, either in headful or headless mode. This to make sure webpage loads faster on slow internet connection. (3) Added def of check time validity of online class, and if has passed current time, program will not notify.

  **23/4/2024 Tghari**: (1) Script has been renamed from `main.py` to `main-notifyOnce.py`. Script has been duplicated, and added database functionality, with filename `main-withDB.py`. (2) `main-withDB.py` file has functionality of saving the course code and datetime in database, iterate contents from the database indefinitely, and nicer stdout of `DEBUG`, `INFO`, `WARN`, `PRINT`, and `INTERRUPT`.

  **23/4/2024 Petang**: Script now has a loop functionality that checks if there is 1 hour left before class, and will notify user.

  **24/4/2024 Pagi Buta**: Script loop has improved more, where ufuture rechecks can be made for every 3 minute interval. You can change this in the script (`line 20`).

  **11/5/2024**: Added QOL improvement where script has been tested to run on Python 3.11.0, and adapted the project to run on Android (a.k.a. self-hosted method).
  
  **13/5/2024**: Added functionality to notify user if class time has arrived, program will notify user to tick attendance in Ufuture.
</details>

# Support my software development on [Ko-Fi](https://ko-fi.com/haiziizzudin)
#### *Thank you from the bottom of my heart ❤️*


###### Disclaimer: uitm-ufuture-notification is nowhere affliated or associated with Universiti Teknologi MARA, UiTM, or it's subsidiaries. This tool is just an experimental by student in their free time to see if we can improve the well being of students who uses Ufuture. This is not a direct attack to UiTM's system, it is an QOL tool for the better. Universiti Teknologi MARA, UiTM, Ufuture, Purple square and circle shape with four books and keris is Copyright © of Universiti Teknologi MARA (UiTM). ALL RIGHTS RESERVED.
