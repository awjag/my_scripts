CHOICE=""
if [ "$1" = "now" ]; then
	CHOICE="Yes"
else
	CHOICE="$(echo -e "Yes\nNo\nExit i3" | dmenu -p "Shutdown?")"
fi
if [ "$CHOICE" = "Yes" ]; then
	$SCRIPTS_DIR/activity-tracker/submit_activity_analysis.sh
	shutdown now
fi
#[ "$CHOICE" = "Exit i3"] && i3-msg exit
