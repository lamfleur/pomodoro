import argparse
import platform
import tkinter as tk
from pathlib import Path
from tkinter import ttk
from typing import Optional

try:
    from plyer import notification
except ImportError:
    notification = None

try:
    import simpleaudio as sa
except ImportError:
    sa = None

# クロスプラットフォーム用 フォールバックbeep
if platform.system() == 'Windows':
    import winsound
    def beep() -> None:
        winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
else:
    def beep() -> None:
        print('\a')

# タイマー設定（秒）
DEFAULT_WORK = 25 * 60
DEFAULT_SHORT_BREAK = 5 * 60
DEFAULT_LONG_BREAK = 20 * 60

TEST_WORK = 20
TEST_SHORT_BREAK = 5
TEST_LONG_BREAK = 15

SETS_BEFORE_LONG_BREAK = 4

# サウンドファイル
SOUND_DIR = Path(__file__).parent / 'sound'
SOUND_EXTS = ['.wav']
START_BASENAME = 'start'
END_BASENAME = 'end'

def _find_sound_file(basename: str) -> Optional[Path]:
    for ext in SOUND_EXTS:
        p = SOUND_DIR / f'{basename}{ext}'
        if p.exists():
            return p
    return None

def _play_file(path: Path) -> None:
    if sa and path.exists() and path.suffix.lower() == ".wav":
        try:
            wave_obj = sa.WaveObject.from_wave_file(str(path))
            wave_obj.play()
            return
        except Exception as e:
            print(f"[DEBUG] simpleaudio error: {e}")
    beep()

def play_start_sound() -> None:
    p = _find_sound_file(START_BASENAME)
    if p:
        _play_file(p)
    else:
        beep()

def play_end_sound() -> None:
    p = _find_sound_file(END_BASENAME)
    if p:
        _play_file(p)
    else:
        beep()

def notify(title: str, message: str) -> None:
    if notification:
        notification.notify(title=title, message=message, timeout=10)

class PomodoroApp:
    def __init__(self, root: tk.Tk, test_mode: bool = False) -> None:
        self.root = root
        self.work_seconds = TEST_WORK if test_mode else DEFAULT_WORK
        self.short_break_seconds = TEST_SHORT_BREAK if test_mode else DEFAULT_SHORT_BREAK
        self.long_break_seconds = TEST_LONG_BREAK if test_mode else DEFAULT_LONG_BREAK
        self.sets_before_long = SETS_BEFORE_LONG_BREAK

        self.state = 'Waiting'
        self.remaining = 0
        self.set_count = 1
        self.timer_id: Optional[str] = None
        self.is_running = False

        self._build_ui()
        self.start()  # 起動と同時に自動スタート

    def _build_ui(self) -> None:
        self.root.title('Pomodoro Timer')
        self.state_label = tk.Label(self.root, text='Waiting', font=('Arial', 14))
        self.time_label = tk.Label(self.root, text='00:00', font=('Arial', 24))
        self.set_label = tk.Label(
            self.root, text=f'Set 0/{self.sets_before_long}', font=('Arial', 12)
        )
        self.progress = ttk.Progressbar(self.root, maximum=1, value=0)
        self.start_button = tk.Button(self.root, text='Start', command=self.start)
        self.reset_button = tk.Button(self.root, text='Reset', command=self.reset)

        self.state_label.pack(padx=10, pady=(10, 0))
        self.time_label.pack(padx=10, pady=(0, 5))
        self.set_label.pack(padx=10, pady=(0, 5))
        self.progress.pack(fill='x', padx=10, pady=5)

        self.start_button.pack(padx=20, pady=10)
        self.reset_button.pack(padx=20, pady=10)

    def start(self) -> None:
        if self.is_running:
            return
        self.is_running = True
        self.set_count = 1
        self._start_work()

    def reset(self) -> None:
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        self.is_running = False
        self.state = 'Waiting'
        self.remaining = 0
        self.set_count = 1
        self._update_labels()
        self.progress.config(maximum=1, value=0)
        play_end_sound()
        notify('Pomodoro', 'Cycle reset')

    def _start_work(self) -> None:
        self.state = 'Work'
        self.remaining = self.work_seconds
        self.progress.config(maximum=self.work_seconds, value=0)
        play_start_sound()  # 作業開始時のみ
        notify(
            'Pomodoro',
            f'Start working! Set {self.set_count}/{self.sets_before_long}',
        )
        self._update_labels()
        self._schedule_tick()

    def _start_short_break(self) -> None:
        self.state = 'Short Break'
        self.remaining = self.short_break_seconds
        self.progress.config(maximum=self.short_break_seconds, value=0)
        # 休憩開始時は音を鳴らさない
        notify('Pomodoro', 'Short break!')
        self._update_labels()
        self._schedule_tick()

    def _start_long_break(self) -> None:
        self.state = 'Long Break'
        self.remaining = self.long_break_seconds
        self.progress.config(maximum=self.long_break_seconds, value=0)
        # 長休憩開始時も音を鳴らさない
        notify('Pomodoro', 'Long break!')
        self._update_labels()
        self._schedule_tick()

    def _schedule_tick(self) -> None:
        self.timer_id = self.root.after(1000, self._tick)

    def _tick(self) -> None:
        if not self.is_running:
            return
        self.remaining -= 1
        self.progress['value'] = self.progress['maximum'] - self.remaining
        self._update_labels()
        if self.remaining <= 0:
            self._advance_phase()
        else:
            self._schedule_tick()

    def _advance_phase(self) -> None:
        if self.state == 'Work':
            play_end_sound()  # 作業終了時のみ
            if self.set_count == self.sets_before_long:
                self._start_long_break()
            else:
                self._start_short_break()
        elif self.state == 'Short Break':
            self.set_count += 1
            self._start_work()
        elif self.state == 'Long Break':
            self.set_count = 1
            self._start_work()

    def _update_labels(self) -> None:
        minutes, seconds = divmod(self.remaining, 60)
        time_text = f'{minutes:02}:{seconds:02}' if self.is_running else '00:00'
        self.state_label.config(text=self.state)
        self.time_label.config(text=time_text)
        set_display = 0 if not self.is_running else self.set_count
        self.set_label.config(text=f'Set {set_display}/{self.sets_before_long}')

def main() -> None:
    parser = argparse.ArgumentParser(description='Pomodoro timer')
    parser.add_argument('--test', action='store_true', help='enable short test mode')
    args = parser.parse_args()

    root = tk.Tk()
    app = PomodoroApp(root, test_mode=args.test)
    root.mainloop()

if __name__ == '__main__':
    main()
