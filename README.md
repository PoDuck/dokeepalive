DO Keepalive is a small script to keep tabs on DigitalOcean servers that have a tendency to freeze up.  It will check if a given port is open, and if it isn't, it will use the DO(Digitalocean) API to reboot the server.

Due to this script using low level network access, you must run this script as root.  You can either do this from the command line by using sudo, or you can add it to root's crontab with `sudo crontab -e`

1. Clone this repository into a folder on your stable server.
2. Create a virtual environment for the repository
3. `pip install -r requirements.txt`
4. `python create_config.py` and follow instructions.
5. add `@reboot sleep 60 && /path/to/virtualenv/python /path/to/dokeepalive.py` to root's crontab.  change the sleep period (60) to suit the amount of time, in seconds, your system may take to fully boot.
6. Reboot the machine, or run dokeepalive.py.