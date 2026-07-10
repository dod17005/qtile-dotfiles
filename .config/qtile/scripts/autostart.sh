#!/bin/bash

picom --daemon --config $HOME/.config/qtile/scripts/picom.conf & 
/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &
#/usr/bin/wired &
dunst &
eval $(gnome-keyring-daemon --start) 
nm-applet &
autorandr --change &
