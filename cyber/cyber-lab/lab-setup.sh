#!/bin/bash
# Sets up the Corner Café practice lab on YOUR OWN Ubuntu practice server: the café website, a staff app with
# security bugs on purpose (Module 5), and a few realistic mistakes for you to find. Never run it on a real server.
#   ./lab-setup.sh        (run it again after restarting the server)
set -euo pipefail
cd "$(dirname "$0")"

echo "== Installing nginx, Python Flask and SQLite"
sudo apt-get update -qq
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq nginx python3-flask sqlite3 > /dev/null

echo "== The café website"
sudo cp site/*.html /var/www/html/

echo "== The staff orders app on port 5000 (it has security bugs on purpose)"
mkdir -p ~/cafe-app && cp cafe_app.py ~/cafe-app/
sudo systemctl stop cafe-app 2> /dev/null || true
sudo systemd-run --quiet --unit=cafe-app --uid="$USER" --working-directory="$HOME/cafe-app" python3 cafe_app.py

echo "== A few mistakes for you to find"
# a test web server someone forgot to turn off, sharing a folder that has a secrets file in it
mkdir -p ~/old-test && cp env-example ~/old-test/.env && echo "Test page — delete me" > ~/old-test/index.html
sudo systemctl stop old-test-server 2> /dev/null || true
sudo systemd-run --quiet --unit=old-test-server --uid="$USER" --working-directory="$HOME/old-test" python3 -m http.server 8080
# a shared folder anyone can change
sudo mkdir -p /srv/cafe-shared && sudo chmod 777 /srv/cafe-shared
# the firewall off
sudo ufw --force disable > /dev/null

echo "Lab ready. The café website is at http://$(hostname -I | awk '{print $1}')"
