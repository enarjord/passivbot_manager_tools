import json
import os
import random
import string
from datetime import datetime
from dataclasses import asdict, dataclass

import digitalocean

# Replace with your Digital Ocean API token
TOKEN = "YOUR_TOKEN"

# Initialize the DigitalOcean API client
manager = digitalocean.Manager(token=TOKEN)


# Define the dataclass to store droplet information
@dataclass
class DropletInfo:
    name: str
    ip_address: str
    password: str


def generate_droplet_name():
    adjectives = ["tiny", "cloudy", "misty", "sunny", "bright", "warm", "cool", "calm"]
    nouns = ["droplet", "instance", "server", "node", "machine", "host", "cloud"]
    adjective = random.choice(adjectives)
    noun = random.choice(nouns)

    # Get the current date and time, precise to seconds
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")

    # Generate a random string
    random_string = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))

    # Combine the adjective, noun, timestamp, and random string
    unique_name = f"{adjective}-{noun}-{timestamp}-{random_string}"
    return unique_name


# Function to create a new droplet
def create_droplet():
    # Generate a unique droplet name
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
        ssh_keys=[],
        monitoring=False,
        vpc_uuid=None,
        tags=None,
    )
    droplet.create(manager)

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
