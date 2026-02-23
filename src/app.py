from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from textual.binding import Binding
from .timer import TimerWidget
from .models import config

from .tasks import TaskQueueWidget
from textual.containers import Vertical, Container

from textual import on
from .timer import TimerWidget, TimerFinished
from .notifications import play_sound, send_desktop_notification
from .settings import SettingsScreen
from . import themes

class PomodoroApp(App):
    """A Textual app to manage pomodoro sessions."""
    
    CSS_PATH = "app.tcss"
    
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("space", "toggle_timer", "Pause/Resume"),
        Binding("m", "toggle_layout", "Toggle Minimal Mode"),
        Binding("s", "open_settings", "Settings"),
        Binding("t", "toggle_theme", "Toggle Theme"),
    ]

    def __init__(self):
        super().__init__()
        self.minimal_mode = False
        self._current_theme_idx = 0
        self._theme_names = ["nord", "catppuccin", "dracula"]

    def on_mount(self) -> None:
        """Register custom themes and set default."""
        self.register_theme(themes.nord)
        self.register_theme(themes.catppuccin_mocha)
        self.register_theme(themes.dracula)
        self.theme = "nord"

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        with Container(id="left-panel"):
            yield TimerWidget(id="timer")
        with Container(id="right-panel"):
            yield TaskQueueWidget()
        yield Footer()

    @on(TimerFinished)
    async def on_timer_finished(self, event: TimerFinished) -> None:
        state_str = event.state.value
        title = "Timer Finished!"
        msg = f"Your {state_str} session has ended."
        
        self.run_worker(play_sound(), exclusive=False)
        self.run_worker(send_desktop_notification(title, msg), exclusive=False)
        self.notify(msg, title=title)

        if config.session_logs and event.state.name == "POMODORO":
            import os, datetime
            try:
                log_file = os.path.expanduser("~/.config/pomodoro_tui/session.log")
                os.makedirs(os.path.dirname(log_file), exist_ok=True)
                with open(log_file, "a") as f:
                    f.write(f"[{datetime.datetime.now().isoformat()}] Pomodoro completed.\n")
            except Exception as e:
                self.notify(f"Could not log session: {e}", severity="error")

    def action_toggle_timer(self) -> None:
        """Pause or resume the timer."""
        timer_widget = self.query_one("#timer", TimerWidget)
        timer_widget.toggle_pause()
        
    def action_open_settings(self) -> None:
        """Open the settings screen."""
        
        def check_settings(saved: bool) -> None:
            if saved:
                # Update timer values based on new settings
                timer_widget = self.query_one("#timer", TimerWidget)
                timer_widget.time_remaining = config.pomodoro_min * 60.0
                self.notify("Settings saved!")
        
        self.push_screen(SettingsScreen(), check_settings)
        
    def action_toggle_theme(self) -> None:
        """Cycle through available themes."""
        self._current_theme_idx = (self._current_theme_idx + 1) % len(self._theme_names)
        self.theme = self._theme_names[self._current_theme_idx]
        self.notify(f"Theme changed to: {self.theme.capitalize()}")
        
    def action_toggle_layout(self) -> None:
        """Toggle between full dashboard and minimal timer view."""
        self.minimal_mode = not self.minimal_mode
        if self.minimal_mode:
            self.screen.add_class("minimal")
            self.query_one(Header).display = False
            self.query_one(Footer).display = False
        else:
            self.screen.remove_class("minimal")
            self.query_one(Header).display = True
            self.query_one(Footer).display = True
            
if __name__ == "__main__":
    app = PomodoroApp()
    app.run()
