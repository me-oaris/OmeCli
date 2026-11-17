from rich.console import Console, Group
from rich.text import Text
from rich.align import Align
from rich.panel import Panel
from rich.style import Style
from rich import box

from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.styles import Style as PTStyle

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

bindings = KeyBindings()

style = PTStyle.from_dict({
    "selected": "fg:#FFFFFF bg:#123D2A bold",
    "normal": "fg:#FFFFFF",
})
# Gotta find a way to make menu dynamic for it to work with binding
def get_menu():
    print("Yum!! Buttons here (Ts is ass):")
    print(options[0][0])
    print(options[1][0])
    print(options[2][0])
    print(options[3][0])

#Bindings for Controls Remaining

application = Application(
    layout=Layout(
        Window(
            FormattedTextControl(get_menu),
            dont_extend_height=True
        )
    ),
    key_bindings=bindings,
    style=style,
    full_screen=False
)

option = application.run()

console.print(f"You selected: {options[option][0]}")