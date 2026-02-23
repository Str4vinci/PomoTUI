# Pomodoro TUI

A feature-rich Pomodoro Terminal User Interface (TUI) built with Python and the [Textual](https://textual.textualize.io/) framework.

## Features

- **Split Dashboard**: View your timer and your session's task queue side-by-side.
- **Task Queue**: Jot down ideas or distractions on the fly during a Pomodoro, and check them off when completed.
- **Customizable Timers**: Adjust Pomodoro, Short Break, and Long Break durations to your liking.
- **Auto-Transitions**: Configure the app to automatically start breaks or pomodoros.
- **Layout Toggles**: Switch to a minimal view showing only the timer for maximum focus.
- **Color Themes**: Built-in support for Nord, Catppuccin Mocha, and Dracula themes.
- **System Notifications**: Uses native Linux `notify-send` and FreeDesktop sounds `paplay` when a timer completes.
- **Session Logging**: Optionally log completed Pomodoros to a file `~/.config/pomodoro_tui/session.log`.

## Installation

This project uses `uv` for dependency management. To set it up manually:

```bash
git clone <repository_url>
cd pomodoro_tui
uv venv
uv pip install textual textual-dev pydantic
```

## Usage

You can run the application directly via the terminal by simply typing:

```bash
pomotui
```

*(This runs a symlinked wrapper script that handles the local virtual environment and executes the Textual app.)*

### Keybindings

- `space`: Pause or Resume the timer.
- `m`: Toggle Minimal layout.
- `s`: Open the Settings modal.
- `t`: Cycle through color themes (Nord, Catppuccin, Dracula).
- `q`: Quit the application.
- `ctrl+p`: Open Textual's built-in command palette.

## Configuration

Settings are accessible inside the app (press `s`) and are applied instantly to the current session. The task queue explicitly runs in-memory and resets automatically when the application is restarted.
