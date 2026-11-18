import asyncio
import websockets
import json

waitingClient = set()
pairs = {}

async def handler(websocket):
    global waitingClient
    print(f"Client Connected: {websocket.remote_address}")

    try:
        while True:
            if websocket not in pairs:
                if websocket not in waitingClient:
                    waitingClient.add(websocket)
                    await websocket.send(json.dumps({
                        "type" : "status",
                        "message" : "Searching for stranger..."
                    }))

                while websocket not in pairs:
                    otherClients = [c for c in waitingClient if c != websocket and c.close_code is None]

                    if otherClients:
                        peer = otherClients[0]

                        waitingClient.discard(websocket)
                        waitingClient.discard(peer)

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
                        break

                    await asyncio.sleep(0.5)
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
                            elif msgType == "video":
                                if peerSocket in pairs:
                                    await peerSocket.send(json.dumps({
                                        "type" : "video",
                                        "frame" : data.get("frame")
                                    }))
                            elif msgType == "skip":
                                pairs.pop(websocket,None)
                                if peerSocket in pairs:
                                    pairs.pop(peerSocket, None)
                                    waitingClient.add(peerSocket)
                                    await peerSocket.send(json.dumps({
                                        "type" : "status",
                                        "message" : "Stranger has discontinued. Finding a new stranger..."
                                    }))

                                waitingClient.add(websocket)
                                await websocket.send(json.dumps({
                                    "type" : "status",
                                    "message" : "Searching for a stranger..."
                                }))
                                break
                    except websockets.exceptions.ConnectionClosed:
                        break

    except websockets.exceptions.ConnectionClosed:
        print(f"Cleint Disconnected: {websocket.remote_address}")
    finally:
        waitingClient.discard(websocket)

        peerSocket = pairs.pop(websocket, None)
        if peerSocket:
            pairs.pop(peerSocket, None)
            waitingClient.add(peerSocket)
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

        print(f"Cleaned up connection for {websocket.remote_address}")

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765, ping_interval=5, ping_timeout=5):
        print("Websocket Online, `ws://0.0.0.0:8765`")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
                