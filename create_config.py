#!/usr/bin/python
from string import Template


def main():
    frequency = input("Enter interval in minutes to poll server status: ")
    DO_Token = input("Enter your Digital Ocean API token: ")
    domain_info = []
    while True:
        print("For each domain, enter the domain, the port to check, and the droplet ID."
              "  When finished, enter a blank line on the domain line to stop.")
        domain = input("Domain (blank to stop input): ")
        if not domain:
            break
        port = input("Port: ")
        droplet_id = input("Droplet ID: ")
        domain_info.append(['"' + domain + '"', port, droplet_id])

    if domain_info:
        domains = []
        domain_list = "[\n"
        for domain in domain_info:
            domain_list += '    [' + ', '.join(domain) + '],\n'
        domain_list += ']'
        sub = {
            'FREQUENCY': frequency,
            'DO_TOKEN': DO_Token,
            'LIST': domain_list
        }
        with open('config.template', 'r') as f:
            src = Template(f.read())
            result = src.substitute(sub)
            f.close()

        with open('config.py', 'w') as f:
            f.write(result)
            f.close()


if __name__ == '__main__':
    main()
