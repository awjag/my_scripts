awk -F'\t' '{ usage[$1] += $2 } END { for (webpage in usage) print webpage, "\t", usage[webpage] " seconds" }' $SCRIPTS_DIR/activity-tracker/focused_webpage_log.tsv | sort -k2 -nr
