#!/usr/bin/python
import time
from config import droplet, domain
from datetime import datetime
import socket


def port_is_open(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((domain, port)) == 0


def main():
    while True:
        if not port_is_open(443):
            now = datetime.now()
            droplet.reboot()
            with open("dokeepalive.log", "a+") as logfile:
                logfile.write("Site down - " + str(now))
        time.sleep(300)


if __name__ == '__main__':
    main()
