awk -F',' '{ usage[$2] += $3 } END { for (app in usage) print app, "\t", usage[app] " seconds" }' $SCRIPTS_DIR/activity-tracker/focus_log.csv | sort -k2 -nr
