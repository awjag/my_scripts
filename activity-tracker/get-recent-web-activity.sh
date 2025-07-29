#!/bin/bash
PREVIOUS_END_TIMESTAMP="$(cat $SCRIPTS_DIR/activity-tracker/last-web-activity)"
RECENT_ACTIVITY="$(sqlite3 -separator " ||APESEPARATOR|| " ~/.config/local/qutebrowser/history.sqlite "SELECT url,title,atime FROM History" | sed 's/ ||APESEPARATOR|| /\t/g' | awk -F '\t' -v prev="$PREVIOUS_END_TIMESTAMP" '$3 > prev' )"
RECENT_ACTIVITY_READABLE_TIMESTAMPS="$(echo "$RECENT_ACTIVITY" |  awk -F '\t' '{
  cmd = "date -d @" $3 " \"+%Y-%m-%d %H:%M:%S%P\""
  cmd | getline humantime
  close(cmd)
  print $1 "\t" $2 "\t" humantime
}' )"

echo "----------------Web Browser History--------------------"

#echo "$RECENT_ACTIVITY" > recent-activity.txt
#echo "------------------------------------------" >> recent-activity.txt
#echo "$RECENT_ACTIVITY_READABLE_TIMESTAMPS" >> recent-activity.txt
echo "$RECENT_ACTIVITY_READABLE_TIMESTAMPS" > recent-activity.txt
NEW_END_TIMESTAMP="$(echo "$RECENT_ACTIVITY" | tail -n 1 | awk -F '\t' '{print $3}')"

echo "The old last-web-activity contained: |$PREVIOUS_END_TIMESTAMP|"
echo "The new last-web-activity will contain: |$NEW_END_TIMESTAMP|"
echo "$NEW_END_TIMESTAMP" > last-web-activity

#ACTIVITY="$(sqlite3 -separator " ||APESEPARATOR|| " ~/.config/local/qutebrowser/history.sqlite "SELECT url,title,atime FROM History" | sed 's/ ||APESEPARATOR|| /\t/g')"
#LAST_TIMESTAMP="$(echo "$ACTIVITY" | awk -F '\t' '{print $3}' | tail -n 1)"
#echo "
