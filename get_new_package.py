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


def verify_for_package(json_package_path, base_url):
    global packages

    initial_req = requests.get(base_url, allow_redirects=False)
    initial_req.raise_for_status()
    url = initial_req.headers["Location"]
    filename = url.split("/")[-1]

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


versions = {
    "stable": {
        "url": "https://discord.com/api/download?platform=linux&format=deb",
        "package_json": "stable_packages.json"
    },
    "ptb": {
        "url": "https://discord.com/api/download/ptb?platform=linux&format=deb",
        "package_json": "ptb_packages.json"
    },
    "canary": {
        "url": "https://discord.com/api/download/canary?platform=linux&format=deb",
        "package_json": "canary_packages.json"
    }
}

return_code = 1

for _version_name, version in versions.items():
    code = verify_for_package(version["package_json"], version["url"])
    return_code = min(code, return_code)

exit(return_code)
