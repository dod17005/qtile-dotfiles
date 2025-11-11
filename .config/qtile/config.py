# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar, layout, qtile, hook, extension
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from qtile_extras import widget
from qtile_extras.widget.decorations import RectDecoration, BorderDecoration
from qtile_extras.popup import PopupMenu, PopupMenuItem, PopupMenuSeparator

import os
import subprocess

mod = "mod4"
terminal = guess_terminal()

# Colorschemes
gruvbox_dark = ["#282828","#928374","#1d2021","",        # bg, gray, bg0_h
                "#cc241d","#fb4934","#282828","#32302f", # red, red, bg0, bg0_s
                "#98971a","#b8bb26","#3c3836","#a89984", # green, green, bg1, fg4
                "#d79921","#fabd2f","#504945","#bdae93", # yellow, yellow, bg2, fg3
                "#458588","#83a598","#665c54","#d5c4a1", # blue, blue, bg3, fg2
                "#b16286","#d3869b","#7c6f64","#ebdbb2", # purple, purple, bg4, fg1
                "#689d6a","#8ec07c","#928374","#fbf1c7", # aqua, aqua, gray, fg0
                "#a89984","#ebdbb2","#d65d0e","#fe8019"] # gray, fg, orange, orange

colors = gruvbox_dark

# Power menu
@lazy.function
def show_text_power_menu(qtile):
    items = [
        PopupMenuItem(text="Power", enabled=False),
        PopupMenuSeparator(),
        PopupMenuItem(
            text="Lock",
            mouse_callbacks={
                "Button1": lazy.spawn("light-locker-command -l")
            },
            highlight=colors[16],
            highlight_method="text",
        ),
        PopupMenuItem(
            text="Log out",
            mouse_callbacks={
                "Button1": lazy.shutdown()
            },
            highlight=colors[16],
            highlight_method="text",
        ),
        PopupMenuItem(
            text="Restart",
            mouse_callbacks={
                "Button1": lazy.spawn("systemctl reboot")
            },
            highlight=colors[16],
            highlight_method="text",
        ),
        PopupMenuItem(
            text="Shutdown",
            mouse_callbacks={
                "Button1": lazy.spawn("systemctl shutdown")
            },
            highlight_method="text",
            highlight=colors[5]
        )
    ]
    menu = PopupMenu.generate(qtile, 
                              menuitems=items, 
                              background=colors[0],
                              )
    
    menu.show(centered=True)

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    #Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +10%"), desc="Raise volume by 10%"),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -10%"), desc="Lower volume by 10%"),
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle"), desc="Mute volume"),
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +5%"), desc="Increase brightness by 5%"),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 5%-"), desc="Decrease brightness by 5%"),
    Key([mod, "shift"], "q", show_text_power_menu),
    Key([], "Print", lazy.spawn("xfce4-screenshooter")),

]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}",
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc=f"Switch to & move focused window to group {i.name}",
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )


groups.append(
        ScratchPad("scratchpad", [
            DropDown("files", 
                     "/usr/bin/thunar", 
                     height=0.5, 
                     y=0.2,
                     opacity=1)]))

keys.append(Key([mod],"z", lazy.group["scratchpad"].dropdown_toggle('files')))


layout_style = dict(
    border_focus=colors[16],
    border_normal=colors[0],
    border_width=3,
    margin=4,
)

layouts = [
    layout.RatioTile(**layout_style),
    layout.Columns(**layout_style),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    layout.Tile(**layout_style),
    layout.Floating(**layout_style),
    #layout.TreeTab(
    #    bg_color=colors[7],
    #),
    # layout.VerticalTile(),
    layout.Zoomy(),
]

widget_defaults = dict(
    font="MesloLGS NF",
    fontsize=16,
    foreground="#ebdbb2"
)
extension_defaults = widget_defaults.copy()

decoration_group = {
    "decorations": [
        RectDecoration(colour=colors[16], 
                       radius=12, 
                       filled=True,
                       )
    ],
    "padding": 10
}

decoration_group_2 = {
    "decorations": [
        BorderDecoration(colour=colors[16],
                         border_width=[0,0,3,0],
                         )
        ]

}

spacer_length = 5

def remove_app_name(text):
    return ""


screens = [
    Screen(
        
        wallpaper="/home/atdodge/Pictures/Wallpapers/pxfuel.jpg",
        wallpaper_mode="fill",
                top=bar.Bar(
            [
                widget.CurrentLayout(**decoration_group_2),
                #widget.QuickExit(**decoration_group_2),
                #widget.Sep(**sep_args),
                widget.Spacer(length=spacer_length),
                widget.GroupBox(highlight_method='line', 
                                this_current_screen_border=colors[16],
                                highlight_color = [colors[6],colors[0]],
                                ),
                widget.Spacer(length=spacer_length),
                widget.Prompt(),
                widget.Spacer(length=spacer_length),
                widget.Spacer(length=bar.STRETCH),
                widget.Pomodoro(),
                #widget.WindowName(**decoration_group_2),
                widget.Spacer(length=bar.STRETCH),
                widget.Systray(),
                widget.Spacer(length=spacer_length),
                widget.PulseVolume(mute_format="󰜺", fmt=" {}", **decoration_group_2),
                widget.Spacer(length=spacer_length),
                widget.Battery(
                    format="{char} {percent:2.0%}",
                    charge_char="󱐋",
                    discharge_char="",
                    empty_char="",
                    full_char="󰁹",
                    **decoration_group_2),
                widget.Spacer(length=spacer_length),
                widget.Clock(format="%Y-%m-%d %a %I:%M %p", **decoration_group_2),
            ],
            24,
            background=colors[7],
            #border_width=2,
            #border_color="#928374",
            margin=4
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

# Startup script
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call(home)

keys.append(Key([mod], "r", lazy.run_extension(extension.J4DmenuDesktop(
    background=colors[0],
    #dmenu_height=10,
    dmenu_lines=10,
    dmenu_ignorecase=True,
    fontsize=12,
    font="MesloLGS NF",
))))
