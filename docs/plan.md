# GlanceAway plan

## Problem and approach

Build a small Tkinter-based macOS desktop timer that follows the phases described in AGENTS.md: minimal UI, accurate countdown logic, work/break transitions, simple validation, and optional notifications only after the core loop works. Keep the implementation small and readable, with most logic in a single app file unless the code becomes unmanageable.

## Phase checklist

- [x] Phase 1: Basic UI
  - [x] Create the main window and title.
  - [x] Add work and break duration inputs.
  - [x] Show the current phase label and countdown display.
  - [x] Add Start, Pause, and Reset buttons.
  - [x] Keep the layout minimal and readable.

- [x] Phase 2: Countdown behavior
  - [x] Implement accurate time tracking using elapsed time rather than decrementing by one second per tick.
  - [x] Start should begin a fresh work timer when first run or resume from paused remaining time.
  - [x] Pause should stop the countdown without losing remaining time.
  - [x] Reset should stop the timer and restore the full work duration from the inputs.
  - [x] Verify manual timing logic before adding phase switching.

- [x] Phase 3: Work/break cycle
  - [x] Automatically switch WORKING -> BREAK when the countdown reaches zero.
  - [x] Automatically switch BREAK -> WORKING and continue repeating.
  - [x] Reload the correct duration for each phase and resume automatically.
  - [x] Ensure the user sees a clear phase indicator during transitions.

- [x] Phase 4: Validation and error handling
  - [x] Accept positive integer minutes only.
  - [x] Reject empty, zero, negative, decimal, and non-numeric input.
  - [x] Prevent crashes with a simple visible error message.
  - [x] Keep validation deliberately small and explicit.

- [x] Phase 5: Notifications
  - [x] Show a message box when a phase changes, with a message for the upcoming phase.
  - [x] Pause at 00:00 and wait for the user to dismiss the message before switching phases.
  - [x] Start the next phase's full countdown only after the message is dismissed.
  - [x] Sound the system bell on each of the final three displayed countdown seconds.

- [x] Phase 6: Polish and verification
  - [x] Check the UI is visible and usable.
  - [x] Verify start/pause/resume/reset behavior.
  - [x] Verify input validation edge cases.
  - [x] Ensure the app remains simple, readable, and beginner-friendly.

## Notes and decisions

- Prioritize correctness and simplicity over extra features.
- Use Python standard library features only; avoid unnecessary dependencies.
- Keep the project small and focused on the timer itself rather than a productivity platform.
- Do not implement long-break, saved settings, or app packaging unless requested later.
- Use short test durations during development instead of waiting for full 25-minute work cycles.
