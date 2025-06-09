Pomodoro Timer
==============

This script provides an automated Pomodoro timer. Use the **Start** button to
begin the cycle. The timer loops through the following sequence:

1. Work for 25 minutes
2. Take a 5 minute break
3. Repeat the above four times
4. After the fourth work session, take a 20 minute long break
5. The cycle repeats indefinitely

The window shows the current state (work or break), a countdown, progress bar
and the current set number. **Start** begins the timer and **Reset** stops it
and returns to the waiting state.

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
5. For quick testing you can launch the script with the `--test` option which
   shortens all timings (work 20s, break 5s, long break 15s).

The program runs entirely locally and does not require an internet connection.
