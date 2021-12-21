import logging
from datetime import timedelta
from scapy.all import *
import digitalocean
import json
import re


# logging.basicConfig(filename="dokeepalive.log", filemode="a", format='%(asctime)s - %(message)s', level=logging.INFO)
formatter = logging.Formatter('%asctime)s %(levelname)s %(message)s')


def logger_setup(name, log_file, level=logging.INFO):
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger


logger = logger_setup('info_logger', 'access.log')
error_logger = logger_setup('error_logger', 'error.log', logging.ERROR)


def port_is_open(domain, port):
    ip = socket.gethostbyname(domain)
    request = IP(dst=ip)/TCP(dport=port, flags="S")
    resp = sr1(request, timeout=1, verbose=0)
    try:
        if resp.getlayer(TCP).flags == "SA":
            return True
    except AttributeError:
        return False


class Site(object):
    def __init__(self, site_data, manager):
        self.site_data = site_data
        self.manager = manager
        self.droplet_id = str(site_data['droplet_id'])
        self.droplet = self.manager.get_droplet(droplet_id=self.droplet_id)
        self.host = site_data['host']
        self.port = int(site_data['port'])
        temp = re.compile("([0-9]+)([a-zA-Z]+)")
        res = temp.match(site_data['interval']).groups()
        if res[1] == "s":
            self.interval = timedelta(seconds=int(res[0]))
        elif res[1] == "m":
            self.interval = timedelta(minutes=int(res[0]))
        elif res[1] == "h":
            self.interval = timedelta(hours=int(res[0]))
        elif res[1] == "d":
            self.interval = timedelta(hours=int(res[0]))
        self.last_checked = datetime.now() - self.interval

    def reboot(self):
        self.droplet.reboot()

    def update(self):
        now = datetime.now()
        if self.last_checked <= now - self.interval:
            if not port_is_open(self.host, self.port):
                error_logger.error("Site: " + self.host + " was reported not responsive")
                self.reboot()
            else:
                logger.info("Site: " + self.host + " was reported open")
            self.last_checked = now


class User(object):
    def __init__(self, user_data):
        self.sites = []
        self.token = user_data['token']
        self.manager = digitalocean.Manager(token=self.token)
        for site in user_data['sites']:
            self.sites.append(Site(site, self.manager))

    def update(self):
        for site in self.sites:
            site.update()


class UsersAndSites(object):
    def __init__(self):
        with open("dokeepalive.conf") as config_data:
            self.apis = json.load(config_data)
        self.users = []
        for user in self.apis:
            self.users.append(User(user))

    def update(self):
        for user in self.users:
            user.update()


def main():
    dka = UsersAndSites()
    while True:
        dka.update()


if __name__ == '__main__':
    main()
