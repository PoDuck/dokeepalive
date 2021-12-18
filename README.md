DO Keepalive is a small script to keep tabs on servers that tend to freeze up on digitalocean.  It will check if a given port is open, and if it isn't, it will use the DO(Digitalocean) API to reboot the server.

1. Clone this repository into a folder on your stable server.
2. Create a virtual environment for the repository
3. `pip install -r requirements.txt`
4. `python create_config.py` and follow instructions.
5. add `@reboot sleep 60 && /path/to/virtualenv/python /path/to/dokeepalive.py` to crontab.  change the sleep period to suit the amount of time your system may take to fully boot.
6. Reboot the machine, or run dokeepalive.py.