# AGENTS.md — GlanceAway

## Project Overview

**Glance Away** is a simple macOS desktop application that reminds the user to take breaks after a configurable amount of work time.

The application should be intentionally small, simple, and easy to understand.

The primary goal is to build a working desktop timer, not a feature-rich productivity application.

## Technology

Use:

- **Python 3**
- **Tkinter** for the graphical user interface
- Python standard library whenever possible

Do **not** introduce:

- Web frameworks
- JavaScript
- React
- Electron
- Tauri
- PyQt/PySide
- Databases
- Cloud services
- External APIs
- Unnecessary third-party packages

The application should run locally on macOS.

## Core Features

The application must provide:

1. A simple graphical interface.
2. A field for setting **work time** in minutes.
3. A field for setting **break time** in minutes.
4. A countdown timer showing the remaining time.
5. A clear indication of the current state:
   - `WORKING`
   - `BREAK`

6. A **Start** button.
7. A **Pause** button.
8. A **Reset** button.
9. Automatic transition:
   - Work → Break
   - Break → Work
   - Continue repeating while running.

10. A notification or other clear indication when the timer changes from work to break or break to work.

## Initial UI

Keep the interface minimal.

A reasonable layout is:

```text
             GlanceAway

             WORKING

              24:37

      Work: 25 min
      Break: 5 min

       [ Start ] [ Pause ] [ Reset ]
```

The exact visual design can be improved later, but functionality comes first.

## Timer Behavior

### Start

When the user presses **Start**:

- Start the countdown.
- If the timer has never started, use the configured work duration.
- If the timer was paused, continue from the current remaining time.

### Pause

When the user presses **Pause**:

- Stop the countdown.
- Preserve the remaining time.
- Pressing Start should continue from where it stopped.

### Reset

When the user presses **Reset**:

- Stop the timer.
- Reset the application to the beginning of a work period.
- Reload the current work duration from the input field.
- Display the full work duration.

### Phase Changes

When the countdown reaches zero:

1. Change the current phase.
2. Load the appropriate duration.
3. Start the new countdown automatically.
4. Notify the user.

Example:

```text
WORKING → BREAK
BREAK → WORKING
```

## Timer Accuracy

Do not implement the timer by simply assuming that this code will execute exactly once per second:

```python
time_left -= 1
```

GUI event loops are not perfectly precise.

Instead, calculate the remaining time based on the actual elapsed time.

For example, track:

- the time when the current countdown started
- the duration of the current phase
- the current time

Then calculate the remaining time from those values.

The displayed countdown can update approximately once per second.

Accuracy is more important than perfectly synchronized GUI updates.

## Input Validation

Keep validation simple.

The application should:

- Accept positive whole numbers for work and break duration.
- Reject empty values.
- Reject zero or negative values.
- Reject non-numeric values.
- Prevent the application from crashing because of invalid input.

Display a simple error message when necessary.

Do not build an elaborate settings or validation system.

## Code Structure

Start with a very small project:

```text
time_out/
├── app.py
├── README.md
└── AGENTS.md
```

Do not split the application into many modules unless there is a clear reason to do so.

For the first version, keeping most of the application in `app.py` is acceptable.

If the application becomes difficult to understand because `app.py` becomes too large, suggest a refactoring before making the project more complex.

## Code Quality

Prioritize:

1. Correct behavior
2. Simplicity
3. Readability
4. Maintainability

Use clear function and variable names.

Prefer straightforward Python over clever abstractions.

Avoid:

- unnecessary classes
- unnecessary design patterns
- excessive abstraction
- premature optimization
- large dependencies
- complicated state-management systems

Comments should explain **why** something is done when the reason is not obvious.

Do not add comments that merely repeat what the code says.

## Development Approach

Build the application incrementally.

### Phase 1 — Basic UI

Create:

- application window
- title
- work/break settings
- countdown display
- Start/Pause/Reset buttons
- current phase indicator

Do not implement notifications yet.

### Phase 2 — Countdown

Implement:

- countdown
- Start
- Pause
- Reset

Verify that these work before adding automatic phase changes.

### Phase 3 — Work/Break Cycle

Implement:

```text
WORK → BREAK → WORK → BREAK → ...
```

Verify that phase transitions work correctly.

### Phase 4 — Notifications

Add a simple macOS-friendly notification or other clear visual/audio indication when a phase changes.

Keep this implementation simple.

### Phase 5 — Polish

Only after the core functionality works, consider small improvements such as:

- better typography
- window sizing
- keyboard shortcuts
- sound
- menu bar support
- saved settings
- launch-at-login
- packaging as a `.app`

Do not implement these automatically.

Ask before adding significant new functionality.

## Vibe Coding Rules

This project is also intended as a learning project.

When making changes:

1. Explain what you are changing.
2. Prefer small, understandable changes.
3. Show the relevant code or explain the important parts.
4. Avoid making large changes when a small change will work.
5. Do not introduce new technologies without explaining why.
6. Preserve working functionality when adding features.

If there are multiple reasonable approaches, recommend the simplest one first.

## Testing

After making changes, test the application.

At minimum verify:

### UI

- Application opens successfully.
- All controls are visible.
- Work and break durations can be changed.

### Timer

- Start works.
- Pause works.
- Start after Pause resumes correctly.
- Reset works.
- Countdown reaches zero.
- Work changes to Break.
- Break changes to Work.
- The cycle continues.

### Validation

Test:

- empty input
- zero
- negative number
- decimal number
- text
- normal positive integer

The application should not crash.

## Important Testing Rule

Do not require the user to wait 25 minutes to test the application.

During development, use short durations such as:

```text
Work: 1 minute
Break: 1 minute
```

or, when appropriate, temporarily use seconds for testing.

Do not permanently change the application's user-facing behavior just to make testing faster.

## Error Handling

Handle expected user errors gracefully.

The application should never crash because the user entered an invalid duration.

Do not add broad exception handling such as:

```python
try:
    ...
except Exception:
    pass
```

unless there is a specific reason.

Do not silently hide errors.

## Dependencies

Keep dependencies to a minimum.

Before adding an external package, ask:

> Can this be done reasonably well using Python's standard library?

If yes, use the standard library.

## Git

Make small, logical commits.

Example:

```text
Initial Tkinter UI
Add countdown timer
Add pause and reset
Add work-break cycle
Add notifications
Polish timer interface
```

Do not combine unrelated changes into one commit.

## Future Features

Potential future features include:

- configurable number of work/break cycles
- long break after several work periods
- custom notification sounds
- menu bar mode
- statistics
- daily break tracking
- saved preferences
- launch at login
- packaging as a macOS `.app`

These are **not part of the initial version**.

Do not implement them unless explicitly requested.

## Definition of Done

The first version is complete when:

- The application runs on macOS.
- The user can set work minutes.
- The user can set break minutes.
- Start works.
- Pause works.
- Reset works.
- The countdown is displayed.
- Work automatically changes to Break.
- Break automatically changes to Work.
- The user receives a clear indication when a break starts.
- Invalid input does not crash the application.
- The code remains simple enough for a beginner to understand.

## Guiding Principle

> **Build the smallest application that solves the problem well.**

Do not turn GlanceAway into a productivity platform.

Simple, reliable, understandable code is more important than having many features.
