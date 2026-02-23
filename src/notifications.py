import asyncio

from .models import config

async def play_sound() -> None:
    try:
        # volume ranges from 0 to 65536
        vol = int(65536 * (max(0, min(100, config.notification_volume)) / 100))
        process = await asyncio.create_subprocess_exec(
            "paplay", f"--volume={vol}", "/usr/share/sounds/freedesktop/stereo/complete.oga",
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL
        )
        await process.communicate()
    except Exception:
        pass

async def send_desktop_notification(title: str, message: str) -> None:
    try:
        process = await asyncio.create_subprocess_exec(
            "notify-send", "-a", "Pomodoro TUI", title, message,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL
        )
        await process.communicate()
    except Exception:
        pass
