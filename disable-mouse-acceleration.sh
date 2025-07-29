TRACKPAD_ID="$(xinput list | grep "Touchpad" | sed 's/.*id=//' | awk '{print $1}')"
xinput --set-prop "$TRACKPAD_ID" "libinput Accel Profile Enabled" 0, 1
