from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout  import Layout
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.controls import FormattedTextControl

selected = 0
items = ["Find a stranger", "About OmeCli", "Settings", "Quit OmeCli"]

def get_menu():
    result = []

    for i, item in enumerate(items):
        if i == selected:
            result.append(("fg:white bg:green bold", f" > {item} \n"))
        else:
            result.append(("fg:white", f" {item} \n"))
    return result

kb =KeyBindings()

@kb.add("up")
def move_up(event):
    global selected
    if selected == 0:
        selected = 3
    else:
        selected -= 1
    event.app.invalidate()

@kb.add("down")
def move_down(event):
    global selected
    if selected == 3:
        selected = 0
    else:
        selected += 1
    event.app.invalidate()

@kb.add("enter")
def select(event):
    event.app.exit(result=items[selected])

app = Application(
    layout=Layout(
       Window(FormattedTextControl(get_menu))
    ),
    key_bindings=kb,
    full_screen=True,
    erase_when_done=True
)

print("Selected", app.run())