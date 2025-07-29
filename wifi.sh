SELECTION="$1"
if [ "$SELECTION" = "on" ]; then
	sudo systemctl start NetworkManager 
else
	sudo systemctl stop NetworkManager
fi
