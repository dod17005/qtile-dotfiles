#!/bin/sh
nm-applet &
picom &
xrandr --auto &
xfce4-clipman &
blueman-applet &
light-locker --lock-on-lid --lock-after-screensaver=10 &
