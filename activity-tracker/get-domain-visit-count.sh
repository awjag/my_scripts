python3 get-most-visited-domains.sh_python.py  | awk '{print $1}' | sort | uniq -c | sort -k2 -nr
