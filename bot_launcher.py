import json
import os
import uuid
from fabric import Connection


def launch_bot(
    droplet_ip,
    droplet_user,
    droplet_password,
    user_first_name,
    user_last_name,
    exchange,
    api_key,
    api_secret,
    api_passphrase,
    market_symbols,
    long_enabled,
    short_enabled,
    total_wallet_exposure_limit_long,
    total_wallet_exposure_limit_short,
):
    # Generate a unique user name
    unique_user_name = f"{user_first_name}_{user_last_name}_{uuid.uuid4().hex[:8]}"

    # Connect to the Droplet
    with Connection(
        host=droplet_ip, user=droplet_user, connect_kwargs={"password": droplet_password}
    ) as conn:
        # Navigate to the Passivbot directory
        with conn.cd("~/passivbot"):
            # Load existing api-keys.json
            api_keys_json = conn.run("cat api-keys.json").stdout

            # Parse the JSON data
            api_keys = json.loads(api_keys_json)

            # Add the new entry
            api_keys[unique_user_name] = {
                "exchange": exchange,
                "key": api_key,
                "secret": api_secret,
                "passphrase": api_passphrase,
            }

            # Save the updated JSON data back to api-keys.json
            new_api_keys_json = json.dumps(api_keys, indent=4)
            conn.run(f"echo '{new_api_keys_json}' > api-keys.json")

            # Create the new HJSON config file
            config_data = {
                "user": unique_user_name,
                "loss_allowance_pct": 0.002,
                "pnls_max_lookback_days": 30,
                "stuck_threshold": 0.9,
                "unstuck_close_pct": 0.01,
                "execution_delay_seconds": 2,
                "auto_gs": True,
                "TWE_long": total_wallet_exposure_limit_long,
                "TWE_short": total_wallet_exposure_limit_short,
                "long_enabled": long_enabled,
                "short_enabled": short_enabled,
                "symbols": market_symbols,
                "live_configs_dir": "configs/live/multisymbol/no_AU/",
                "default_config_path": "configs/live/recursive_grid_mode.example.json",
            }
            config_path = f"configs/live/{unique_user_name}.hjson"
            conn.run(f"echo '{json.dumps(config_data, indent=4)}' > {config_path}")

            # Start a new tmux session and run Passivbot
            session_name = unique_user_name
            conn.run(f"tmux new-session -d -s '{session_name}'")
            conn.run(
                f"tmux send-keys -t '{session_name}' 'python3 passivbot_multi.py {config_path}' Enter"
            )

    print(f"Passivbot instance launched for {user_first_name} {user_last_name} on {droplet_ip}")


def main():
    droplet_ip = ""
    droplet_password = ""

    exchange = "bitget"
    api_key = "key"
    api_secret = "secret"
    api_passphrase = "passphrase"
    market_symbols = [
        "GRTUSDT",
        "HBARUSDT",
        "HOTUSDT",
        "MATICUSDT",
        "RSRUSDT",
        "SUSHIUSDT",
    ]
    long_enabled = True
    short_enabled = False
    total_wallet_exposure_limit_long = 2.1
    total_wallet_exposure_limit_short = 0.1

    # Example usage
    launch_bot(
        droplet_ip=droplet_ip,
        droplet_user="root",
        droplet_password=droplet_password,
        user_first_name="John",
        user_last_name="Doe",
        exchange=exchange,
        api_key=api_key,
        api_secret=api_secret,
        api_passphrase=api_passphrase,
        market_symbols=market_symbols,
        long_enabled=long_enabled,
        short_enabled=short_enabled,
        total_wallet_exposure_limit_long=total_wallet_exposure_limit_long,
        total_wallet_exposure_limit_short=total_wallet_exposure_limit_short,
    )


if __name__ == "__main__":
    main()
