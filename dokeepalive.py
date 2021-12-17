#!/usr/bin/python
import time
from config import domain_port_droplet
from datetime import datetime, timedelta
import socket


def port_is_open(domain, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((domain, port)) == 0


def main():
    while True:
        for i in range(len(domain_port_droplet)):
            (domain, port, droplet, last_checked) = domain_port_droplet[i]
            if last_checked is None:
                last_checked = domain_port_droplet[i][3] = datetime.now() - timedelta(minutes=5)
            if datetime.now() - last_checked > timedelta(minutes=5):
                domain_port_droplet[i][3] = datetime.now()
                if not port_is_open(domain, port):
                    now = datetime.now()
                    droplet.reboot()
                    with open("dokeepalive.log", "a+") as logfile:
                        logfile.write("Site " + domain + " down - " + str(now) + "\n")
        # if not port_is_open(443):
        #     now = datetime.now()
        #     droplet.reboot()
        #     with open("dokeepalive.log", "a+") as logfile:
        #         logfile.write("Site down - " + str(now))
        # time.sleep(300)


if __name__ == '__main__':
    main()
