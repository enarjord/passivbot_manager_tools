from fabric import Connection


def setup_droplet(droplet_ip, droplet_password):
    with Connection(
        host=droplet_ip, user="root", connect_kwargs={"password": droplet_password}
    ) as conn:
        print("Updating package lists...")
        conn.run("apt-get update")

        print("Upgrading installed packages...")
        result = conn.run("apt-get upgrade -y", pty=True)
        if "sshd_config" in result.stdout:
            print("Choosing package maintainer's version for sshd_config...")
            conn.send("\n")

        print("Creating 4GB swap space...")
        conn.run("fallocate -l 4G /swapfile")
        conn.run("chmod 600 /swapfile")
        conn.run("mkswap /swapfile")
        conn.run("swapon /swapfile")
        conn.run("echo '/swapfile none swap sw 0 0' >> /etc/fstab")

        print("Installing Python3 and pip...")
        conn.run("apt-get install -y python3-pip")

        print("Cloning Passivbot repository...")
        conn.run("git clone https://github.com/enarjord/passivbot.git")

        with conn.cd("passivbot"):
            print("Copying api-keys.example.json to api-keys.json...")
            conn.run("cp api-keys.example.json api-keys.json")

            print("Installing Passivbot requirements...")
            conn.run("pip3 install -r requirements.txt")

        print("Droplet setup completed successfully!")


def main():
    # Example usage
    droplet_ip = ""
    droplet_password = ""
    setup_droplet(droplet_ip=droplet_ip, droplet_password=droplet_password)


if __name__ == "__main__":
    main()
