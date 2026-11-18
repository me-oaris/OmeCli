<h1 align="center">OmeCli</h1>

<p align="center">
    <b>An anonymous Omegle clone made for the command line</b>
</p>

Well, most CLI apps out there are pretty bland, so I wanted to mix things up by building something that integrates OpenCV video processsing and a slick, modern terminal UI.
What's better than spending your time in terminal talking to complete strangers?

<p align="center">
    <img alt="OmeCli Preview" src="https://i.ibb.co/5xSrWMKP/image.png" width="800">
</p>

## Overview

OmeCli captures live frames straight from your webcam, converts them on the fly into realtime ASCII art, and streams everything seamlessly to the server using WebSockets. Zero clutter, full anonymity

## Features

**ASCII Video Engine**: Captures webcam frames using OpenCV and renders them live into terminal ASCII art
**Built-In Themes**: Switch dynamically from one theme to another, anytime, anywhere, based of your mood
    - **Dark Mode**: Clean default terminal look
    - **Cyber Green**: Matrix inspired green look
    - **Amber Retro**: Warm terminal look
    - **Synthwave**: Neon pink cyberpunk look
    - **Dracula**: Deep purple, cyan look
**Chat History Log**: Automatically saved chats from each conversations with timestamps
**Fully Keyboard Driven**: Smooth navigation with only keyboard

## Project Structure

```
OmeCli/
├── client/
│   ├── pages/
│   │   ├── about.py        # About page
│   │   ├── home.py         # Main menu
│   │   ├── room.py         # Talk/Chat room
│   │   └── settings.py     # Theme switcher and user preferences
│   ├── video/
│   │   └── engine.py       # CV2 ASCII Engine
│   ├── config.json         # Persistent settings
│   └── main.py             # Client initilization, handlers, websockets
├── server/
│   └── server.py           # Serverside websockets
├── pyproject.toml          # PyPI packaging & CLI entry point config
└── README.md               # Project documentation
```

## Installation and Quick Start

**Install via PyPi**

```
pip install omecli
omecli
```

**Run Locally**

1. Clone Repository
```
git clone [https://github.com/yourusername/OmeCli.git](https://github.com/yourusername/OmeCli.git)
cd OmeCli
```

2. Install Dependencies

```
pip install prompt-toolkit rich websockets opencv-python
```

3. Start the WebSocket Server

```
python server/server.py
```

4. Launch the Client

```
python client/main.py
```

## Controls and Commands

| Key / Command | Action |
| :--- | :--- |
| `↑` / `↓` | Navigate menus and settings |
| `Enter` | Select option / Send chat message |
| `Esc` | Return to main menu / Disconnect from room |
| `/next` | Skip current stranger and match with someone new |

## Tech Stack
- **Terminal UI**: `prompt_toolkit` and `rich`
- **Networking**: `websockets`
- **Video Engine**: `OpenCV (cv2)`
- **Config Storage** : `JSON`