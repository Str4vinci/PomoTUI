from textual.widgets import Static
from textual.app import ComposeResult
from textual.reactive import reactive
from textual.message import Message
import time
from enum import Enum
from .models import config

class TimerState(Enum):
    POMODORO = "Pomodoro"
    SHORT_BREAK = "Short Break"
    LONG_BREAK = "Long Break"

class TimerFinished(Message):
    """Emitted when a timer finishes"""
    def __init__(self, state: TimerState):
        self.state = state
        super().__init__()

class TimerWidget(Static):
    """A widget to display and manage the timer."""

    time_remaining = reactive(config.pomodoro_min * 60.0)
    current_state = reactive(TimerState.POMODORO)
    is_running = reactive(False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._last_tick = 0
        self.pomodoros_completed = 0
        self.update_timer = None

    def on_mount(self) -> None:
        """Called when widget is added to app. Update timer every 0.1s."""
        self.update_timer = self.set_interval(0.1, self.tick)
        self.update_timer.pause() # start paused

    def tick(self) -> None:
        """Update the time remaining."""
        if not self.is_running:
            return
            
        now = time.monotonic()
        elapsed = now - self._last_tick
        self._last_tick = now
        
        new_time = self.time_remaining - elapsed
        if new_time <= 0:
            self.time_remaining = 0
            self.handle_timer_finish()
        else:
            self.time_remaining = new_time

    def watch_time_remaining(self, time_remaining: float) -> None:
        """Called when time_remaining changes."""
        minutes, seconds = divmod(int(time_remaining), 60)
        state_str = self.current_state.value
        status = "⏱️ Running" if self.is_running else "⏸️ Paused"
        
        self.update(f"[{state_str}] - {status}\n\n[bold]{minutes:02d}:{seconds:02d}[/bold]")

    def watch_is_running(self, is_running: bool) -> None:
        """Called when is_running changes to update UI."""
        # This will trigger an update due to time_remaining but we force it here
        minutes, seconds = divmod(int(self.time_remaining), 60)
        state_str = self.current_state.value
        status = "⏱️ Running" if is_running else "⏸️ Paused"
        self.update(f"[{state_str}] - {status}\n\n[bold]{minutes:02d}:{seconds:02d}[/bold]")

    def toggle_pause(self) -> None:
        if self.is_running:
            self.is_running = False
            self.update_timer.pause()
        else:
            self.is_running = True
            self._last_tick = time.monotonic()
            self.update_timer.resume()
            
    def handle_timer_finish(self) -> None:
        self.is_running = False
        self.update_timer.pause()
        self.post_message(TimerFinished(self.current_state))
        
        # Transition logic
        if self.current_state == TimerState.POMODORO:
            self.pomodoros_completed += 1
            if self.pomodoros_completed % config.pomodoros_until_long_break == 0:
                self.current_state = TimerState.LONG_BREAK
                self.time_remaining = config.long_break_min * 60.0
            else:
                self.current_state = TimerState.SHORT_BREAK
                self.time_remaining = config.short_break_min * 60.0
                
            if config.auto_start_breaks:
                self.toggle_pause()
                
        elif self.current_state in (TimerState.SHORT_BREAK, TimerState.LONG_BREAK):
            self.current_state = TimerState.POMODORO
            self.time_remaining = config.pomodoro_min * 60.0
            
            if config.auto_start_pomodoros:
                self.toggle_pause()
