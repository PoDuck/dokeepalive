DO Keepalive keeps tabs on DigitalOcean servers that have a tendency to freeze up, or that require a high degree of
availability. It will check if a given port is open, and if it isn't, it will use the DO(Digitalocean) API to reboot the
server. This is much different
than [the method Digitalocean suggests](https://www.digitalocean.com/community/tutorials/how-to-set-up-highly-available-web-servers-with-keepalived-and-floating-ips-on-ubuntu-14-04)
, which fails over to a secondary server only, and makes no attempt to recover the original server if it becomes
unresponsive.

If you really need to ensure that you maintain high availability, you may decide to use dokeepalive in conjunction with
keepalived, just in case the backup server goes down before you notice the main server has failed. In fact, if you run
dokeepalive on both servers and keep tabs on the other, it will ensure that your failover server is available in case
your main server goes down.

### Simple Setup Instructions:

1. Clone this repository into a folder on your stable server.
2. Create a virtual environment for the repository
3. `pip install -r requirements.txt`
4. `python config_setup.py` and follow instructions.
5. It is best to either create a systemd service or create some other way to start the script on boot.
6. Reboot the machine, or run dokeepalive.py.

To create the systemd service, create a file:

`nano /lib/systemd/system/dokeepalive.service`

In that file, paste the following:

```
[Unit]
Description=DOKeepalive Service
After=multi-user.target

[Service]
User=USER_WITH_ACCESS
Group=GROUP_WITH_ACCESS
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

### Configuration file

dokeepalive will look for a configuration file in its home directory called `dokeepalive.conf`. It can handle multiple
users, and multiple sites per user.

You need the digital ocean api token for each user, the droplet ID of the droplet you intend to monitor/reboot, the port
of the service you want to test, and the interval at which you want to test.

The interval can use s, m, h, d for seconds, minutes, hours, or days. As an example, to check every 5 minutes, the
interval should be `5m`. To check every hour and a half, `1h30m`.

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

Finally, if you want to have things be a little easier to setup, there is a docker version at [https://github.com/PoDuck/dokeepalive_docker](https://github.com/PoDuck/dokeepalive_docker) that does most of this for you.