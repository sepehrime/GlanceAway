# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

**Read `docs/AGENTS.md` first.** It is the authoritative spec for this project: required features, allowed technology (Python 3 + Tkinter + standard library only), code-style rules, the phased development approach, the manual testing checklist, and the rule to ask before adding significant new functionality. This is a learning project, so explain changes and keep them small. `docs/plan.md` tracks which phases are done. `docs/` is git-ignored and exists only on the owner's machine, so it may be missing in other checkouts.

## Commands

```sh
python3 GlanceAway.py   # run the app (or .venv/bin/python GlanceAway.py)
./build_mac.sh          # build release/GlanceAway.app and release/GlanceAway.dmg with PyInstaller
```

- `build_mac.sh` prefers `.venv/bin/python` if it exists, otherwise `python3`. PyInstaller must be installed in that interpreter. The app is built for the architecture of the Mac that runs the script.
- `build/`, `dist/`, `release/` and `GlanceAway.spec` are generated and git-ignored. The build script passes all options on the command line, so edit `build_mac.sh` instead of the spec file.
- There is no test suite or linter. Test by hand against the checklist in `docs/AGENTS.md`, using 1-minute durations. Don't change user-facing units to make testing faster.

## Architecture

Everything lives in `GlanceAway.py`, inside a single `main()` function. Timer state (`current_phase`, `remaining_seconds`, `is_running`, `started_at`, `remaining_at_start`, `update_id`, `timer_started`, `last_belled_second`) is held in local variables. The nested handlers change it through `nonlocal`, and there are no classes. When you add state, declare it `nonlocal` in every handler that assigns to it.

How the timer works:
- Remaining time comes from elapsed time: `remaining_at_start - (time.monotonic() - started_at)`. It never decrements a counter. `update_countdown` reschedules itself with `root.after(200, ...)` and keeps its handle in `update_id` so that Pause and Reset can cancel it.
- Pause saves the remaining time into `remaining_seconds`. Start then resets `started_at` and `remaining_at_start` from that value.
- At zero, `update_countdown` stops the timer and calls `notify_phase_change`. That function opens its own alert window (a `Toplevel` with `-topmost`) so the alert shows above other apps even when the sound is muted. It takes a grab and blocks on `wait_window` until the user clicks OK. Only then does `load_next_phase` swap the phase and read the new duration, and the countdown restarts with a fresh `started_at`. Because of this, the next phase starts its full duration only after the alert is dismissed. This is intended behavior.
- If the next phase's duration field is invalid at that moment, `load_next_phase` returns `False` and the timer stays stopped at 00:00. The `remaining_seconds == 0` branch in `start_timer` handles pressing Start from that state.
- The system bell rings once on each of the last three displayed seconds. `last_belled_second` stops it from ringing more than once per second.

Validation is in `read_duration`. It accepts whole numbers from 1 to `MAX_MINUTES` (999) written with ASCII digits, and shows a `messagebox.showerror` for anything else. The length check runs before `int()` because Python refuses to convert digit strings longer than 4300 characters.

The UI uses the default light ttk look. The owner tried a dark theme and rejected it.

The `version` string at the top of `GlanceAway.py` is shown in the window footer. Update it when you make a release.
