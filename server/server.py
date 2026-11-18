import asyncio
import websockets
import json

waitingClient = None
pairs = {}

async def handler(websocket):
    global waitingClient
    print(f"Client Connected: {websocket.remote_address}")

    try:
        while True:
            if websocket not in pairs:
                if waitingClient is None:
                    waitingClient = websocket
                    await websocket.send(json.dumps({
                        "type" : "status",
                        "message" : "Searching for stranger..."
                    }))

                    while waitingClient == websocket and websocket not in pairs:
                        await asyncio.sleep(0.5)

                elif waitingClient == websocket:
                    await asyncio.sleep(0.5)
                else:
                    peer = waitingClient
                    waitingClient = None

                    pairs[websocket] = peer
                    pairs[peer] = websocket

                    await websocket.send(json.dumps({
                        "type" : "status",
                        "message" : "Connected to a stranger!"
                    }))

                    await peer.send(json.dumps({
                        "type" : "status",
                        "message" : "Connected to a stranger!"
                    }))

                peerSocket = pairs.get(websocket)
                if peerSocket:
                    try:
                        async for rawMessage in websocket:
                            data = json.loads(rawMessage)
                            msgType = data.get("type")

                            if msgType == "message":
                                if peerSocket in pairs:
                                    await peerSocket.send(json.dumps({
                                        "type" : "message",
                                        "text" : data.get("text")
                                    }))
                            elif msgType == "skip":
                                pairs.pop(websocket, None)
                                if peerSocket in pairs:
                                    pairs.pop(peerSocket, None)
                                    await peerSocket.sendZ(json.dumps({
                                        "type" : "status",
                                        "message" : "Stranger has disconnected. Finding a new stranger..."
                                    }))
                                    waitingClient = peerSocket
                                    await peerSocket.send(json.dumps({
                                        "type" : "status",
                                        "message" : "Searching for a stranger..."
                                    }))

                                waitingClient = websocket
                                await websocket.send(json.dumps({
                                    "type" : "status",
                                    "message" : "Searching for a stranger..."
                                }))
                                break
                    except websockets.exceptions.ConnectionClosed:
                        break

    except websockets.exceptions.ConnectionClosed:
        print(f"Client disconnected: {websocket.remote_address}")
    finally:
        if waitingClient == websocket:
            waitingClient = None

        peerSocket = pairs.pop(websocket, None)
        if peerSocket:
            pairs.pop(peerSocket, None)
            waitingClient = peerSocket
            try:
                await peerSocket.send(json.dumps({
                    "type" : "status",
                    "message" : "Stranger has disconnected!"
                }))
                await peerSocket.send(json.dumps({
                    "type" : "status",
                    "message" : "Searching for stranger..."
                }))
            except:
                pass
        print(f"Initilized websock for {websocket.remote_address}")

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("Websocket Online, `ws://localhost:8765`")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())