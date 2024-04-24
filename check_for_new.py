import subprocess
import requests
from sys import exit

initial_req = requests.get("https://discord.com/api/download?platform=linux&format=deb", allow_redirects=False)
initial_req.raise_for_status()

url = initial_req.headers["Location"]
filename = url.split("/")[-1]

res = subprocess.check_output(["git", "lfs", "ls-files", "--name-only"], encoding='utf-8')
existing = [f.split("/")[-1] for f in res.splitlines()]

print(filename, existing)
if filename in existing:
    exit(1)
else:
    exit(0)