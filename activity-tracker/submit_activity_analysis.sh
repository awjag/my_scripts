cd $SCRIPTS_DIR/activity-tracker/
MIN_UPTIME=600
echo "$(cat /proc/uptime | awk '{print $1}') > 999" | bc -l

#Step 1: run get-recent-web-activity.sh - it outputs to recent-activity.txt
$SCRIPTS_DIR/activity-tracker/get-recent-web-activity.sh

#Step 2: run graphical-summary.py - it outputs a pdf
python3 $SCRIPTS_DIR/activity-tracker/graphical-summary.py

#Step 3: take the outputted pdf and email it to a friend.
mv $SCRIPTS_DIR/activity-tracker/productivity_report.pdf  "$SCRIPTS_DIR/activity-tracker/$(date "+%B-%d-%Y--%I_%M_%S_%p___Productivity_Report.pdf")"

# MAKE SURE last-web-activity IS UPDATED? I think get-recent-web-activity.sh will automatically update it BUT ONLY IF YOU LET IT which it does WHEN IT ECHOES THE NEW EJND TIME STAMP

# Step 4: MAKE SURE TO DELETE focus_log.csv
rm $SCRIPTS_DIR/activity-tracker/focus_log.csv
rm $SCRIPTS_DIR/activity-tracker/focused_webpage_log.tsv
