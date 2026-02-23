# PomoTUI
![Main Interface](assets/pomotui.png)

A feature-rich Pomodoro Terminal User Interface (TUI) built with Python and the [Textual](https://textual.textualize.io/) framework. Keep track of your focus sessions, rest automatically, and jot down tasks to preserve your workflow.

![Settings Panel](assets/options.png)

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

This project uses `uv` for modern, fast Python dependency management. To set it up:

```bash
git clone https://github.com/Str4vinci/PomoTUI.git
cd PomoTUI
uv sync
```

## Usage

You can run the application directly via the terminal by setting up a global command:

```bash
mkdir -p ~/.local/bin
ln -s $(pwd)/run.sh ~/.local/bin/pomotui
```

Then simply type:

```bash
pomotui
```

### Keybindings

- `space`: Pause or Resume the timer.
- `n`: Skip the current timer and move to the next phase.
- `m`: Toggle Minimal layout.
- `s`: Open the Settings modal.
- `t`: Cycle through color themes (Nord, Catppuccin, Dracula).
- `q`: Quit the application.
- `ctrl+p`: Open Textual's built-in command palette.

### Slash Commands
You can also control the timer directly from the Task Queue by typing these commands and pressing `<Enter>`:
- `/start`
- `/pause`
- `/stop`
- `/skip`

## Configuration

Settings are accessible inside the app (press `s`) and are applied instantly to the current session. You can manage durations, auto-transitions, session logging toggle, and the **Notification Volume**. The task queue explicitly runs in-memory and resets automatically when the application is restarted.

## Safety and Portability 🛡️

**Is this safe to download and use?**
Yes. PomoTUI is 100% safe to use on any machine. It acts as an offline, standalone application:
- It makes **no network requests** and collects zero telemetry or tracking data.
- It leverages isolated virtual environments via `uv`, so it does not interfere with system-wide Python libraries.
- The task queue uses pure machine memory (RAM) and securely discards task records when it closes.

**Will this work on other Linux distros and computers?**
Absolutely. Because it uses Python + `uv` to manage its own sandbox, it is highly portable across *any* Linux distribution (Ubuntu, Arch, Fedora, etc.). 
For audio alerts and desktop notifications, the app executes the universal standard Linux tools under the hood:
- `paplay`: Standard playback on any system using `pulseaudio` or `pipewire-pulse` (which covers 99% of modern distros).
- `notify-send`: The `libnotify` standard for shooting toast popups to your desktop.

**Does it work on all terminals?**
Yes! PomoTUI is built utilizing the powerful `Textual` rendering engine, meaning it works flawlessly out-of-the-box on virtually any modern terminal emulator (like GNOME Terminal, Kitty, Alacritty, Konsole, Terminator, and standard TTYs). If your terminal supports colors and standard ANSI codes, this will run smoothly!

If you ever want to run this on a different computer, you can safely `git clone` this repository onto it, run `uv sync`, and execute it the exact same way.
