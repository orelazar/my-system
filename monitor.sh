#!/bin/bash

relaunch_polybar () {
	$HOME/.config/polybar/launch.sh
}

move_all_workspaces () {
	workspaces=$(i3-msg -t get_workspaces | jq -r | grep "name" | sed 's/[",]//g' | awk '{print $2}')
	for i in $workspaces
	do
		i3-msg workspace $i && i3-msg move workspace to output $1
	done
}

while getopts "hsm" opt; do
	case $opt in
		"h")
			echo "home was chosen"
			xrandr --auto
			if [[ $(xrandr --listmonitors | grep "DP-3") ]]; then
				xrandr --output DP-3-1 --left-of eDP-1
				move_all_workspaces DP-3-1
			fi
			if [[ $(xrandr --listmonitors | grep "HDMI") ]]; then 
				xrandr --output HDMI-1 --left-of eDP-1
				i3-msg workspace 2 && i3-msg move workspace to output HDMI-1 
				i3-msg workspace 1 && i3-msg move workspace to output HDMI-1
			fi
			;;
		"s")
			echo "single was chosen!"
			xrandr --auto
			move_all_workspaces eDP-1
			;;
		"m")
			echo "three screens"
			xrandr --auto
			if [[ $(xrandr --listmonitors | grep "DP-3") ]]; then
				xrandr --output DP-3-3 --left-of eDP-1
				xrandr --output DP-3-2 --left-of DP-3-3
				i3-msg workspace 2 && i3-msg move workspace to output DP-3-3
				i3-msg workspace 1 && i3-msg move workspace to output DP-3-3
			fi
			if [[ $(xrandr --listmonitors | grep "HDMI") ]]; then 
				xrandr --output HDMI-1 --left-of eDP-1
				i3-msg workspace 2 && i3-msg move workspace to output HDMI-1 
				i3-msg workspace 1 && i3-msg move workspace to output HDMI-1
			fi 
	esac
done

feh --bg-fill $HOME/Downloads/kakshi.jpg
