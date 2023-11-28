# LA_Overlay - Lost Ark Overlay

<p align="center">
  <img src="https://i.imgur.com/J1KqXGR.gif" alt="Your Image Description">
</p>

## Description
**LA_Overlay** is a standalone overlay designed specifically for *Lost Ark*. It operates independently of the game, ensuring no interaction with the game's memory or packet analysis, making it completely safe.

## Features
- ``Class Support:`` Currently only supports the Bard class with plans to expand to other classes.
- ``Skill Cooldowns:`` Tracks and displays skill cooldowns.
- ``Buff Uptime:`` Tracks and displays skill's buff uptime. Buffs are represented by a green bar below the skill's icon, which decreases over time.
- ``Audio and Visual Alerts:`` Provides an audio alert and flashes the buff skill icon in red 3 seconds before the expiration of Bard's Heavenly Tune and Sonic Vibration buffs to help prevent overlapping of buffs and ensure efficient rotation.
- ``Gauge Tracker:`` Shows class gauge bars. You might need to adjust it for your screen size. Right now, it only works for the Bard class at 3440x1440p flawlessly.
- ``Key Blocking:`` Currently commented out, but can be enabled to prevent the use of Heavenly Tune or Sonic Vibration while the buff is still up. (Not recommended for use in raids but good for practice.)

## Future Plans 
(*When I have time and if not lazy*)
- ``Expanded Notifications:`` Include boss phases/mechanics change notifications with the exact phase/mech name based on the boss's HP bars, and notification for counters to allow players to position themselves and prepare to counter the boss.

## Motivation
The development of LA Overlay stemmed from the need for a more customizable and resolution scalable UI. It focuses on providing a minimal interface to easily monitor important buffs in the fast paced and visually busy environment of Legion Raids.

## Future Hope
The hope is that Smile Gate developers will stop being lazy and eventually either allow UI addons or implement more modern and customizable UI options.

------------------

## Installation

1. Install Python.
2. In the Command Prompt, type `pip install pygame pywin32 keyboard opencv-python`.
3. Open the `SETTINGS.py` in your sub class directory in a code editor like Sublime Text or Notepad++ and add your gems and swiftness stat. Also, edit the positioning of the overlay based on your resolution( `WINDOW_POS_X` and `WINDOW_POS_Y`, Default settings are for 3440x1440p).
4. Run the program by typing `py main.py` in the Command Prompt in the main directory.

## Guide to Editing
Soon...

```diff
+ Please consider sharing any useful modifications you make to this and any assistance is welcome.
```
