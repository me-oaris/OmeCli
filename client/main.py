from pages.home import render_home
from pages.room import render_room
from rich.console import Console
from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.controls import FormattedTextControl 
from prompt_toolkit.styles import Style as PTStyle
from prompt_toolkit.formatted_text import ANSI
from prompt_toolkit.widgets import TextArea
from prompt_toolkit.layout.containers import Window, HSplit, ConditionalContainer
from prompt_toolkit.filters import Condition


richConsole = Console()
bindings = KeyBindings()

style = PTStyle.from_dict({
    "selected": "fg:#FFFFFF bg:#123D2A bold",
    "normal": "fg:#FFFFFF"
})   

selected = 0
current_page = "menu"
messages = []

def send_message(buffer):
    message = buffer.text.strip()
    if message:
        messages.append(message)
    buffer.text = ""
    app.invalidate()

message_input = TextArea(
    height=1,
    prompt="You: ",
    style="class:input-field",
    multiline=False,
    wrap_lines=False,
    accept_handler=send_message
)

def get_page():
    if current_page == "menu":  
        return render_home(selected)
    elif current_page == "room":
        return render_room(messages)
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

@bindings.add(
        "enter",
        filter=Condition(lambda: current_page == "menu"))
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

@bindings.add("/")
def focus_input(event):
    if current_page == "room":
        message_input.buffer.cursor_position = len(message_input.text)
        event.app.layout.focus(message_input.window)

app = Application(
    layout=Layout(
        HSplit([
            Window(
                FormattedTextControl(get_page),
                dont_extend_height=True
            ),
            ConditionalContainer(
                content=message_input,
                filter=Condition(lambda: current_page == "room")
            )
        ])
    ),
    key_bindings=bindings,
    style=style,
    full_screen=True,
    erase_when_done=True
)

menu = app.run()

if menu is None:
    exit()
