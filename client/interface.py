from rich.console import Console, Group
from rich.text import Text
from rich.align import Align
from rich.panel import Panel
from rich.style import Style
from rich import box
from io import StringIO
from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.styles import Style as PTStyle
from prompt_toolkit.formatted_text import ANSI

console = Console()

logs = Text()

logs.append("◈ ", style="bold blue")
logs.append("OMECLI", style="bold white")
logs.append(" / ANONYMOUS CHAT", style="dim white")

#console.print(Panel(Align.center(logs, vertical="middle"), box=box.SQUARE, padding=(2,4), title="Title IG", subtitle="Subtitle"))


welcomeText = Text()
versionText = Text()

welcomeText.append("Welcome to OmeCli\n", style="bold white")
welcomeText.append("""                                                        
  ▄▄▄▄▄   ▄▄▄      ▄▄▄  ▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄ ▄▄▄      ▄▄▄▄▄ 
▄███████▄ ████▄  ▄████ ███▀▀▀▀▀ ███▀▀▀▀▀ ███       ███  
███   ███ ███▀████▀███ ███▄▄    ███      ███       ███  
███▄▄▄███ ███  ▀▀  ███ ███      ███      ███       ███  
 ▀█████▀  ███      ███ ▀███████ ▀███████ ████████ ▄███▄ 
                                                        
                                                        \n""", style="bold cyan")

versionText.append("Version 0.0.1", style="dim italic white")

centeredText = Group(
    Align.left(welcomeText),
    Align.right(versionText)
)

welcomePanel = Panel(centeredText,box=box.SQUARE_DOUBLE_HEAD)

#console.print(welcomePanel)

findButton = Panel(
    Align.center(
        Text("1. Find a Stranger", style="bold white")
    ),
    border_style="bright_green",
    box = box.SQUARE_DOUBLE_HEAD,
    padding=(0,4)
)

aboutButton = Panel(
    Align.center(
        Text("2. About OmeCli", style="bold white")
    ),
    border_style="bright_blue",
    box = box.SQUARE_DOUBLE_HEAD,
    padding=(0,4)   
)
settingButton = Panel(
    Align.center(
        Text("3. Settings", style="bold white")
    ),
    border_style="bright_white",
    box=box.SQUARE_DOUBLE_HEAD,
    padding=(0,4)
)

quitButton = Panel(
    Align.center(
        Text("4. Quit OmeCli", style="bold white")
    ),
    border_style="bright_red",
    box=box.SQUARE_DOUBLE_HEAD,
    padding=(0,4),
    style=Style(bgcolor="bright_red")
)

buttons = Group(
    findButton,
    aboutButton,
    settingButton,
    quitButton
)

# console.print(buttons)

options = [
    ("1. Find a Stranger", "#123D2A", "bright_green"),
    ("2. About OmeCli", "#172D4D", "bright_blue"),
    ("3. Settings", "#303030", "bright_white"),
    ("4. Quit OmeCli", "#4A1717", "bright_red")
]

selected = 0
current_page = "menu"

bindings = KeyBindings()

style = PTStyle.from_dict({
    "selected": "fg:#FFFFFF bg:#123D2A bold",
    "normal": "fg:#FFFFFF",
})

def get_menu():
    if current_page == "room":
        return ANSI("\033[2J\033[HFind a Stranger")
    elif current_page == "about":
        return ANSI("\033[2J\033[HAbout OmeCli")
    elif current_page == "settings":
        return ANSI("\033[2J\033[HSettings")
    
    output = StringIO()

    rich_Console = Console(
        file=output,
        force_terminal=True,
        color_system="truecolor",
        width=60   
        )

    rich_Console.print(welcomePanel)

    buttons_panels = [
        Panel(
            Align.center(Text("1. Find a Stranger", style="bold white")),
            border_style="bright_green",
            box=box.SQUARE_DOUBLE_HEAD,
            padding=(0,4),
            style=Style(bgcolor="#123D2A" if selected == 0 else "#0D1117")
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

    for button in buttons_panels:
        rich_Console.print(button)

    return ANSI(output.getvalue())

#Starting Bindings

@bindings.add("up")
def move_up(event):
    global selected
    if selected == 0:
        selected = 3
    else:
        selected -= 1
    event.app.invalidate()

@bindings.add("down")
def move_down(event):
    global selected
    if selected == 3:
        selected = 0
    else:
        selected += 1
    event.app.invalidate()

@bindings.add("enter")
def select_option(event):
    global current_page

    if selected == 0:
        current_page = "room"
    elif selected == 1:
        current_page = "about"
    elif selected == 2:
        current_page = "settings"
    elif current_page == 3:
        event.app.exit()
        return

    event.app.invalidate()

application = Application(
    layout=Layout(
        Window(
            FormattedTextControl(get_menu),
            dont_extend_height=True
        )
    ),
    key_bindings=bindings,
    style=style,
    full_screen=True,
    erase_when_done=True
)

option = application.run()

console.print(f"You selected: {options[option][0]}")