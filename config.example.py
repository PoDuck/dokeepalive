import digitalocean

# Add your digital ocean API token
manager = digitalocean.Manager(token="DO_TOKEN")

# add list of "[DOMAIN, PORT, DROPLET_ID]" for each site
domain_port_droplet = [
    # ["DOMAIN", PORT#, DROPLET_ID],
]

# Do not edit below this line
for i in range(len(domain_port_droplet)):
    domain, port, droplet = domain_port_droplet[i]
    domain_port_droplet[i] = [domain, port, manager.get_droplet(droplet_id=str(droplet)), None]
