from textual.widgets import Static, Label, ProgressBar
from textual.containers import Vertical, Center
from textual.app import ComposeResult
from textual.reactive import reactive
from textual.message import Message
import time
from enum import Enum
from .models import config

class TimerState(Enum):
    POMODORO = ("Pomodoro", "🍅", "pomodoro")
    SHORT_BREAK = ("Short Break", "☕", "short-break")
    LONG_BREAK = ("Long Break", "🌴", "long-break")

class TimerFinished(Message):
    """Emitted when a timer finishes"""
    def __init__(self, state: TimerState):
        self.state = state
        super().__init__()

class TimerWidget(Vertical):
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
        # Initial updates
        self.watch_time_remaining(self.time_remaining)
        
    def compose(self) -> ComposeResult:
        yield Label(id="clock-label")
        with Center():
            yield ProgressBar(total=100, show_eta=False, show_percentage=False, id="progress-bar")

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
        self._update_display(time_remaining, self.is_running)

    def watch_is_running(self, is_running: bool) -> None:
        """Called when is_running changes to update UI."""
        self._update_display(self.time_remaining, is_running)
        
    def _update_display(self, time_remaining: float, is_running: bool) -> None:
        minutes, seconds = divmod(int(time_remaining), 60)
        state_name, state_emoji, state_class = self.current_state.value
        status = "⏱️ Running" if is_running else "⏸️ Paused"
        
        progress_percent = 0.0
        total_time = config.pomodoro_min * 60.0
        if self.current_state == TimerState.SHORT_BREAK:
            total_time = config.short_break_min * 60.0
        elif self.current_state == TimerState.LONG_BREAK:
            total_time = config.long_break_min * 60.0
            
        if total_time > 0:
            progress_percent = ((total_time - time_remaining) / total_time) * 100

        try:
            clock = self.query_one("#clock-label", Label)
            clock.update(f"[bold]{state_emoji} {state_name}[/bold] - {status}\n\n[bold text-title]{minutes:02d}:{seconds:02d}[/bold text-title]  ({int(progress_percent)}%)")
            
            # Remove all possible state classes and add the current one
            clock.remove_class("pomodoro", "short-break", "long-break")
            clock.add_class(state_class)
        except Exception:
            pass
            
        try:
            pb = self.query_one("#progress-bar", ProgressBar)
            pb.update(progress=progress_percent)
        except Exception:
            pass

    def toggle_pause(self) -> None:
        if self.is_running:
            self.pause_timer()
        else:
            self.start_timer()
            
    def start_timer(self) -> None:
        if not self.is_running:
            self.is_running = True
            self._last_tick = time.monotonic()
            self.update_timer.resume()
            
    def pause_timer(self) -> None:
        if self.is_running:
            self.is_running = False
            self.update_timer.pause()
            
    def stop_timer(self) -> None:
        self.pause_timer()
        if self.current_state == TimerState.POMODORO:
            self.time_remaining = config.pomodoro_min * 60.0
        elif self.current_state == TimerState.SHORT_BREAK:
            self.time_remaining = config.short_break_min * 60.0
        elif self.current_state == TimerState.LONG_BREAK:
            self.time_remaining = config.long_break_min * 60.0
            
    def skip_timer(self) -> None:
        self.time_remaining = 0
        self.handle_timer_finish()
            
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
