# What's this?

Written in Python and powered by Selenium, Ntfy.sh and TOML, uitm-ufuture-notification is a Python script that accesses your Ufuture and if any notification about online class present, ntfy.sh will push it to your mobile device, granted you install ntfy.sh and configure same server name with your config. 

# Running this script

## How to run

1. Install Python (make sure Python is accessible in PATH)
1. Install ntfy - PUT/POST to your phone | 
[Android](https://play.google.com/store/apps/details?id=io.heckel.ntfy) | 
[iOS](https://apps.apple.com/us/app/ntfy/id1625396347) | 
[F-Droid](https://f-droid.org/en/packages/io.heckel.ntfy/) |
2. Setup Ntfy on your phone, and provide a globally unique Topic.
2. Now on your computer or server, run: 
```
pip install selenium requests tomllib
```
2. Next, run: 
```
git clone https://github.com/HaiziIzzudin/uitm-ufuture-notification.git
```
3. Configure `credentials.toml`. Please refer [configuration](#credentialstoml-configuration) for how to configure `credential.toml`
3. Finally, run by invoking:
```
python app.py
``` 

## `credentials.toml` Configuration
Make a new file named it `credentials.toml`. Copy and paste the configuration below:
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

# Problems?
Write it in [issues](https://github.com/HaiziIzzudin/uitm-ufuture-notification/issues)

# Support my software development on [Ko-Fi](https://ko-fi.com/haiziizzudin)
#### *Thank you from the bottom of my heart ❤️*