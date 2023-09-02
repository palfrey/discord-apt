debian/Packages: debian/pool/*.deb
	cd debian && dpkg-scanpackages --multiversion . > Packages

debian/Packages.gz: debian/Packages
	cd debian && gzip -9c Packages > Packages.gz

debian/Release: debian/Packages debian/Packages.gz
	cd debian && apt-ftparchive release . > Release

debian/Release.gz: debian/Release
	cd debian && gzip -9c Release > Release.gz

debian/Release.gpg: debian/Release
	cd debian && rm -f Release.gpg && (echo ${KEY_PASSPHRASE} | gpg --pinentry-mode loopback --passphrase-fd 0 -abs -o Release.gpg --local-user "Discord Apt Repository" Release)