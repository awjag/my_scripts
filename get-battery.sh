charging="$(upower -i /org/freedesktop/UPower/devices/battery_BAT0 | grep state | awk '{print $2}')"
[ "$charging" = "charging" ] && printf "^^^^" || printf " vv "
bat="$(upower -i /org/freedesktop/UPower/devices/battery_BAT0 | grep perce | awk '{print $2}' | sed "s/%//")"
echo "$bat"
if (( $bat <= 10 )) && [ "$charging" != "charging" ]; then
	notify-send -u CRITICAL "Battery Warning" "<span font='30px'>BATTERY IS LOW</span>" -t 3000
	$SCRIPTS_DIR/set-brightness.sh 3%- > /dev/null
	if (( $bat <= 8 && $bat > 5 )); then
		notify-send -u CRITICAL "WIFI and Bluetooth shutoff IMMINENT" "<span font='20px'>AIRPLANE MODE ACTIVATING at 5%</span>" -t 3000
	elif (( $bat <= 5 )); then
		$SCRIPTS_DIR/set-brightness.sh 1% > /dev/null
		notify-send -u CRITICAL "Battery Warning" "<span font='20px'>Airplane Mode is on</span> <span font='40px'>Shutting down at 3%</span>" -t 3000
		rfkill block all
	elif (( $bat <= 3 )); then
		i3-msg exit
		sleep 3
		$SCRIPTS_DIR/activity-tracker/shutdown.sh now
	fi
elif (( $bat >= 85 )) && [ "$charging" = "charging" ]; then
	notify-send -u CRITICAL "Battery Warning" "<span font='40px'>BATTERY IS VERY HIGH</span> - DAMAGE TO BATTERY IMMINENT" -t 5000 -h "INT:x:800,INT:y:470" -i /usr/share/icons/Adwaita/symbolic/legacy/battery-full-charging-symbolic.svg
fi
