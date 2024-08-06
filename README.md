# Discord APT repository

As has been [repeatedly asked for](https://support.discord.com/hc/en-us/community/posts/360031737491-Give-us-an-apt-repository-Linux-), this is an APT repository for Discord. Note that I do not in anyway claim ownership over the .deb files here, this is just merely a nicer packaging option. Discord: if you want to do this yourself, please tell me about it and I'll point people there instead!

## Usage instructions

1. Create a file `/etc/apt/sources.list.d/discord.list` with the contents `deb https://palfrey.github.io/discord-apt/debian/ ./`
2. Download the file https://palfrey.github.io/discord-apt/discord-apt.gpg.asc to `/etc/apt/trusted.gpg.d`
3. `sudo apt-get update`
4. Install the desired version

| Version | Command                               |
| ------- | ------------------------------------- |
| Stable  | `sudo apt-get install discord`        |
| PTB     | `sudo apt-get install discord-ptb`    |
| Canary  | `sudo apt-get install discord-canary` |

BTW, if you want full-colour emojis, install `fonts-noto-color-emoji`. The discord packages really should depend on that, but apparently don't for some reason.

(I have no interest in PRs to improve these instructions or helper scripts for this. They're not very hard, but I don't want to provide free support here for anyone who can't follow those instructions. If you disagree with this, either bug Discord into supporting this themselves or fork this repo and do whatever in your fork.)

## Manual update instructions

This should not be needed, as `.github/workflows/update.yml` should do this, but just in case..

1. `pip install -r requirements.txt`
2. `python get_new_package.py`
   - If this says `already have discord-<version>.deb` and there's no new .debs in the repo, there's nothing to do further.
3. `export KEY_PASSPHRASE=<key phrase for the Discord Apt Repository key>`
4. `make debian/Release.gpg`, which should regenerate all the other files.
5. Commit, push, etc and the Github Pages automation will deal with the rest.
