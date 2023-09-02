from pathlib import Path
import shutil
import requests


initial_req = requests.get("https://discord.com/api/download?platform=linux&format=deb", allow_redirects=False)
initial_req.raise_for_status()

url = initial_req.headers["Location"]
filename = url.split("/")[-1]
debian_pool = Path(__file__).parent.joinpath("debian", "pool")
local_path = debian_pool.joinpath(filename)
if not local_path.exists():
    print("getting", filename)
    with requests.get(url, stream=True) as r:
        with local_path.open('wb') as f:
            shutil.copyfileobj(r.raw, f)
else:
    print(f"Already have {filename}")