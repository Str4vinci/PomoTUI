from textual.app import ComposeResult
from textual.widgets import Input, ListView, ListItem, Label, Static
from textual.containers import Vertical, VerticalScroll

class TaskItem(ListItem):
    """A single task item in the queue."""
    def __init__(self, text: str, **kwargs):
        super().__init__(**kwargs)
        self.task_text = text
        self.is_done = False
        
    def compose(self) -> ComposeResult:
        yield Label(f"[ ] {self.task_text}", id="label")
        
    def toggle_done(self) -> None:
        self.is_done = not self.is_done
        label = self.query_one("#label", Label)
        if self.is_done:
            label.update(f"[x] [strike]{self.task_text}[/strike]")
            self.classes = "done"
        else:
            label.update(f"[ ] {self.task_text}")
            self.classes = ""

from textual.message import Message

class SlashCommand(Message):
    """Emitted when the user types a command starting with /"""
    def __init__(self, command: str):
        self.command = command
        super().__init__()

class TaskQueueWidget(Static):
    """A widget for managing session tasks."""
    
    def compose(self) -> ComposeResult:
        with Vertical():
            yield Label("Session Tasks", id="queue-title")
            with VerticalScroll(id="task-list-container"):
                yield ListView(id="task-list")
            yield Input(placeholder="Add a task or type /start, /pause, /stop...", id="task-input")
            
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Add a new task when the user presses Enter, or process slash commands."""
        text = event.value.strip()
        if not text:
            return
            
        if text.startswith("/"):
            self.post_message(SlashCommand(text))
            event.input.value = ""
            return
            
        task_list = self.query_one("#task-list", ListView)
        task_list.append(TaskItem(text))
        event.input.value = ""
            
    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Toggle task completion when selected."""
        item = event.item
        if isinstance(item, TaskItem):
            item.toggle_done()
