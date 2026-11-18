from rich.console import Console, Group
from rich.text import Text
from rich.align import Align
from rich.panel import Panel
from rich.columns import Columns
from rich.table import Table
from rich import box

from io import StringIO
from prompt_toolkit.formatted_text import ANSI

import shutil

def render_room(messages, yourFrame="Starting Camera..", strangerFrame="Waiting for stranger...", appSettings=None):
    if appSettings is None:
        appSettings = {"theme":"Dark Mode", "anon_display": True}

    isCyber = appSettings.get("theme") == "Cyber Green"
    isAmber = appSettings.get("theme") == "Amber Retro"
    isSynthwave = appSettings.get("theme") == "Synthwave"
    isDracula = appSettings.get("theme") == "Dracula"

    if isCyber:
        headerStyle = "bold bright_green"
        youStyle = "bright_green"
        youBorder = "bright_green"
        strangerStyle = "green"
        strangerBorder = "green"
        chatBorder = "bright_green"
    elif isAmber:
        headerStyle = "bold bright_yellow"
        youStyle = "bright_yellow"
        youBorder = "bright_yellow"
        strangerStyle = "yellow"
        strangerBorder = "yellow"
        chatBorder = "bright_yellow"
    elif isSynthwave:
        headerStyle = "bold bright_magenta"
        youStyle = "bright_magenta"
        youBorder = "magenta"
        strangerStyle = "pink1"
        strangerBorder = "bright_magenta"
        chatBorder = "magenta"
    elif isDracula:
        headerStyle = "bold #BD93F9"
        youStyle = "#8BE9FD"
        youBorder = "#BD93F9"
        strangerStyle = "#50FA7B"
        strangerBorder = "#8BE9FD"
        chatBorder = "#BD93F9"
    else:
        headerStyle = "bold white"
        youStyle = "bright_cyan"
        youBorder = "bright_blue"
        strangerStyle = "bright_green"
        strangerBorder = "bright_green"
        chatBorder = "bright_white"

    headerLeft = Text()
    headerLeft.append("OMECLI", style=headerStyle)
    headerRight = Text()
    headerRight.append("Anonymous Talk" if appSettings.get("anon_display") else "Public Talk", style="dim white")
    
    header = Columns(
        [headerLeft,headerRight],
        expand=True
    )

    youContent = Text(yourFrame, style=youStyle)

    you = Panel(
        Align.center(
            youContent,
            vertical = "middle"
        ),
        title="You",
        border_style=youBorder,
        box=box.SQUARE,
        height=16,
        expand=True
    )

    strangerContent = Text(strangerFrame, style=strangerStyle)
    stranger = Panel(
        Align.center(
            strangerContent,
            vertical = "middle"
        ),
        title="Stranger",
        border_style=strangerBorder,
        box=box.SQUARE,
        height=16,
        expand=True
    )

    terminalWidth = shutil.get_terminal_size().columns
    consoleWidth = max(40, terminalWidth - 2)
    leftWidth = consoleWidth // 2
    rightWidth = consoleWidth - leftWidth

    video_table = Table.grid(expand=True)
    video_table.add_column(width=leftWidth)
    video_table.add_column(width=rightWidth)
    video_table.add_row(you, stranger)

    chat_text = Text()

    if messages:
        maxMessages = 3
        for message in messages[-maxMessages:]:
            if message.startswith("You:"):
                msgStyle = "bold bright_green" if isCyber else "bright_blue"
            elif message.startswith("Stranger:"):
                msgStyle = "green" if isCyber else "bright_green"
            else:
                msgStyle = "dim bright_green" if isCyber else "dim yellow"
            chat_text.append(f"{message}\n", style=msgStyle)
    else:
        chat_text.append(
            "Your conversation will appear here...",
            style="dim white"
        )

    chat_history = Panel(
        chat_text,
        title="Conversation",
        title_align="left",
        border_style=chatBorder,
        box=box.SQUARE,
        height=7,
        padding=(1,2),
        expand=True
    )

    output = StringIO()

    rich_console = Console(
        file=output,
        force_terminal=True,
        color_system="truecolor",
        width=consoleWidth
    )

    rich_console.print(header)
    rich_console.print()
    rich_console.print(video_table)
    rich_console.print(chat_history)

    return ANSI(output.getvalue())
    