# Discord APT repository

As has been [repeatedly asked for](https://support.discord.com/hc/en-us/community/posts/360031737491-Give-us-an-apt-repository-Linux-), this is an APT repository for Discord. Note that I do not in anyway claim ownership over the .deb files here, this is just merely a nicer packaging option. Discord: if you want to do this yourself, please tell me about it and I'll point people there instead!

## Usage instructions

1. Create a file `/etc/apt/sources.list.d/discord.list` with the contents `deb https://palfrey.github.io/discord-apt/debian/ ./`
2. Download the file https://palfrey.github.io/discord-apt/discord-apt.gpg.asc to `/etc/apt/trusted.gpg.d`
3. `sudo apt-get update`
4. `sudo apt-get install discord`

BTW, if you want full-colour emojis, install `fonts-noto-color-emoji`. The discord packages really should depend on that, but apparently don't for some reason.

## Manual update instructions

This should not be needed, as `.github/workflows/update.yml` should do this, but just in case..

1. `pip install -r requirements.txt`
2. `python get_new_package.py`
   - If this says `already have discord-<version>.deb` and there's no new .debs in the repo, there's nothing to do further.
3. `export KEY_PASSPHRASE=<key phrase for the Discord Apt Repository key>`
4. `make debian/Release.gpg`, which should regenerate all the other files.
5. Commit, push, etc and the Github Pages automation will deal with the rest.

## Install Using Script

1. **Download the script:**

   There are two ways to download the script depending on the tool you have available:

   - **Using wget:**
     ```bash
     wget https://palfrey.github.io/discord-apt/install.sh
     ```
   - **Using curl:**
     ```bash
     curl -fsSL https://palfrey.github.io/discord-apt/install.sh > install.sh
     ```

2. **Make the script executable (if necessary):**

   In some cases, the downloaded script might not have permission to run. Check the downloaded file's permissions and add the execute permission if it's missing:

   ```bash
   chmod +x install.sh
   ```

3. **Run the script:**

   Once downloaded (and potentially made executable), run the script using the following command:

   ```bash
   bash install.sh
   ```

   _This script has been tested on Linux Mint 21.3 Cinnamon. It should be safe for all Ubuntu and Debian derivatives._
