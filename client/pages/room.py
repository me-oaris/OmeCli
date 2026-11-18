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

    headerStyle = "bold bright_green" if isCyber else "bold white"
    youStyle = "bright_green" if isCyber else "bright_cyan"
    youBorder = "bright_green" if isCyber else "bright_blue"
    strangerStyle = "green" if isCyber else "bright_green"
    strangerBorder = "green" if isCyber else "bright_white"
    chatBorder = "bright_green" if isCyber else "bright_white"

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
    