from rich.console import Console, Group
from rich.text import Text
from rich.align import Align
from rich.panel import Panel
from rich import box
import shutil

from io import StringIO
from prompt_toolkit.formatted_text import ANSI

def render_about(appSettings=None):
    if appSettings is None:
        appSettings = {"theme" : "Dark Mode"}

    isCyber = appSettings.get("theme") == "Cyber Green"
    isAmber = appSettings.get("theme") == "Amber Retro"
    isSynthwave = appSettings.get("theme") == "Synthwave"
    isDracula = appSettings.get("theme") == "Dracula"

    if isCyber:
        titleStyle="bold bright_green"
        borderColor="bright_green"
        featureColor = "bright_green"
    elif isAmber:
        titleStyle="bold bright_yellow"
        borderColor="bright_yellow"
        featureColor = "bright_yellow"
    elif isSynthwave:
        titleStyle="bold bright_magenta"
        borderColor = "magenta"
        featureColor = "bright_magenta"
    elif isDracula:
        titleStyle = "bold #BD93F9"
        borderColor = "#8BE9FD"
        featureColor = "#BD93F9"
    else:
        titleStyle="bold cyan"
        borderColor="bright_blue"
        featureColor="bright_green"

    title_text = Text("About OmeCli", style=titleStyle)

    body_text = Text()
    body_text.append("OmeCli is a terminal based anonymous talk room, inspired by Omegle\nPurely built in Python.\n", style="bold white")
    body_text.append("Key Features:\n", style=f"bold {featureColor}")
    body_text.append("> Fast, lightweight and fully keyboard controllled\n",style="dim white")
    body_text.append("> ASCII video engine and chat support\n", style="dim white")
    body_text.append("> Responsive layout\n", style="dim white")
    body_text.append("Press [ESC] to return to the main menu",style="bright yellow")

    content = Group(
        Align.center(title_text),
        Align.center(body_text)
    )

    about_panel = Panel(
        content,
        title="OmeCli v0.0.1",
        title_align="left",
        border_style=borderColor,
        box=box.SQUARE_DOUBLE_HEAD,
        padding=(2,4),
        expand=True
    )

    output = StringIO()

    terminalWidth = shutil.get_terminal_size().columns
    consoleWidth = max(40, terminalWidth - 2)

    rich_console = Console(
        file=output,
        force_terminal=True,
        color_system="truecolor",
        width=consoleWidth
    )

    rich_console.print(about_panel)

    return ANSI((output.getvalue()))