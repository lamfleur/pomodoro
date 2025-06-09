Pomodoro Timer
==============

This script provides an automated Pomodoro timer. It starts immediately and
loops through the following cycle without manual start/stop controls:

1. Work for 25 minutes
2. Take a 5 minute break
3. Repeat the above four times
4. After the fourth work session, take a 20 minute long break
5. The cycle repeats indefinitely

A small window displays only a **Reset** button. Pressing it resets the cycle
and starts again from the first work session.

Notifications and a simple sound alert are issued at every phase (work start,
break start, long break start). Windows users hear a system beep.

Setup
-----
1. Install Python 3.x
2. Install required libraries:
   ```bash
   pip install plyer
   ```
3. Place `pomodoro.py` anywhere you like.
4. To start automatically when Windows boots, create a shortcut to
   `pomodoro.py` (or to `pythonw.exe pomodoro.py`) and place it in the
   `Startup` folder.

The program runs entirely locally and does not require an internet connection.
