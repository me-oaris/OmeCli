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

def render_room(messages, yourFrame="Starting Camera.."):

    headerLeft = Text()
    headerLeft.append("OMECLI", style="bold white")
    headerRight = Text()
    headerRight.append("Anonymous Talk", style="dim white")

    header = Columns(
        [headerLeft,headerRight],
        expand=True
    )

    youContent = Text(yourFrame, style="bright_cyan")

    you = Panel(
        Align.center(
            youContent,
            vertical = "middle"
        ),
        title="You",
        border_style="bright_blue",
        box=box.SQUARE,
        height=16,
        expand=True
    )

    stranger = Panel(
        Align.center(
            Text("Stranger...", style="dim white"),
            vertical = "middle"
        ),
        title="Stranger",
        border_style="bright_green",
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
            chat_text.append(f"You: {message}\n", style="bright_blue")
    else:
        chat_text.append(
            "Your conversation will appear here...",
            style="dim white"
        )

    chat_history = Panel(
        chat_text,
        title="Conversation",
        title_align="left",
        border_style="bright_white",
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
    