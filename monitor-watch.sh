#!/bin/bash

while true
do
	location=$(dirname "$0")
	monitors=$(xrandr --current  | grep " connected" | wc -l)
	prev=$(cat "$location/status.txt")
	if [[ $monitors -ne $prev ]]; then
		echo "$monitors" > "$location/status.txt"
		[[ $monitors -eq 1 ]] && echo "In single!" && $HOME/scripts/system/monitor.sh -s
		[[ $monitors -eq 2 ]] && echo "In multiple!" && sleep 1 && $HOME/scripts/system/monitor.sh -h
	fi
	sleep 5
done
