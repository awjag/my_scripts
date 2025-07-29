python3 get-most-visited-domains.sh_python.py | awk -F'\t' '{ usage[$1] += $2 } END { for (webpage in usage) print webpage, "\t", usage[webpage] " " }'  | sort -k2 -nr

# got rid of word seconds xd
