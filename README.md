DO Keepalive keeps tabs on DigitalOcean servers that have a tendency to freeze up, or that require a high degree of
availability. It will check if a given port is open, and if it isn't, it will use the DO(Digitalocean) API to reboot the
server.

Due to this script using low level network access, you must run this script as root. You can do this from the command
line by using sudo, add it to root's crontab with `sudo crontab -e`, or create a systemd service with root as the user.

###### Simple Setup Instructions:

1. Clone this repository into a folder on your stable server.
2. Create a virtual environment for the repository
3. `pip install -r requirements.txt`
4. `python create_config.py` and follow instructions.
5. add `@reboot sleep 60 && /path/to/virtualenv/python /path/to/dokeepalive.py` to root's crontab. change the sleep
   period (60) to suit the amount of time, in seconds, your system may take to fully boot.
6. Reboot the machine, or run dokeepalive.py.

Alternatively, you can add a systemd file to start things.

`nano /lib/systemd/system/dokeepalive.service`

In that file, paste the following:

```
[Unit]
Description=DOKeepalive Service
After=multi-user.target

[Service]
User=root
Group=root
Type=simple
Restart=always
ExecStart=/path/to/virtual/python /path/to/dokeepalive/dokeepalive.py > /path/to/dokeepalive/dokeepalive.error.log 2>&1
WorkingDirectory=/path/to/dokeepalive/

[Install]
WantedBy=multi-user.target
```

Then run the following commands:

`sudo systemctl daemon-reload`

`sudo systemctl enable dokeepalive.service`

`sudo systemctl start dokeepalive.service`

Check the status with:

`sudo systemctl status dokeepalive.service`

###### Configuration file

dokeepalive will look for a configuration file in its home directory called `dokeepalive.conf`. It can handle multiple
users, and multiple sites per user.

You need the digital ocean api token for each user, the droplet ID of the droplet you intend to monitor/reboot, the port
of the service you want to test, and the interval at which you want to test.

The interval can use s, m, h, d for seconds, minutes, hours, or days. You can only use a single character, so if you
want to have a day and a half, you should probably use the lowest interval you need to have precision on, such as hours.
This means the interval would be "36h", for instance.

The `description` field is only for your information, and is not used by the program. It can be left out if you desire
as well.

```json
[
  {
    "token": "YOUR DIGITALOCEAN API TOKEN",
    "description": "DESCRIPTION OF TOKEN",
    "sites": [
      {
        "droplet_id": "DROPLET ID",
        "host": "DOMAIN OR IP OF DROPLET",
        "port": "PORT TO CHECK",
        "interval": "5m"
      }
    ]
  }
]
```