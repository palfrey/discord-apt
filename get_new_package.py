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

if filename not in packages or (len(argv) > 1 and argv[1] == "--force"):
    print("getting", filename)
    with requests.get(url, stream=True) as r:
        local_path = debian.joinpath("pool", filename)
        with local_path.open('wb') as f:
            shutil.copyfileobj(r.raw, f)        
    exit(0)    
else:
    print(f"Already have {filename}")
    exit(1)