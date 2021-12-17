import digitalocean

manager = digitalocean.Manager(token="DIGITAL OCEAN TOKEN HERE")
domain = "DOMAIN TO TEST"
droplet = manager.get_droplet(droplet_id="DROPLET ID")
