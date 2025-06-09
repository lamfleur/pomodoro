# Pomodoro Timer

This script provides an automated Pomodoro timer with a simple GUI.
Use the **Start** button to begin the cycle. The timer loops through the following sequence:

1. Work for 25 minutes
2. Take a 5 minute break
3. Repeat steps 1 and 2 four times
4. After the fourth work session, take a 20 minute long break
5. The cycle repeats indefinitely

The window shows the current state (work or break), a countdown timer, a progress bar, and the current set number.
**Start** begins the timer, and **Reset** stops it and returns to the waiting state.

At every phase change (work start, break start, long break start, and end), a notification is issued and a sound is played.
If `sound/start.wav`, `sound/start.mp3`, `sound/end.wav`, or `sound/end.mp3` exist, they will be played automatically using the `playsound` library.
If none of these files are found, a simple system beep is used as a fallback.

**Note:**

* **Sound files are not provided in this repository.**
  Please obtain appropriate sound effect files (WAV or MP3, e.g. from free sound effect sites), and place them in the `sound/` directory as `start.wav`/`start.mp3` and `end.wav`/`end.mp3`.
* If you use git, ensure that the `sound/` directory is included in `.gitignore` to avoid accidentally publishing sound files.

## Setup

1. Install Python 3.x
2. Install required libraries:

   ```bash
   pip install plyer playsound
   ```
3. Place `pomodoro.py` in any folder you like.
4. Place your chosen sound files (`start.wav`/`start.mp3`, `end.wav`/`end.mp3`) into a `sound/` subfolder in the same directory as `pomodoro.py`.
5. To start automatically when Windows boots, create a shortcut to
   `pomodoro.py` (or to `pythonw.exe pomodoro.py`) and place it in the
   Windows `Startup` folder (`shell:startup`).
6. For quick testing, you can launch the script with the `--test` option which
   shortens all timings (work: 20s, break: 5s, long break: 15s).

The program runs entirely locally and does not require an internet connection.
