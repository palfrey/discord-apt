import json
from pathlib import Path
import shutil
import requests
from sys import exit, argv

# Constants
###########
root = Path(__file__).parent
debian = root.joinpath("debian")
packages = debian.joinpath("Packages").open().read()
###########


def verify_for_package(json_package_path, url, filename):
    global packages
    packages_list = Path(json_package_path)
    if filename not in packages or (len(argv) > 1 and argv[1] == "--force"):
        with packages_list.open() as raw_packages:
            existing_packages = json.load(raw_packages)
        existing_packages[filename] = url
        sorted_keys = sorted(existing_packages.keys())
        while len(existing_packages) > 5:
            key = sorted_keys[0]
            del existing_packages[key]
            sorted_keys = sorted_keys[1:]

        json.dump(existing_packages, packages_list.open("w"), indent=2)

        for package_name, package_url in existing_packages.items():
            if debian.joinpath("pool", package_name).exists():
                continue
            print("getting", package_name)
            with requests.get(package_url, stream=True) as r:
                local_path = debian.joinpath("pool", package_name)
                with local_path.open('wb') as f:
                    shutil.copyfileobj(r.raw, f)
        return 0
    else:
        print(f"Already have {filename}", url)
        return 1


# For Stable Version
####################
stable_initial_req = requests.get(
    "https://discord.com/api/download?platform=linux&format=deb", allow_redirects=False)
stable_initial_req.raise_for_status()

stable_url = stable_initial_req.headers["Location"]
stable_filename = stable_url.split("/")[-1]

verify_for_package("stable_packages.json", stable_url, stable_filename)
####################

# For PTB Version
#################
ptb_initial_req = requests.get(
    "https://discord.com/api/download/ptb?platform=linux&format=deb", allow_redirects=False)
ptb_initial_req.raise_for_status()

ptb_url = ptb_initial_req.headers["Location"]
ptb_filename = ptb_url.split("/")[-1]

verify_for_package("ptb_packages.json", ptb_url, ptb_filename)
#################

# For Canary Version
####################
canary_initial_req = requests.get(
    "https://discord.com/api/download/canary?platform=linux&format=deb", allow_redirects=False)
canary_initial_req.raise_for_status()

canary_url = canary_initial_req.headers["Location"]
canary_filename = canary_url.split("/")[-1]

verify_for_package("canary_packages.json", canary_url, canary_filename)
####################
