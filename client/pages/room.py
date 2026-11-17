from rich.console import Console, Group
from rich.text import Text
from rich.align import Align
from rich.panel import Panel
from rich.columns import Columns
from rich import box

from io import StringIO
from prompt_toolkit.formatted_text import ANSI

def render_room(messages):

    headerLeft = Text()
    headerLeft.append("OMECLI", style="bold white")
    headerRight = Text()
    headerRight.append("Anonymous Talk", style="dim white")

    header = Columns(
        [headerLeft,headerRight],
        expand=True
    )

    you = Panel(
        Align.center(
            Text("You", style="dim white"),
            vertical = "middle"
        ),
        title="You",
        border_style="bright_blue",
        box=box.SQUARE,
        height=12
    )

    stranger = Panel(
        Align.center(
            Text("Stranger. ..", style="dim white"),
            vertical = "middle"
        ),
        title="Stranger",
        border_style="bright_green",
        box=box.SQUARE,
        height=12
    )

    video_containers = Columns(
        [you, stranger],
        equal=True,
        expand=True,
        padding=1
    )

    chat_text = Text()

    if messages:
        for message in messages[-6:]:
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
        height=12,
        padding=(1,2)
    )

    output = StringIO()

    rich_console = Console(
        file=output,
        force_terminal=True,
        color_system="truecolor",
        width=60
    )

    rich_console.print(header)
    rich_console.print()
    rich_console.print(video_containers)
    rich_console.print(chat_history)

    return ANSI(output.getvalue())
    