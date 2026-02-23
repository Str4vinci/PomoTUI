from pydantic import BaseModel, Field

class TimerSettings(BaseModel):
    pomodoro_min: int = Field(default=25, description="Pomodoro duration in minutes")
    short_break_min: int = Field(default=5, description="Short break duration in minutes")
    long_break_min: int = Field(default=15, description="Long break duration in minutes")
    pomodoros_until_long_break: int = Field(default=4, description="Number of pomodoros before a long break")
    auto_start_breaks: bool = Field(default=True, description="Automatically start break timers")
    auto_start_pomodoros: bool = Field(default=False, description="Automatically start pomodoro timers after a break")
    session_logs: bool = Field(default=False, description="Log pomodoro completions")

config = TimerSettings()
