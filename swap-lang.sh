CURRENT_LAYOUT="$(setxkbmap -query | grep layout | awk '{print $2}')"
NEXT_LAYOUT=""
if [ "$CURRENT_LAYOUT" = "us" ]; then
	NEXT_LAYOUT="gr"
else
	NEXT_LAYOUT="us"
fi
setxkbmap "$NEXT_LAYOUT"
notify-send "Current layout is $NEXT_LAYOUT" -t 2000
