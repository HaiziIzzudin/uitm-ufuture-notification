# Acknowledgement

Thank you to these father projects that make this child project possible:

1. [ntfy](https://ntfy.sh/)
1. [selenium](https://www.selenium.dev/)
1. [toml](https://toml.io/en/)

*Go support them!*

# What's this?

Written in Python and powered by Selenium, Ntfy and TOML, uitm-ufuture-notification is a Python script that accesses your Ufuture and if any notification about online class and discussions present, *ntfy* will push it to your mobile device, granted you install ntfy.sh and configure same server name with your config. 

# Running this script

## Preface
This script has 2 types:
1. `app.py`: This one iterate through recent notifications (on the top right) of Ufuture.
2. `main.py`: This one iterate through every subject in the myCourses dropdown (on the top right) of Ufuture. This mode requires you to agree all subject pledges before proceeding.

By default, script is running in headless (selenium webdriver headless) mode. To override this, please add flags `--headful`.
By default, script is running without having i-Discuss check functionality. To override this, please add flags `--idiscuss`.
By default, script is running with ntfy functionality. To turn ntfy noti function off (or dry running), please add flags `--dryrun`.

## How to run

1. Install **Python 3.12** (make sure Python is accessible in PATH)
<details>
  <summary><i>Why Python 3.12?</i></summary>

  > 3.12.2 Added functionality of parsing toml file, under class name `tomllib`. We are leveraging that functionality to ease your experience using this script.

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
python main.py
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
2. Right now this script only run once, and only notify once, directly as a bunch. No timing function (10 minutes before class) is being implemented yet. *If you know how to do so, **cough, cough** can you help me pwease 🥺👉👈, feel free to do a pull request [here](https://github.com/HaiziIzzudin/uitm-ufuture-notification/pulls).*
3. ~~**Commit on 10/4/2024 make the script unusable.** Please wait for next commit that will fix it + new functionality Coming Soon™️.~~<br>
Latest commit has make it back working now, with full code refactor and rewrite. Expect more rollout of new code later on.
4. New code rewrite has some issues regarding loop breaks for every subject. Will fix soon asap.

Have other problems I didn't catch during development? Write it in [issues](https://github.com/HaiziIzzudin/uitm-ufuture-notification/issues).

# Changelog
**26/3/2024**: Just learned how to use python classes and getters (yay!). I have implement it in my code. 

**10/4/2024**: Selenium now running headless. Added new functionality to check for i-Discuss created date. <br>~~**ATTENTION:** This update make breaking changes on the original code that the script is unusable. Please wait for next commit to fix the thing.~~

**16/4/2024**: New code refactor/ rewrite. Expect more rollout of new code later on.

**23/4/2024**: (1) Logs now has labels either debug or info (with colours). (2) Webdriver now will NOT load images, either in headful or headless mode. This to make sure webpage loads faster on slow internet connection. (3) Added def of check time validity of online class, and if has passed current time, program will not notify.

*My fren has a Macintosh operating system and has problems doing `pip install selenium`. Will examine soon, and will update instructions here for MacOS.*

# Support my software development on [Ko-Fi](https://ko-fi.com/haiziizzudin)
#### *Thank you from the bottom of my heart ❤️*


###### Disclaimer: uitm-ufuture-notification is nowhere affliated or associated with Universiti Teknologi MARA, UiTM, or it's subsidiaries. This tool is just an experimental by student in their free time to see if we can improve the well being of students who uses Ufuture. This is not a direct attack to UiTM's system, it is an QOL tool for the better. Universiti Teknologi MARA, UiTM, Ufuture, Purple square and circle shape with four books and keris is Copyright © of Universiti Teknologi MARA (UiTM). ALL RIGHTS RESERVED.