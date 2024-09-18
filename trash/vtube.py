import asyncio
import websockets
import json
import configparser

class VTubeStudio:
    def __init__(self):
        # Load the configuration
        self.config = self.load_config("config.ini")
        self.auth_token = self.config["vtubestudio"]["auth_token"]
        self.websocket = None

    def load_config(self, filename):
        config = configparser.ConfigParser()
        config.read(filename)
        return config

    async def connect(self):
        """Establishes WebSocket connection."""
        self.websocket = await websockets.connect("ws://localhost:8001")

    async def authenticate(self):
        """Authenticates with VTube Studio using the auth token."""
        if self.websocket is None:
            await self.connect()

        auth_request = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "authenticate",
            "messageType": "AuthenticationRequest",
            "data": {
                "pluginName": "YourPlugin",
                "pluginDeveloper": "YourName",
                "authenticationToken": self.auth_token
            }
        }
        # Send authentication request
        await self.websocket.send(json.dumps(auth_request))
        response = await self.websocket.recv()
        print(f"Authentication response: {response}")
        return json.loads(response)

    async def trigger_animation(self):
        """Sends an expression change request."""
        if self.websocket is None:
            print("WebSocket is not connected. Reconnecting...")
            await self.connect()

        expression_request = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "changeExpression",
            "messageType": "ExpressionChangeRequest",
            "data": {
                "expressionFile": "happy.json",  # Example expression file name
                "fadeTime": 0.5
            }
        }
        # Send request to change expression
        await self.websocket.send(json.dumps(expression_request))
        response = await self.websocket.recv()
        print(f"Expression change response: {response}")
