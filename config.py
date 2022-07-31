import os
import re
import socket
import subprocess
from typing import List  # noqa: F401
from libqtile import bar, hook, layout, widget, qtile
from libqtile.config import Click, Drag, Group, Key, KeyChord, Match, Screen, ScratchPad, DropDown
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"
terminal = "kitty"
browser = "firefox"
filemanager = "thunar"

groups = [Group("1", layout='monadtall'),
          Group("2", layout='max'),
          Group("3", layout='monadtall'),
          Group("4", layout='monadtall'),
          Group("5", layout='monadtall'),
          Group("6", layout='monadtall'),
          Group("7", layout='monadtall'),
          Group("8", layout='monadtall'),
          Group("9", layout='monadtall'),
          ScratchPad("scratchpad", [
              DropDown("term", "kitty", x=0.20, width=0.60, height=0.50, opacity=1.0, on_focus_lost_hide=False)]),
]

keys = [
    KeyChord([mod], "p", [
             Key([], "i",
                 lazy.spawn("networkmanager_dmenu"),
                 desc="Networkmanager Dmenu"
                 ),
         ]),

    # Switch between windows
    Key([mod], "h",
        lazy.layout.left(),
        desc="Move focus to left"
        ),
    Key([mod], "l",
        lazy.layout.right(),
        desc="Move focus to right"
        ),
    Key([mod], "j",
        lazy.layout.down(),
        desc="Move focus down"
        ),
    Key([mod], "k",
        lazy.layout.up(),
        desc="Move focus up"
        ),
    Key([mod], "space",
        lazy.layout.next(),
        desc="Move window focus to other window"
        ),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h",
        lazy.layout.shuffle_left(),
        desc="Move window to the left"
        ),
    Key([mod, "shift"], "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right"
        ),
    Key([mod, "shift"], "j",
        lazy.layout.shuffle_down(),
        desc="Move window down"
        ),
    Key([mod, "shift"], "k",
        lazy.layout.shuffle_up(),
        desc="Move window up"
        ),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "j",
        lazy.layout.shrink(),
        desc="Shrink focused window"
        ),
    Key([mod, "control"], "k",
        lazy.layout.grow(),
        desc="Grow focused window"
        ),
    Key([mod, "shift"], "n",
        lazy.layout.reset(),
        desc="Reset all window sizes"
        ),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    #Key([mod, "shift"], "space",
    #    lazy.layout.toggle_split(),
    #    desc="Toggle between split and unsplit sides of stack"
    #    ),

    # Toggle between different layouts as defined below
    Key([mod], "Tab",
        lazy.next_layout(),
        desc="Toggle between layouts"
        ),
    Key([mod], "c",
        lazy.window.kill(),
        desc="Kill focused window"
        ),

    Key([mod, "shift"], "r",
        lazy.restart(),
        desc="Restart Qtile"
        ),
    Key([mod, "shift"], "q",
        lazy.shutdown(),
        desc="Shutdown Qtile"
        ),

    # My own keybindings
    Key([mod], "Return",
        lazy.spawn(terminal),
        desc="Launch kitty terminal"
        ),
    Key([mod], "x",
        lazy.spawn("sh /home/kelvin/.scripts/powermenu.sh"),
        #lazy.spawn("archlinux-logout"),
        desc="Exit menu"
        ),
    Key([mod], "i",
        lazy.spawn("networkmanager_dmenu"),
        desc="networkmanager_dmenu"
        ),
    Key([mod], "d",
        lazy.spawn("rofi -modi drun -show drun -config /home/kelvin/.config/rofi/rofi_menu.rasi"),
        #lazy.spawn("rofi -modi drun -show drun -config /home/kelvin/.config/rofi/rofi_bar.rasi"),
        desc="Rofi app menu"
        ),
    Key([mod], "t",
        lazy.spawn("rofi -show window -config /home/kelvin/.config/rofi/rofi_menu.rasi"),
        desc="Rofi window menu"
        ),
    Key([mod], "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen"
        ),
    Key([mod, "shift"], "space",
        lazy.window.toggle_floating(),
        desc="Toggle floating"
        ),
    Key([mod], "w",
        lazy.spawn(browser),
        desc="Open firefox"
        ),
    Key([mod], "e",
        lazy.spawn("emacsclient -c -a emacs"),
        desc="Open Doom Emacs"
        ),
    Key([mod, "shift"], "Return",
        lazy.spawn(filemanager),
        desc="Open Thunar file manager"
        ),
    Key([mod], "Print",
        lazy.spawn("scrot '%Y-%m-%d-%s_screenshot_$wx$h.jpg' -e 'mv $f $$(xdg-user-dir PICTURES)' --select mode=edge --freeze"),
        desc="Screenshot an area using scrot"
        ),
    Key([mod, "shift"], "Print",
        lazy.spawn("scrot '%Y-%m-%d-%s_screenshot_$wx$h.jpg' -e 'mv $f $$(xdg-user-dir PICTURES)'"),
        desc="Screenshot screen using scrot"
        ),
    Key([mod], "o",
        lazy.spawn("sh /home/kelvin/.scripts/rofi-beats.sh"),
        desc="Rofi beats script"
        ),
    Key([], "F12",
        lazy.group['scratchpad'].dropdown_toggle('term'),
        desc="Dropdown xfce4-terminal"
        ),
    Key([mod], "b",
        lazy.hide_show_bar("all"),
        desc="Hide/show Qtile bar"
        ),

    # Volume control
    #Key([mod], "p",
    #    lazy.spawn("sh /home/kelvin/.scripts/rofi-audio-switch.sh"),
    #    desc="Audio output switch"
    #    ),
    Key([], "XF86AudioRaiseVolume",
        lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%"),
        desc="Raise volume by 5%"
        ),
    Key([], "XF86AudioLowerVolume",
        lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%"),
        desc="Lower volume by 5%"
        ),
    Key(["shift"], "XF86AudioRaiseVolume",
        lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +1%"),
        desc="Raise volume by 1%"
        ),
    Key(["shift"], "XF86AudioLowerVolume",
        lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -1%"),
        desc="Lower volume by 1%"
        ),
    Key([], "XF86AudioMute",
        lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle"),
        desc="Mute volume"
        ),

]

colors = [["#1E1E2E", "#1E1E2E"], #0 panel background
          ["#302D41", "#302D41"], #1 selection
          ["#D9E0EE", "#D9E0EE"], #2 foreground
          ["#6E6C7E", "#6E6C7E"], #3 comment
          ["#89DCEB", "#89DCEB"], #4 cyan
          ["#ABE9B3", "#ABE9B3"], #5 green
          ["#F8BD96", "#F8BD96"], #6 orange
          ["#F5C2E7", "#F5C2E7"], #7 pink
          ["#DDB6F2", "#DDB6F2"], #8 purple
          ["#F28FAD", "#F28FAD"], #9 red
          ["#FAE3B0", "#FAE3B0"]] #10 yellow

# Allow MODKEY+[0 through 9] to bind to groups, see https://docs.qtile.org/en/stable/manual/config/groups.html
# MOD4 + index Number : Switch to Group[index]
# MOD4 + shift + index Number : Send active window to another Group
from libqtile.dgroups import simple_key_binder
dgroups_key_binder = simple_key_binder(mod)

'''
groups = [Group(i) for i in "123456789"]
for i in groups:
    keys.extend([
        Key([mod],
            i.name,
            lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),
        Key([mod], "Right", lazy.screen.next_group(),
            desc="Switch to next group"),
        Key([mod], "Left", lazy.screen.prev_group(),
            desc="Switch to previous group"),
        Key([mod, "shift"],
            i.name,
            lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
    ])
'''

layout_theme = {"border_width": 2,
                "margin": 8,
                "border_focus": colors[5],
                "border_normal": colors[0]
                }

layouts = [
    layout.MonadTall(
        **layout_theme,
        #name = '﬿',
        single_border_width = 0,
        ),
    layout.Max(
        **layout_theme,
        #name = '',
        ),
    #layout.MonadWide(**layout_theme),
    #layout.Bsp(**layout_theme),
    #layout.Columns(**layout_theme),
    #layout.RatioTile(**layout_theme),
    #layout.Tile(shift_windows=True, **layout_theme),
    #layout.VerticalTile(**layout_theme),
    #layout.Matrix(**layout_theme),
    #layout.Floating(**layout_theme),
    #layout.TreeTab(**layout_theme),
    #layout.Zoomy(**layout_theme),
]

prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

##### DEFAULT WIDGET SETTINGS #####
widget_defaults = dict(
    font="Noto Sans Nerd Font Bold",
    fontsize = 14,
    padding = 2,
    background = colors[0]
)
extension_defaults = widget_defaults.copy()

def parse_browser(text):
    for string in [" — Chromium", " — Mozilla Firefox", " — LibreWolf"]:
        text = text.replace(string, "")
    return text

def init_widgets_list():
    widgets_list = [
                widget.CurrentLayoutIcon(
                        foreground = colors[5],
                        scale = 0.7,
                        padding = 2,
                        #custom_icon_paths = ['/home/kelvin/.config/qtile/CurrentLayoutIcon'], # comment line if dark theme
                        ),
                # widget.CurrentLayout(
                #         foreground = colors[5],
                #         scale = 0.6,
                #         padding = 2
                #         ),
                widget.Sep(
                        linewidth = 0,
                        #padding = 6,
                        padding = 3,
                        foreground = colors[2],
                        background = colors[0]
                        ),
                widget.GroupBox(
                        fontsize = 10,
                        margin_y = 4,
                        margin_x = 0,
                        padding_y = 5,
                        padding_x = 5,
                        borderwidth = 3,
                        active = colors[5],
                        inactive = colors[3],
                        rounded = False,
                        disable_drag = True,
                        highlight_color = colors[1],
                        highlight_method = "line",
                        this_current_screen_border = colors[5],
                        this_screen_border = colors [4],
                        other_current_screen_border = colors[6],
                        other_screen_border = colors[4],
                        foreground = colors[2],
                        background = colors[0]
                        ),
                widget.Prompt(
                        prompt = prompt,
                        padding = 10,
                        foreground = colors[9],
                        background = colors[1]
                        ),
                widget.Sep(
                        linewidth = 0,
                        padding = 10,
                        foreground = colors[2],
                        background = colors[0]
                        ),
                widget.TaskList(
                        markup = True,
                        markup_floating = '<span color=#ABE9B3">{}</span>',
                        markup_focused = '<span color="#ABE9B3">{}</span>',
                        markup_maximized = '<span color="#ABE9B3">{}</span>',
                        markup_minimized = '<span color="#D9E0EE">{}</span>',
                        markup_normal = '<span color="#D9E0EE">{}</span>',
                        urgent_border = colors[9],
                        foreground = colors[2],
                        background = colors[0],
                        border = colors[0],
                        border_width = 0,
                        fontsize = 13,
                        padding = 0,
                        spacing = 10,
                        title_width_method = 'uniform',
                        max_title_width = 200,
                        parse_text = parse_browser,
                        highlight_method = 'block',
                        icon_size = 0
                        ),
                widget.TextBox(
                        text = "  ",
                        foreground = colors[8],
                        background = colors[0],
                        fontsize = 14,
                        mouse_callbacks = {
                            'Button1': lambda: qtile.cmd_spawn('pactl set-sink-mute @DEFAULT_SINK@ toggle'),
                            'Button3': lambda: qtile.cmd_spawn('sh /home/kelvin/.scripts/audio-output-switch.sh &'),
                            'Button4': lambda: qtile.cmd_spawn('pactl set-sink-volume @DEFAULT_SINK@ +5%'),
                            'Button5': lambda: qtile.cmd_spawn('pactl set-sink-volume @DEFAULT_SINK@ -5%'),
                            }
                        ),
                widget.Volume(
                        foreground = colors[8],
                        background = colors[0],
                        padding = 5,
                        volume_down_command = "pactl set-sink-volume @DEFAULT_SINK@ -5% &",
                        volume_up_command = "pactl set-sink-volume @DEFAULT_SINK@ +5% &",
                        mouse_callbacks = {'Button3': lambda: qtile.cmd_spawn('sh /home/kelvin/.scripts/audio-output-switch.sh &')}
                        ),
                #volume,
                widget.TextBox(
                        text = "  ",
                        foreground = colors[10],
                        background = colors[0],
                        fontsize = 14,
                        mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' btop')},
                        ),
                widget.Memory(
                        foreground = colors[10],
                        background = colors[0],
                        format = '{MemPercent}%',
                        padding = 5,
                        mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' btop')},
                        ),
                widget.TextBox(
                        text = " ﬙ ",
                        foreground = colors[5],
                        background = colors[0],
                        mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' btop')}
                        ),
                widget.CPU(
                        foreground = colors[5],
                        background = colors[0],
                        format = '{load_percent}%',
                        padding = 5,
                        mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' btop')}
                        ),
                widget.TextBox(
                        text = " ",
                        foreground = colors[9],
                        background = colors[0],
                        fontsize = 14,
                        ),
                widget.ThermalSensor(
                        tag_sensor = "Core 0",
                        foreground = colors[9],
                        background = colors[0],
                        threshold = 90,
                        padding = 5,
                        update_interval = 15,
                        ),
                widget.TextBox(
                        text = "  ",
                        foreground = colors[6],
                        ),
                widget.DF(
                        foreground = colors[6],
                        partition = '/home',
                        visible_on_warn = False,
                        format = '{uf}{m}',
                        padding = 5,
                        ),
                widget.TextBox(
                        text = " ",
                        foreground = colors[4],
                        background = colors[0],
                        fontsize = 14,
                        padding = 5,
                        mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn('networkmanager_dmenu &')}
                        ),
                widget.Net(
                        interface = "wlan0",
                        format = '{down} ↓↑ {up}',
                        #format = '{down}',
                        foreground = colors[4],
                        background = colors[0],
                        padding = 5,
                        mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn('networkmanager_dmenu &')}
                        ),
                widget.TextBox(
                        text = '',
                        foreground = colors[7],
                        fontsize = 14,
                        padding = 5,
                        mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn('sh /home/kelvin/.scripts/calendar-popup.sh curr &'),
                                           'Button4': lambda: qtile.cmd_spawn('sh /home/kelvin/.scripts/calendar-popup.sh prev &'),
                                           'Button5': lambda: qtile.cmd_spawn('sh /home/kelvin/.scripts/calendar-popup.sh next &')}
                        ),
                widget.Clock(
                        foreground = colors[7],
                        background = colors[0],
                        format = "%d/%m/%y %a %H:%M ",
                        update_interval = 1.0,
                        padding = 5,
                        mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn('sh /home/kelvin/.scripts/calendar-popup.sh curr &'),
                                           'Button4': lambda: qtile.cmd_spawn('sh /home/kelvin/.scripts/calendar-popup.sh prev &'),
                                           'Button5': lambda: qtile.cmd_spawn('sh /home/kelvin/.scripts/calendar-popup.sh next &')}
                        ),
                #widget.TextBox(
                #        text = ' ',
                #        foreground = colors[3],
                #        mouse_callbacks={'Button1': lambda: qtile.cmd_spawn('sh /home/kelvin/.scripts/powermenu &')}
                #        ),
            ]
    return widgets_list

def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    #del widgets_screen1[7:8]               # Slicing removes unwanted widgets (systray) on Monitors 1,3
    return widgets_screen1

# def init_widgets_screen2():
#     widgets_screen2 = init_widgets_list()
#     return widgets_screen2                 # Monitor 2 will display all widgets in widgets_list

def init_screens():
    return [#Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=1.0, size=20)),
            #Screen(top=bar.Bar(widgets=init_widgets_screen2(), opacity=1.0, size=20)),
            Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=1.0, size=20))]

if __name__ in ["config", "__main__"]:
    screens = init_screens()
    widgets_list = init_widgets_list()
    widgets_screen1 = init_widgets_screen1()
    #widgets_screen2 = init_widgets_screen2()

def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)

# def window_to_previous_screen(qtile):
#     i = qtile.screens.index(qtile.current_screen)
#     if i != 0:
#         group = qtile.screens[i - 1].group.name
#         qtile.current_window.togroup(group)

# def window_to_next_screen(qtile):
#     i = qtile.screens.index(qtile.current_screen)
#     if i + 1 != len(qtile.screens):
#         group = qtile.screens[i + 1].group.name
#         qtile.current_window.togroup(group)

# def switch_screens(qtile):
#     i = qtile.screens.index(qtile.current_screen)
#     group = qtile.screens[i - 1].group
#     qtile.current_screen.set_group(group)

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
    ]

dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    # default_float_rules include: utility, notification, toolbar, splash, dialog,
    # file_progress, confirm, download and error.
    *layout.Floating.default_float_rules,
    Match(title='Confirmation'),      # tastyworks exit box
    Match(title='Qalculate!'),        # qalculate-gtk
    Match(wm_class='kdenlive'),       # kdenlive
    Match(wm_class='pinentry-gtk-2'), # GPG key password entry
    Match(wm_class='Galculator'),     # Galculator
    Match(wm_class='Gpick'),          # Gpick
    ],
    **layout_theme)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
