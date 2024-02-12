hotkey-fix:
	sudo add-apt-repository ppa:nrbrtx/xorg-hotkeys
	sudo apt-get update
	sudo apt-get dist-upgrade
	sudo apt install --reinstall xserver-xorg-input-all
	sudo dpkg-reconfigure keyboard-configuration
	sudo apt-get install kwin-addons
