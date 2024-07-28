#!/bin/bash

# Check for root privileges
if [[ $EUID -ne 0 ]]; then
    echo "This script requires root privileges. Please run with sudo."
    exit 1
fi

# Check for wget or curl
download_command=""
if command -v wget &>/dev/null; then
    download_command="wget"
elif command -v curl &>/dev/null; then
    download_command="curl"
else
    echo "Error: Neither wget nor curl is installed. Please install one of them."
    exit 1
fi

# Check for discord.list existence and type
if [[ -e /etc/apt/sources.list.d/discord.list ]]; then
    if [[ -d /etc/apt/sources.list.d/discord.list ]]; then
        echo "Error: /etc/apt/sources.list.d/discord.list exists as a directory. Please remove it manually."
        exit 1
    else
        # Prompt to replace content
        read -r -p "/etc/apt/sources.list.d/discord.list already exists. Replace content? (y/N) " replace_content
        if [[ $replace_content =~ ^[Yy]$ ]]; then
            echo "Replacing content..."
        else
            echo "Skipping repository addition."
            exit 0
        fi
    fi
fi

# Add Discord repository (if not replaced)
if [[ ! $replace_content =~ ^[Yy]$ ]]; then # Only if not replaced earlier
    echo "Adding Discord repository..."
    sudo sh -c 'echo "deb https://palfrey.github.io/discord-apt/debian/ ./"> /etc/apt/sources.list.d/discord.list'
fi

# 2. Download GPG key
echo "Downloading Discord GPG key..."
sudo $download_command https://palfrey.github.io/discord-apt/discord-apt.gpg.asc -P /etc/apt/trusted.gpg.d

# 3. Update package lists
echo "Updating package lists..."
sudo apt-get update

# 4. Install Discord
echo "Installing Discord..."
sudo apt-get install discord

echo "Discord installation complete."
