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

    titleStyle = "bold bright_green" if isCyber else "bold yellow"
    outerBorder = "bright_green" if isCyber else "yellow"
    selectedBorder = "bright_green" if isCyber else "bright_yellow"
    selecteBg = "#00FF66" if isCyber else "#3A3012"
    selectedFg = "#000000" if isCyber else "white"

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
                style= Style(bgcolor=selecteBg if is_selected else "#0D1117"),
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
