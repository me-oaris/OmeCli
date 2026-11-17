from pages.home import render_home
from rich.console import Console
from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.controls import FormattedTextControl 
from prompt_toolkit.styles import Style as PTStyle
from prompt_toolkit.formatted_text import ANSI


richConsole = Console()
bindings = KeyBindings()

style = PTStyle.from_dict({
    "selected": "fg:#FFFFFF bg:#123D2A bold",
    "normal": "fg:#FFFFFF"
})   

selected = 0
current_page = "menu"

def get_menu():
    if current_page == "menu":  
        return render_home(selected)
    elif current_page == "room":
        return ANSI("Find a Stranger")
    elif current_page == "about":
        return ANSI("About OmeCli")
    elif current_page == "settings":
        return ANSI("Settings")

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
def select_page(event):
    global current_page
    if selected == 0:
        current_page = "room"
    elif selected == 1:
        current_page = "about"
    elif selected == 2:
        current_page = "settings"
    elif selected == 3:
        event.app.exit()
        return
    event.app.invalidate()

@bindings.add("escape")
def go_back(event):
    global current_page
    if current_page != "menu":
        current_page = "menu"
    event.app.invalidate()

app = Application(
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

menu = app.run()

if menu is None:
    exit()
