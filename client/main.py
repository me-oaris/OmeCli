from pages.home import render_home
from pages.room import render_room
from pages.about import render_about
from pages.settings import render_settings
from video.engine import VideoEngine
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
import shutil
import asyncio
import websockets
import json
import datetime
import os

apiUrl = "ws://localhost:8765"
configFile = "config.json"

bindings = KeyBindings()
videoEngine = VideoEngine()

style = PTStyle.from_dict({
    "selected": "fg:#FFFFFF bg:#123D2A bold",
    "normal": "fg:#FFFFFF"
})   

selected = 0
selectedSetting = 0
current_page = "menu"
messages = []
websocketConnection = None
strangerFrame = "Waiting for stranger video..."

defSettings = {
    "theme": "Dark Mode",
    "anon_display": True,
    "save_history": False
}

def loadSettings():
    if os.path.exists(configFile):
        try:
            with open(configFile, "r", encoding="utf-8") as f:
                saved = json.load(f)
                return {**defSettings, **saved}
        except Exception:
            pass
    return defSettings.copy()

def saveSettings():
    try:
        with open(configFile, "w", encoding="utf-8") as f:
            json.dump(appSettings, f, indent=4)
    except Exception:
        pass

appSettings = loadSettings()


async def connectToServer():
    global websocketConnection, strangerFrame
    try:
        async with websockets.connect(apiUrl) as websocket:
            websocketConnection = websocket
            app.invalidate()

            async for rawMessage in websocket:
                data = json.loads(rawMessage)
                msgType = data.get("type")

                if msgType == "status":
                    messages.append(data.get("message"))
                elif msgType == "message":
                    messages.append(f"Stranger: {data.get('text')}")
                elif msgType == "video":
                    strangerFrame = data.get("frame", "")
                app.invalidate()

    except (websockets.exceptions.ConnectionClosed, ConnectionRefusedError):
        messages.append("Connection to server lost")
        websocketConnection = None
        app.invalidate()

async def videoStreamLoop():
    global websocketConnection
    while True:
        if current_page == "room" and websocketConnection:
            try:
                terminalWidth = shutil.get_terminal_size().columns
                panelInnerWidth = max(20, ((terminalWidth - 2) // 2) - 6)
                frame = videoEngine.get_ascii_frame(targetWidth=panelInnerWidth)

                await websocketConnection.send(json.dumps({
                    "type" : "video",
                    "frame" : frame
                }))
            except Exception:
                pass
        await asyncio.sleep(1 / 15)

def send_message(buffer):
    global websocketConnection
    text = buffer.text.strip()
    if text:
        if text.lower() == "/next":
            messages.append("You skipped the stranger")
            if websocketConnection:
                asyncio.create_task(websocketConnection.send(json.dumps({
                    "type" : "skip"
                })))
        else:
            messages.append(f"You: {text}")
            if websocketConnection:
                asyncio.create_task(websocketConnection.send(json.dumps({
                    "type" : "message",
                    "text" : text
                })))
    buffer.text = ""
    app.invalidate()

def getDynamicStyle():
    if appSettings.get("theme") == "Cyber Green":
        return PTStyle.from_dict({
            "selected" : "fg:#000000 bg:#00FF66 bold",
            "normal" : "fg:#00FF66"
        })
    elif appSettings.get("theme") == "Amber Retro":
        return PTStyle.from_dict({
            "selected" : "fg:#000000 bg:#FFB000 bold",
            "normal" : "fg:#FFB000"
        })
    elif appSettings.get("theme") == "Synthwave":
        return PTStyle.from_dict({
            "selected" : "fg:#FFFFFF bg:#FF007F bold",
            "normal" : "fg:#FF007F" 
        })
    elif appSettings.get("theme") == "Dracula":
        return PTStyle.from_dict({
            "selected" : "fg:#F8F8F2 bg:#BD93F9 bold",
            "normal" : "fg:#8D93F9"
        })
    else:
        return PTStyle.from_dict({
            "selected" : "fg:#FFFFFF bg:#123D2A bold",
            "normal" : "fg:#FFFFFF"
        })

def saveChatHistory():
    if appSettings.get("save_history") and messages:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"chat_history_{timestamp}.txt"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write("\n".join(messages))
            messages.append(f"History saved to {filename}")
        except Exception:
            pass
    

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
        return render_home(selected, appSettings)
    elif current_page == "room":
        terminalWidth = shutil.get_terminal_size().columns
        panelInnerWidth = max(20, ((terminalWidth - 2) // 2) - 6)
        yourframe = videoEngine.get_ascii_frame(targetWidth=panelInnerWidth)
        return render_room(messages, yourFrame=yourframe, strangerFrame=strangerFrame, appSettings=appSettings)
    elif current_page == "about":
        return render_about(appSettings)
    elif current_page == "settings":
        return render_settings(selectedSetting, appSettings)

@bindings.add("up")
def move_up(event):
    global selected, selectedSetting
    if current_page == "menu":
        selected = 3 if selected == 0 else selected - 1
    elif current_page == "settings":
        selectedSetting = 3 if selectedSetting == 0 else selectedSetting - 1
    event.app.invalidate()

@bindings.add("down")
def move_down(event):
    global selected, selectedSetting
    if current_page == "menu":
        selected = 0 if selected == 3 else selected + 1
    elif current_page == "settings":
        selectedSetting = 0 if selectedSetting == 3 else selectedSetting + 1
    event.app.invalidate()

@bindings.add("enter",
              filter=Condition(lambda: current_page in ("menu", "settings"))
)
def handle_enter(event):
    global current_page, selectedSetting
    if current_page == "menu":
        if selected == 0:
            current_page = "room"
            messages.clear()
            messages.append("Connecting to server ...")
            asyncio.create_task(connectToServer())
            event.app.layout.focus(message_input.window)
        elif selected == 1:
            current_page = "about"
        elif selected == 2:
            selectedSetting = 0
            current_page = "settings"
        elif selected == 3:
            event.app.exit()
            return
    elif current_page == "settings":
        if selectedSetting == 0:
            themes = ["Dark Mode", "Cyber Green", "Amber Retro", "Synthwave", "Dracula"]
            currentTheme = appSettings["theme"]
            nextIndex = (themes.index(currentTheme) + 1) % len(themes)
            appSettings["theme"] = themes[nextIndex]
            app.style = getDynamicStyle()
            saveSettings()
        elif selectedSetting == 1:
            appSettings['anon_display'] = not appSettings['anon_display']
        elif selectedSetting == 2:
            appSettings['save_history'] = not appSettings['save_history']
        elif selectedSetting == 3:
            current_page = "menu"
    event.app.invalidate()

@bindings.add("escape")
def go_back(event):
    global current_page, websocketConnection
    if current_page != "menu":
        if current_page == "room":
            saveChatHistory()
            videoEngine.stop()
            if websocketConnection:
                asyncio.create_task(websocketConnection.close())
                websocketConnection = None
        current_page = "menu"
        event.app.invalidate()

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

async def videoLoop():
    while True:
        if current_page == "room":
            app.invalidate()
        await asyncio.sleep(1 / 15)

async def main():
    asyncio.create_task(videoLoop())
    asyncio.create_task(videoStreamLoop())
    await app.run_async()
    videoEngine.stop()

if __name__ == "__main__":
    asyncio.run(main())