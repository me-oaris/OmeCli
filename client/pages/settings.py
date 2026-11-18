from rich.console import Console, Group
from rich.text import Text
from rich.align import Align
from rich.panel import Panel
from rich.style import Style
from rich import box

import shutil

from io import StringIO
from prompt_toolkit.formatted_text import ANSI

def render_settings(selectedSetting, settings):
    isCyber = settings.get("theme") == "Cyber Green"
    isAmber = settings.get("theme") == "Retro Amber"
    isSynthwave = settings.get("theme") == "Synthwave"
    isDracula = settings.get("theme") == "Dracula"

    if isCyber:
        titleStyle = "bold bright_green"
        outerBorder = "bright_green"
        selectedBorder = "bright_green"
        selectedBg = "#00FF66"
        selectedFg = "#000000"
    elif isAmber:
        titleStyle = "bold bright_yellow"
        outerBorder = "bright_yellow"
        selectedBorder = "bright_yellow"
        selectedBg = "#FF8000"
        selectedFg = "#000000"
    elif isSynthwave:
        titleStyle = "bold bright_magenta"
        outerBorder = "magenta"
        selectedBorder = "bright_magenta"
        selectedBg = "#FF007F"
        selectedFg = "#FFFFFF"
    elif isDracula:
        titleStyle = "bold #BD93F9"
        outerBorder = "#8BE9FD"
        selectedBorder = "#BD93F9"
        selectedBg = "#8D93F9"
        selectedFg = "#282A36"
    else:
        titleStyle = "bold yellow"
        outerBorder = "yellow"
        selectedBorder = "bright_yellow"
        selectedBg = "#3A3012"
        selectedFg = "white"

    titleText = Text("OmeCli Settings", style=titleStyle)

    options = [
        f"Theme: {settings['theme']}",
        f"Anonymous Mode: {'Enabled' if settings['anon_display'] else 'Disabled'}",
        f"Save Chat History: {'On' if settings['save_history'] else 'Off'}",
        "Back to Main Menu"
    ]

    settingPanel = []

    for i,opt in enumerate(options):
        is_selected = (selectedSetting == i)
        settingPanel.append(
            Panel(
                Align.center(Text(opt, style=f"bold {selectedFg if is_selected else 'white'}")),
                border_style= selectedBorder if  is_selected  else "dim white",
                box= box.SQUARE_DOUBLE_HEAD,
                padding=(0,4),
                style= Style(bgcolor=selectedBg if is_selected else "#0D1117"),
                expand=True
            )
        )

    contentGroup = Group(
        Align.center(titleText),
        Text(""),
        *settingPanel
    )

    settingsPanel = Panel(
        contentGroup,
        title="Preferences",
        title_align="left",
        border_style=outerBorder,
        box=box.SQUARE_DOUBLE_HEAD,
        padding=(1,2),
        expand=True
    )

    output = StringIO()


    terminalWidth = shutil.get_terminal_size().columns
    consoleWidth = max(40,terminalWidth -2)

    rich_console = Console(
        file=output,
        force_terminal=True,
        color_system="truecolor",
        width=consoleWidth
    )

    rich_console.print(settingsPanel)

    return ANSI(output.getvalue())
