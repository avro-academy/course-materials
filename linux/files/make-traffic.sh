#!/bin/bash
# Sends fake visitors to the website - try: ./make-traffic.sh 400
set -euo pipefail
count="${1:-100}"
pages=(/ / / / / /menu.html /menu.html /menu.html /menu.html /about.html /about.html
  /about.html /favicon.ico /favicon.ico /wp-login.php /contact.html /order /.env)
for ((i = 1; i <= count; i++)); do
  page=${pages[RANDOM % ${#pages[@]}]}
  curl -s -o /dev/null -A "Visitor-$((RANDOM % 40 + 1))" "localhost$page"
done
echo "Sent $count requests"
