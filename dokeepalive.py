from config import frequency, domain_port_droplet
from datetime import datetime, timedelta
from scapy.all import *


def port_is_open(domain, port):
    ip = socket.gethostbyname(domain)
    request = IP(dst=ip)/TCP(dport=port, flags="S")
    resp = sr1(request, timeout=1, verbose=0)
    try:
        if resp.getlayer(TCP).flags == "SA":
            return True
    except AttributeError:
        return False


def main():
    while True:
        # Iterate over domains
        for i in range(len(domain_port_droplet)):
            (domain, port, droplet, last_checked) = domain_port_droplet[i]
            # Check if domain has been tested already, set time to 5 minutes ago so it will start immediately.
            if last_checked is None:
                last_checked = domain_port_droplet[i][3] = datetime.now() - timedelta(minutes=frequency)
            # If the last time domain was checked was over 5 minutes ago, check again.
            if datetime.now() - last_checked > timedelta(minutes=frequency):
                # Reset the last checked time to now.
                domain_port_droplet[i][3] = datetime.now()
                # If the port is not open, server is down, so restart.
                if not port_is_open(domain, port):
                    now = datetime.now()
                    droplet.reboot()
                    with open("dokeepalive.log", "a") as logfile:
                        logfile.write("Site " + domain + " down - " + str(now) + "\n")


if __name__ == '__main__':
    main()
