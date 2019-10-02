# Cloudflare DNS External IP Synchronizer (Python)

This awkwardly named repository will synchronize a CloudFlare DNS record with your current public IP addresses.

I created this as a solution to the annoyingly short DHCP leases handed out by my ISP. Personally, I use it to set an A record on one of my site's subdomains- allowing me to RDP into my machine by hostname, without having to worry about whether or not my external IP changed.


## Features
- Easy to configure, sporting an ini file to easily change all relevant settings
- Support for all types of DNS records
- Logging

## Installation
Download the repository to your computer, placing the unzipped files somewhere out of the way (assuming you want it to run scheduled).

Create an API token for CloudFlare at this link: https://dash.cloudflare.com/profile/api-tokens
Give the token the following permissions:
*    Zone   Zone   Read
*    Zone   DNS    Edit

Open the "src" folder, and open "config.ini" in your favorite text editor.

Fill out the fields with the appropriate information. Here's an example:
```ini
[CloudFlare-API]
token = fJldweoEslakCwpLsaecCeroscorlaecp
siteName = mydomain.com

[DNS]
name = home.mydomain.com
recordType = A
proxied = False
createRecord = True

[general]
loggingEnabled = True
logPath = /var/log/CF-DNS.log
logLevel = 2
```

pip install the following packages: configparser, requests
```bash
pip install configparser requests
```
(requirements.txt located in the "src" folder if you have issues with versioning)

You should now be good to run "main.py" in the "src" folder.

If it's not working, a good place to start is checking the log file you specified in the ini folder (should be created automatically).

## Auto-Run Scheduling (Windows/Task Scheduler)
Create a .bat file somewhere in the project directory. add the following contents:
```bash
cd "C:\absolute\path\to\the\project\src"
python main.py
```
feel free to add a "pause" at the end for testing.

>NOTE:  be sure to add the FULL path! relative path will not work from task scheduler

>NOTE2: ensure "python" is the correct identifier. May be "py", "python3", etc
double click the newly created .bat file.

You'll know it worked if a log file gets created at the path you specified in the ini file.

Assuming all is well at this point, open the start menu and type "task scheduler".

Click "Action" at the top, then "Create Task".

Here's some screenshots of my configuration (runs every 10 minutes)

> [General Tab](http://bit.ly/2nvvIe1)

> [Triggers > New](http://bit.ly/2nvyLTv)

> [Actions](http://bit.ly/2lXrcEE)

When finished, you can right click the newly created task & click "Run". Then, check the log file for a new entry.

## Auto-Run Scheduling (Linux/Cron)
Open terminal (assuming GUI)

type "crontab -e"
create a cron job at the desired frequency with the command "python /path/to/project/main.py"
>Note: If you dont know how to format a cron job, use this: https://crontab-generator.org/
