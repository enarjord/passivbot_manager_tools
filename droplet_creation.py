import json
import os
import random
import string
from dataclasses import asdict, dataclass

import digitalocean

# Replace with your Digital Ocean API token
TOKEN = "your_digitalocean_api_token"

# Initialize the DigitalOcean API client
client = digitalocean.Client(token=TOKEN)


# Define the dataclass to store droplet information
@dataclass
class DropletInfo:
    name: str
    ip_address: str
    password: str


# Function to generate a random droplet name
def generate_droplet_name():
    adjectives = ["tiny", "cloudy", "misty", "sunny", "bright", "warm", "cool", "calm"]
    nouns = ["droplet", "instance", "server", "node", "machine", "host", "cloud"]
    adjective = random.choice(adjectives)
    noun = random.choice(nouns)
    return f"{adjective}-{noun}"


# Function to create a new droplet
def create_droplet():
    # Generate a random droplet name
    droplet_name = generate_droplet_name()

    # Create a new Droplet
    droplet = digitalocean.Droplet(
        token=TOKEN,
        name=droplet_name,
        region="sgp1",  # Singapore
        image="ubuntu-22-04-x64",
        size_slug="s-1vcpu-512mb-10gb",  # Smallest droplet size
        backups=False,
        ipv6=False,
        user_data=None,
        ssh_keys=None,
        monitoring=False,
        vpc_uuid=None,
        tags=None,
    )
    droplet.create()

    # Generate a random password
    password = "".join(random.choices(string.ascii_letters + string.digits, k=12))

    # Retrieve the droplet's IP address
    ip_address = droplet.ip_address

    # Store droplet information in a dictionary
    droplet_info = DropletInfo(name=droplet_name, ip_address=ip_address, password=password)

    # Save droplet information to a JSON file
    save_droplet_info(droplet_info)

    return droplet_info


# Function to save droplet information to a JSON file
def save_droplet_info(droplet_info):
    file_path = "droplets.json"
    data = []

    # Check if the file exists
    if os.path.isfile(file_path):
        # Load existing data from the file
        with open(file_path, "r") as file:
            data = json.load(file)

    # Append the new droplet information to the data
    data.append(asdict(droplet_info))

    # Write the updated data to the file
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)

    print(f"Droplet information saved to {file_path}")


# Example usage
if __name__ == "__main__":
    droplet_info = create_droplet()
    print(f"Droplet Name: {droplet_info.name}")
    print(f"IP Address: {droplet_info.ip_address}")
    print(f"Password: {droplet_info.password}")
