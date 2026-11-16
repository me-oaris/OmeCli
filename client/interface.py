from rich.console import Console, Group
from rich.text import Text
from rich.align import Align
from rich.panel import Panel
from rich.style import Style
from rich import box

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

console.print(welcomePanel)

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

console.print(buttons)