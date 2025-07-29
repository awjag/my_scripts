#!/bin/bash

logfile=$SCRIPTS_DIR/activity-tracker/focus_log.csv
last_app=""
last_time=$(date +%s)

while true; do
    app=$(i3-msg -t get_tree | jq -r '.. | objects | select(.window_properties? and .focused == true) | .window_properties.class')
    now=$(date +%s)

    if [ "$app" != "$last_app" ]; then
        if [ -n "$last_app" ]; then
            duration=$((now - last_time))
            echo "$(date +%Y-%m-%d\ %H:%M:%S),$last_app,$duration" >> "$logfile"
        fi
        last_app=$app
        last_time=$now
    fi

    sleep 1
done
