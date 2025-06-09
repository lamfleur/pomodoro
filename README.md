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

A notification is issued at the start and end of each work phase.
A sound is played **only at the beginning and end of each work session**:

* At the **start of work**: `sound/start.wav`
* At the **end of work**: `sound/end.wav`

Break and long break phases **do not play any sound**.

If `sound/start.wav` or `sound/end.wav` exist, they are played using the `simpleaudio` library.
If not, a simple system beep is used as a fallback.

**Note:**

* **Sound files are not provided in this repository.**
  Please obtain appropriate sound effect files (WAV format, e.g. from free sound effect sites), and place them in the `sound/` directory as `start.wav` and `end.wav`.
* Only standard PCM WAV files are supported (16bit/44.1kHz recommended).
* If you use git, ensure that the `sound/` directory is included in `.gitignore` to avoid accidentally publishing sound files.

## Setup

1. Install Python 3.x

2. Install required libraries:

   ```bash
   pip install plyer simpleaudio
   ```

3. Place `pomodoro.py` in any folder you like.

4. Place your chosen sound files (`start.wav`, `end.wav`) into a `sound/` subfolder in the same directory as `pomodoro.py`.

5. To start automatically when Windows boots, create a shortcut to
   `pomodoro.py` (or to `pythonw.exe pomodoro.py`) and place it in the
   Windows `Startup` folder (`shell:startup`).

6. For quick testing, you can launch the script with the `--test` option which
   shortens all timings (work: 20s, break: 5s, long break: 15s).

The program runs entirely locally and does not require an internet connection.
