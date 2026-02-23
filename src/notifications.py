import asyncio

async def play_sound() -> None:
    try:
        process = await asyncio.create_subprocess_exec(
            "paplay", "/usr/share/sounds/freedesktop/stereo/complete.oga",
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
