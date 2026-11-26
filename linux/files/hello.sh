#!/bin/bash
# Says hello to whoever you name, and tells you about this computer.
name="${1:-there}"

echo "Hello, $name!"
echo "This is $(hostname), and it's $(date +%A)."

hour=$(date +%H)
if [ "$hour" -lt 12 ]; then
  echo "Good morning — coffee time."
elif [ "$hour" -lt 17 ]; then
  echo "Good afternoon — still coffee time."
else
  echo "Good evening — the café is closed."
fi

for item in "Flat white" "Latte" "Chai"; do
  echo "On the menu: $item"
done
