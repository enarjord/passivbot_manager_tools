import os
import json
import digitalocean
import time

# Replace with your Digital Ocean API token
TOKEN = "YOUR_TOKEN"

# Initialize the DigitalOcean API client
manager = digitalocean.Manager(token=TOKEN)


def get_droplets():
    droplets = manager.get_all_droplets()
    droplet_data = load_droplet_data()

    for droplet in droplets:
        print(f"Name: {droplet.name}")
        print(f"IP Address: {droplet.ip_address}")
        print(f"Region: {droplet.region['name']}")
        print(f"Status: {droplet.status}")
        print(f"Created At: {droplet.created_at}")
        print("---")

        # Update the IP address in the droplet data
        update_droplet_ip(droplet_data, droplet.name, droplet.ip_address)

    # Write the updated data to the file
    save_droplet_data(droplet_data)

    return droplets


def load_droplet_data():
    file_path = "droplets.json"
    data = []

    # Check if the file exists
    if os.path.isfile(file_path):
        # Load existing data from the file
        with open(file_path, "r") as file:
            data = json.load(file)

    return data


def save_droplet_data(data):
    file_path = "droplets.json"

    # Write the updated data to the file
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)


def update_droplet_ip(droplet_data, droplet_name, droplet_ip):
    # Update the IP address for the droplet
    for droplet_info in droplet_data:
        if droplet_info["name"] == droplet_name and droplet_info["ip_address"] is None:
            droplet_info["ip_address"] = droplet_ip
            print(f"Updated IP address for '{droplet_name}' to '{droplet_ip}'")


if __name__ == "__main__":
    print("Retrieving droplet information...")
    get_droplets()
