import math
import time
import tkinter as tk
from tkinter import messagebox, ttk


def main():
    root = tk.Tk()
    root.title("GlanceAway")
    root.geometry("400x360")
    root.minsize(320, 340)

    content = ttk.Frame(root, padding=24)
    content.pack(fill="both", expand=True)
    content.columnconfigure(0, weight=1)

    title = ttk.Label(content, text="GlanceAway", font=("TkDefaultFont", 18, "bold"))
    title.grid(row=0, column=0, pady=(0, 20))

    phase = ttk.Label(content, text="WORKING", font=("TkDefaultFont", 12, "bold"))
    phase.grid(row=1, column=0, pady=(0, 4))

    countdown = ttk.Label(content, text="25:00", font=("TkDefaultFont", 36))
    countdown.grid(row=2, column=0, pady=(0, 20))

    remaining_seconds = 25 * 60
    current_phase = "WORKING"
    timer_started = False
    is_running = False
    started_at = None
    remaining_at_start = remaining_seconds
    update_id = None
    last_belled_second = None

    def show_time(seconds):
        display_seconds = math.ceil(max(0, seconds))
        minutes, seconds = divmod(display_seconds, 60)
        countdown.config(text=f"{minutes:02}:{seconds:02}")

    def notify_phase_change(next_phase):
        message = (
            "Eyes up - your break starts now. Give them a little distance."
            if next_phase == "BREAK"
            else "Break complete - ease back into your next focus session."
        )
        messagebox.showinfo("GlanceAway", message, parent=root)

    def read_duration(entry, name):
        value = entry.get()
        if not value.isascii() or not value.isdecimal():
            messagebox.showerror(
                f"Invalid {name} duration",
                "Enter a positive whole number of minutes.",
                parent=root,
            )
            return None

        try:
            minutes = int(value)
        except ValueError:
            messagebox.showerror(
                f"Invalid {name} duration",
                "Enter a positive whole number of minutes.",
                parent=root,
            )
            return None

        if minutes <= 0:
            messagebox.showerror(
                f"Invalid {name} duration",
                "Enter a positive whole number of minutes.",
                parent=root,
            )
            return None

        return minutes

    def read_durations():
        work_minutes = read_duration(work_duration, "work")
        if work_minutes is None:
            return None

        break_minutes = read_duration(break_duration, "break")
        if break_minutes is None:
            return None

        return work_minutes, break_minutes

    def load_next_phase():
        nonlocal current_phase, last_belled_second
        nonlocal remaining_seconds, remaining_at_start
        next_phase = "BREAK" if current_phase == "WORKING" else "WORKING"
        entry = break_duration if next_phase == "BREAK" else work_duration
        minutes = read_duration(entry, next_phase.lower())
        if minutes is None:
            return False

        current_phase = next_phase
        last_belled_second = None
        phase.config(text=current_phase)
        remaining_seconds = minutes * 60
        remaining_at_start = remaining_seconds
        return True

    def update_countdown():
        nonlocal remaining_seconds, current_phase, is_running, started_at, update_id
        nonlocal last_belled_second, remaining_at_start
        update_id = None

        if not is_running or started_at is None:
            return

        elapsed = time.monotonic() - started_at
        remaining_seconds = remaining_at_start - elapsed
        if remaining_seconds <= 0:
            remaining_seconds = 0
            is_running = False
            started_at = None
            show_time(remaining_seconds)
            next_phase = "BREAK" if current_phase == "WORKING" else "WORKING"
            notify_phase_change(next_phase)
            if not load_next_phase():
                return

            is_running = True
            started_at = time.monotonic()
            update_countdown()
            return

        show_time(remaining_seconds)
        displayed_seconds = math.ceil(remaining_seconds)
        if 0 < displayed_seconds <= 3 and displayed_seconds != last_belled_second:
            root.bell()
            last_belled_second = displayed_seconds

        update_id = root.after(200, update_countdown)

    def start_timer():
        nonlocal remaining_seconds, timer_started, is_running, started_at
        nonlocal remaining_at_start
        if is_running:
            return

        durations = read_durations()
        if durations is None:
            return

        if not timer_started:
            work_minutes, _ = durations
            remaining_seconds = work_minutes * 60
            timer_started = True
        elif remaining_seconds == 0:
            next_phase = "BREAK" if current_phase == "WORKING" else "WORKING"
            notify_phase_change(next_phase)
            if not load_next_phase():
                return

        is_running = True
        started_at = time.monotonic()
        remaining_at_start = remaining_seconds
        update_countdown()

    def pause_timer():
        nonlocal remaining_seconds, is_running, started_at, update_id
        if not is_running or started_at is None:
            return

        remaining_seconds = max(
            0, remaining_at_start - (time.monotonic() - started_at)
        )
        is_running = False
        started_at = None
        if update_id is not None:
            root.after_cancel(update_id)
            update_id = None
        show_time(remaining_seconds)

    def reset_timer():
        nonlocal remaining_seconds, current_phase, timer_started, is_running
        nonlocal last_belled_second, remaining_at_start, started_at, update_id
        is_running = False
        started_at = None
        if update_id is not None:
            root.after_cancel(update_id)
            update_id = None

        minutes = read_duration(work_duration, "work")
        if minutes is None:
            show_time(remaining_seconds)
            return

        current_phase = "WORKING"
        last_belled_second = None
        phase.config(text=current_phase)
        remaining_seconds = minutes * 60
        timer_started = True
        remaining_at_start = remaining_seconds
        show_time(remaining_seconds)

    settings = ttk.Frame(content)
    settings.grid(row=3, column=0, pady=(0, 24))

    ttk.Label(settings, text="Work (min)").grid(row=0, column=0, padx=(0, 8), pady=4)
    work_duration = ttk.Entry(settings, width=7, justify="center")
    work_duration.insert(0, "25")
    work_duration.grid(row=0, column=1, padx=(0, 20), pady=4)

    ttk.Label(settings, text="Break (min)").grid(row=0, column=2, padx=(0, 8), pady=4)
    break_duration = ttk.Entry(settings, width=7, justify="center")
    break_duration.insert(0, "5")
    break_duration.grid(row=0, column=3, pady=4)

    buttons = ttk.Frame(content)
    buttons.grid(row=4, column=0)

    ttk.Button(buttons, text="Start", command=start_timer).grid(
        row=0, column=0, padx=4
    )
    ttk.Button(buttons, text="Pause", command=pause_timer).grid(
        row=0, column=1, padx=4
    )
    ttk.Button(buttons, text="Reset", command=reset_timer).grid(
        row=0, column=2, padx=4
    )

    root.mainloop()


if __name__ == "__main__":
    main()
