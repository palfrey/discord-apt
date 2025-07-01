import json
from pathlib import Path
import shutil
import requests
from sys import exit, argv
import re
from typing import Dict, List, Tuple

# Constants
###########
root = Path(__file__).parent
debian = root.joinpath("debian")
packages_file = debian.joinpath("Packages")
MAX_PACKAGES = 3
###########

def parse_version(filename: str) -> Tuple[int, int, int]:
    """Extract version numbers from filename for proper sorting."""
    match = re.search(r'(\d+)\.(\d+)\.(\d+)', filename)
    if match:
        return (int(match.group(1)), int(match.group(2)), int(match.group(3)))
    return (0, 0, 0)

def sort_packages_by_version(packages: Dict[str, str]) -> List[str]:
    """Sort package filenames by version number, newest first."""
    return sorted(packages.keys(), key=parse_version, reverse=True)

def missing_packages(base_url: str, json_package_path: str) -> bool:
    """Check if we need to download new packages."""
    try:
        initial_req = requests.get(base_url, allow_redirects=False, timeout=30)
        initial_req.raise_for_status()
        url = initial_req.headers["Location"]
        filename = url.split("/")[-1]
        
        # Check if forced update
        if len(argv) > 1 and argv[1] == "--force":
            return True
            
        # Check JSON package list
        json_file = Path(json_package_path)
        if json_file.exists():
            with json_file.open() as f:
                existing_packages = json.load(f)
            return filename not in existing_packages
        
        return True
        
    except Exception as e:
        print(f"Error checking packages for {base_url}: {e}")
        return False

def get_all_packages(json_package_path: str, base_url: str) -> None:
    """Download and manage packages with proper version sorting."""
    try:
        # Get current package info
        initial_req = requests.get(base_url, allow_redirects=False, timeout=30)
        initial_req.raise_for_status()
        url = initial_req.headers["Location"]
        filename = url.split("/")[-1]
        
        print(f"Latest available: {filename}")
        
        # Load existing packages
        packages_list = Path(json_package_path)
        if packages_list.exists():
            with packages_list.open() as raw_packages:
                existing_packages = json.load(raw_packages)
        else:
            existing_packages = {}
        
        # Add new package if not exists or forced
        if filename not in existing_packages or (len(argv) > 1 and argv[1] == "--force"):
            existing_packages[filename] = url
            print(f"Added {filename} to download list")
        
        # Sort by version (newest first) and keep only MAX_PACKAGES
        sorted_filenames = sort_packages_by_version(existing_packages)
        if len(sorted_filenames) > MAX_PACKAGES:
            # Keep only the newest MAX_PACKAGES
            to_keep = sorted_filenames[:MAX_PACKAGES]
            existing_packages = {k: v for k, v in existing_packages.items() if k in to_keep}
            print(f"Keeping {MAX_PACKAGES} newest packages: {to_keep}")
        
        # Save updated package list
        packages_list.parent.mkdir(parents=True, exist_ok=True)
        with packages_list.open("w") as f:
            json.dump(existing_packages, f, indent=2, sort_keys=True)
        
        # Download missing packages
        pool_dir = debian.joinpath("pool")
        pool_dir.mkdir(parents=True, exist_ok=True)
        
        for package_name, package_url in existing_packages.items():
            local_path = pool_dir.joinpath(package_name)
            if local_path.exists():
                print(f"Already exists: {package_name}")
                continue
                
            print(f"Downloading: {package_name}")
            try:
                with requests.get(package_url, stream=True, timeout=60) as r:
                    r.raise_for_status()
                    with local_path.open('wb') as f:
                        shutil.copyfileobj(r.raw, f)
                print(f"Downloaded: {package_name}")
            except Exception as e:
                print(f"Failed to download {package_name}: {e}")
                # Remove from list if download failed
                if local_path.exists():
                    local_path.unlink()
                    
    except Exception as e:
        print(f"Error in get_all_packages for {base_url}: {e}")

def main():
    """Main function to orchestrate package downloads."""
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
    
    # Ensure debian directory exists
    debian.mkdir(parents=True, exist_ok=True)
    
    # Check if any packages are missing
    any_missing = False
    for version_name, version_info in versions.items():
        print(f"Checking {version_name}...")
        if missing_packages(version_info["url"], version_info["package_json"]):
            any_missing = True
            print(f"  {version_name}: Updates available")
        else:
            print(f"  {version_name}: Up to date")
    
    if not any_missing:
        print("All packages are up to date")
        return 0
    
    print("\nDownloading packages...")
    for version_name, version_info in versions.items():
        print(f"\n--- Processing {version_name} ---")
        get_all_packages(version_info["package_json"], version_info["url"])
    
    print("\nDownload complete!")
    return 0

if __name__ == "__main__":
    exit(main())
