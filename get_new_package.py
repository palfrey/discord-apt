import json
from pathlib import Path
import shutil
import requests
from sys import exit, argv

root = Path(__file__).parent
debian = root.joinpath("debian")

initial_req = requests.get("https://discord.com/api/download?platform=linux&format=deb", allow_redirects=False)
initial_req.raise_for_status()

packages = debian.joinpath("Packages").open().read()

url = initial_req.headers["Location"]
filename = url.split("/")[-1]

packages_list = Path("packages.json")

if filename not in packages or (len(argv) > 1 and argv[1] == "--force"):
    with packages_list.open() as raw_packages:
        existing_packages = json.load(raw_packages)
    existing_packages[filename]= url
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
    exit(0)    
else:
    print(f"Already have {filename}", url)
    exit(1)