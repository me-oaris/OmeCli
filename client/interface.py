from rich.console import Console
from rich.text import Text
from rich.align import Align
from rich.panel import Panel
from rich.table import Table
from rich import box

console = Console()

logs = Text()

logs.append("◈ ", style="bold blue")
logs.append("OMECLI", style="bold white")
logs.append(" / ANONYMOUS CHAT", style="dim white")

#console.print(Panel(Align.center(logs, vertical="middle"), box=box.SQUARE, padding=(2,4), title="Title IG", subtitle="Subtitle"))


welcomeText = Text()

welcomeText.append("Welcome to OmeCli\n", style="bold white")
welcomeText.append("""                                                        
  ▄▄▄▄▄   ▄▄▄      ▄▄▄  ▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄ ▄▄▄      ▄▄▄▄▄ 
▄███████▄ ████▄  ▄████ ███▀▀▀▀▀ ███▀▀▀▀▀ ███       ███  
███   ███ ███▀████▀███ ███▄▄    ███      ███       ███  
███▄▄▄███ ███  ▀▀  ███ ███      ███      ███       ███  
 ▀█████▀  ███      ███ ▀███████ ▀███████ ████████ ▄███▄ 
                                                        
                                                        \n""", style="bold cyan")
welcomeText.append("Version 0.0.1", style="dim italic white")

centeredText = Align.left(welcomeText, vertical="top")

welcomePanel = Panel(centeredText,box=box.SQUARE_DOUBLE_HEAD)

console.print(welcomePanel)
