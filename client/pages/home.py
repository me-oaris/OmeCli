from rich.console import Console, Group
from rich.text import Text
from rich.align import Align
from rich.panel import Panel
from rich.style import Style
from rich import box

from io import StringIO
from prompt_toolkit.formatted_text import ANSI
from prompt_toolkit.key_binding import KeyBindings

def render_home(selected):
    # Welcome Banner Part ;-;
    welcomeText = Text()
    versionText = Text()

    welcomeText.append("Welcome to OmeCli\n", style="bold white")
    welcomeText.append("""
  ▄▄▄▄▄   ▄▄▄      ▄▄▄  ▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄ ▄▄▄      ▄▄▄▄▄ 
▄███████▄ ████▄  ▄████ ███▀▀▀▀▀ ███▀▀▀▀▀ ███       ███  
███   ███ ███▀████▀███ ███▄▄    ███      ███       ███  
███▄▄▄███ ███  ▀▀  ███ ███      ███      ███       ███  
 ▀█████▀  ███      ███ ▀███████ ▀███████ ████████ ▄███▄ """,style="bold cyan")
    versionText.append("Version 0.0.1", style="dim italic white")

    groupedWelcome = Group(
        Align.left(welcomeText),
        Align.right(versionText)
    )

    welcomePanel = Panel(groupedWelcome, box=box.SQUARE_DOUBLE_HEAD) 

    # Buttons

    buttons_panels =[
        Panel(
        Align.center(Text("1. Find a Stranger", style="bold white")),
        border_style="bright_green",
        box=box.SQUARE_DOUBLE_HEAD,
        padding=(0,4),
        style =Style(bgcolor="#123D2A" if selected == 0 else "#0D1117")
    ),
        Panel(
        Align.center(Text("2. About OmeCli", style="bold white")),
        border_style="bright_blue",
        box=box.SQUARE_DOUBLE_HEAD,
        padding=(0,4),
        style=Style(bgcolor="#172D4d" if selected == 1 else "#0D1117")
    ),
        Panel(
            Align.center(Text("3. Settings", style="bold white")),
            border_style="bright_white",
            box=box.SQUARE_DOUBLE_HEAD,
            padding=(0,4),
            style=Style(bgcolor="#303030" if selected == 2 else "#0D1117")
        ),
        Panel(
            Align.center(Text("4. Quit OmeCli", style="bold white")),
            border_style="bright_red",
            box=box.SQUARE_DOUBLE_HEAD,
            padding=(0,4),
            style=Style(bgcolor="#4A1717" if selected == 3 else "#0D1117")
        )
    ] 

    output = StringIO()

    rich_console = Console(
        file=output,
        force_terminal=True,
        color_system="truecolor",
        width=60
    )

    rich_console.print(welcomePanel)

    for button in buttons_panels:
        rich_console.print(button)

    return ANSI(output.getvalue())