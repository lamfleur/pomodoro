import threading
import time
import platform
try:
    from plyer import notification
except ImportError:
    notification = None
import tkinter as tk

# Cross-platform sound notification
if platform.system() == 'Windows':
    import winsound
    def play_sound():
        winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
else:
    def play_sound():
        print('\a')

WORK_MINUTES = 25
SHORT_BREAK_MINUTES = 5
LONG_BREAK_MINUTES = 20
SETS_BEFORE_LONG_BREAK = 4

reset_flag = False


def notify(title: str, message: str):
    if notification:
        notification.notify(title=title, message=message, timeout=10)
    play_sound()


def wait_with_reset(seconds: int) -> bool:
    """Wait for the specified seconds. Return True if reset was triggered."""
    global reset_flag
    for _ in range(seconds):
        time.sleep(1)
        if reset_flag:
            reset_flag = False
            return True
    return False


def pomodoro_loop():
    set_count = 1
    while True:
        notify('Pomodoro', f'Start working! Set {set_count}/{SETS_BEFORE_LONG_BREAK}')
        if wait_with_reset(WORK_MINUTES * 60):
            set_count = 1
            continue

        if set_count == SETS_BEFORE_LONG_BREAK:
            notify('Pomodoro', 'Long break! 20 minutes')
            if wait_with_reset(LONG_BREAK_MINUTES * 60):
                set_count = 1
                continue
            set_count = 1
        else:
            notify('Pomodoro', 'Short break! 5 minutes')
            if wait_with_reset(SHORT_BREAK_MINUTES * 60):
                set_count = 1
                continue
            set_count += 1


def on_reset():
    global reset_flag
    reset_flag = True
    notify('Pomodoro', 'Cycle reset')


def start_thread():
    thread = threading.Thread(target=pomodoro_loop, daemon=True)
    thread.start()


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Pomodoro Timer')
    reset_button = tk.Button(root, text='Reset', command=on_reset)
    reset_button.pack(padx=20, pady=20)
    start_thread()
    root.mainloop()
