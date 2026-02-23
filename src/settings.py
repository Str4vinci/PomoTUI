from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Input, Button, Label
from textual.containers import Vertical, Horizontal
from .models import config

class SettingsScreen(ModalScreen[bool]):
    """Screen to adjust timer settings."""
    
    CSS = """
    SettingsScreen {
        align: center middle;
    }
    
    #settings-dialog {
        padding: 1 2;
        width: 60;
        height: auto;
        border: thick $background 80%;
        background: $surface;
    }
    
    .setting-row {
        height: auto;
        margin-bottom: 1;
    }
    
    .setting-label {
        width: 1fr;
        content-align: left middle;
    }
    
    .setting-input {
        width: 15;
    }
    
    #buttons {
        margin-top: 1;
        align: right middle;
        height: auto;
    }
    """
    
    def compose(self) -> ComposeResult:
        with Vertical(id="settings-dialog"):
            yield Label("[bold]Timer Settings[/bold]", classes="setting-row")
            
            with Horizontal(classes="setting-row"):
                yield Label("Pomodoro (min):", classes="setting-label")
                yield Input(value=str(config.pomodoro_min), id="pom-min", classes="setting-input")
                
            with Horizontal(classes="setting-row"):
                yield Label("Short Break (min):", classes="setting-label")
                yield Input(value=str(config.short_break_min), id="sb-min", classes="setting-input")
                
            with Horizontal(classes="setting-row"):
                yield Label("Long Break (min):", classes="setting-label")
                yield Input(value=str(config.long_break_min), id="lb-min", classes="setting-input")

            with Horizontal(classes="setting-row"):
                yield Label("Volume (0-100):", classes="setting-label")
                yield Input(value=str(config.notification_volume), id="vol-level", classes="setting-input")

            from textual.widgets import Checkbox
            with Horizontal(classes="setting-row"):
                yield Checkbox("Auto-start Breaks", value=config.auto_start_breaks, id="auto-breaks")
            with Horizontal(classes="setting-row"):
                yield Checkbox("Auto-start Pomodoros", value=config.auto_start_pomodoros, id="auto-pom")
            with Horizontal(classes="setting-row"):
                yield Checkbox("Enable Session Logs", value=config.session_logs, id="session-logs")
            with Horizontal(classes="setting-row"):
                yield Checkbox("Progress Bar Fills Up (elapsed)", value=config.progress_bar_fills_up, id="pb-fills-up")

            with Horizontal(id="buttons"):
                yield Button("Cancel", id="cancel", variant="error")
                yield Button("Save", id="save", variant="success")
                
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            try:
                config.pomodoro_min = int(self.query_one("#pom-min", Input).value)
                config.short_break_min = int(self.query_one("#sb-min", Input).value)
                config.long_break_min = int(self.query_one("#lb-min", Input).value)
                
                vol = int(self.query_one("#vol-level", Input).value)
                config.notification_volume = max(0, min(100, vol))
                
                # Checkboxes
                from textual.widgets import Checkbox
                config.auto_start_breaks = self.query_one("#auto-breaks", Checkbox).value
                config.auto_start_pomodoros = self.query_one("#auto-pom", Checkbox).value
                config.session_logs = self.query_one("#session-logs", Checkbox).value
                config.progress_bar_fills_up = self.query_one("#pb-fills-up", Checkbox).value
                
                self.dismiss(True)
            except ValueError:
                # Basic validation failed, ignore for now
                pass
        else:
            self.dismiss(False)
