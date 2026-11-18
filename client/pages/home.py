from rich.console import Console, Group
from rich.text import Text
from rich.align import Align
from rich.panel import Panel
from rich.style import Style
from rich import box

from io import StringIO
from prompt_toolkit.formatted_text import ANSI

import shutil

def render_home(selected, appSettings=None):
    if appSettings is None:
        appSettings = {"theme":"Dark Mode"}
    isCyber = appSettings.get("theme") ==  "Cyber Green"

    bannerColor = "bright_green" if isCyber else "bright_cyan"
    selectedBg = "#047230" if isCyber else "#123D2A"
    selectedFg = "#000000" if isCyber else "#FFFFFF"
    # Welcome Banner Part ;-;
    welcomeText = Text()
    versionText = Text()

    welcomeText.append("Welcome to OmeCli\n", style="bold white")
    welcomeText.append("""
  ▄▄▄▄▄   ▄▄▄      ▄▄▄  ▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄ ▄▄▄      ▄▄▄▄▄ 
▄███████▄ ████▄  ▄████ ███▀▀▀▀▀ ███▀▀▀▀▀ ███       ███  
███   ███ ███▀████▀███ ███▄▄    ███      ███       ███  
███▄▄▄███ ███  ▀▀  ███ ███      ███      ███       ███  
 ▀█████▀  ███      ███ ▀███████ ▀███████ ████████ ▄███▄ """,style=bannerColor)
    versionText.append("Version 0.0.1", style="dim italic white")

    groupedWelcome = Group(
        Align.left(welcomeText),
        Align.right(versionText)
    )

    welcomePanel = Panel(groupedWelcome, box=box.SQUARE_DOUBLE_HEAD, expand=True) 

    # Buttons

    buttons_panels =[
        Panel(
        Align.center(Text("1. Find a Stranger", style="bold white")),
        border_style="bright_green",
        box=box.SQUARE_DOUBLE_HEAD,
        padding=(0,4),
        style =Style(bgcolor=selectedBg if selected == 0 else "#0D1117", color=selectedFg if selected == 0 else "white"),
        expand=True
    ),
        Panel(
        Align.center(Text("2. About OmeCli", style="bold white")),
        border_style="bright_blue",
        box=box.SQUARE_DOUBLE_HEAD,
        padding=(0,4),
        style=Style(bgcolor=selectedBg if selected == 1 else "#0D1117", color=selectedFg if selected == 1 else "white"),
        expand=True
    ),
        Panel(
            Align.center(Text("3. Settings", style="bold white")),
            border_style="bright_white",
            box=box.SQUARE_DOUBLE_HEAD,
            padding=(0,4),
            style=Style(bgcolor=selectedBg if selected == 2 else "#0D1117", color=selectedFg if selected == 2 else "white"),
            expand=True
        ),
        Panel(
            Align.center(Text("4. Quit OmeCli", style="bold white")),
            border_style="bright_red",
            box=box.SQUARE_DOUBLE_HEAD,
            padding=(0,4),
            style=Style(bgcolor=selectedBg if selected == 3 else "#0D1117", color=selectedFg if selected == 3 else "white"),
            expand=True
        )
    ] 

    output = StringIO()

    terminalWidth = shutil.get_terminal_size().columns
    consoleWidth = max (40, terminalWidth - 2)
    rich_console = Console(
        file=output,
        force_terminal=True,
        color_system="truecolor",
        width=consoleWidth
    )

    rich_console.print(welcomePanel)
    rich_console.print()
    
    for button in buttons_panels:
        rich_console.print(button)

    return ANSI(output.getvalue())