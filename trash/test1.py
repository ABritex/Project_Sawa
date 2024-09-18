import sounddevice as sd
import numpy as np
import asyncio
import websockets
import json
import logging
import configparser
import soundfile as sf
import time

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

VTS_API_URL = "ws://127.0.0.1:8001"

class VTubeStudioAPI:
    def __init__(self):
        self.websocket = None
        self.auth_token = None
        self.config = self.load_config("config.ini")
        self.auth_token = self.config["vtubestudio"].get("auth_token")
        self.smoothing_factor = 0.1
        self.last_value = 0.0

    def load_config(self, filename):
        config = configparser.ConfigParser()
        config.read(filename)
        return config

    async def connect(self):
        try:
            self.websocket = await websockets.connect(VTS_API_URL)
            logging.info("Connected to VTube Studio")
            await self.authenticate()
        except websockets.exceptions.ConnectionClosed:
            logging.error("Failed to connect to VTube Studio. Is it running?")
            raise
        except Exception as e:
            logging.error(f"Unexpected error during connection: {str(e)}")
            raise

    async def authenticate(self):
        try:
            if self.auth_token:
                auth_request = {
                    "apiName": "VTubeStudioPublicAPI",
                    "apiVersion": "1.0",
                    "requestID": "authenticate",
                    "messageType": "AuthenticationRequest",
                    "data": {
                        "pluginName": "VTubeLipSync",
                        "pluginDeveloper": "YourName",
                        "authenticationToken": self.auth_token
                    }
                }
                await self.websocket.send(json.dumps(auth_request))
                response = await self.websocket.recv()
                logging.debug(f"Authentication response with existing token: {response}")
                response_data = json.loads(response)

                if response_data.get("messageType") == "AuthenticationResponse":
                    if response_data.get("data", {}).get("authenticated") == True:
                        logging.info("Successfully authenticated with VTube Studio")
                        return
                    else:
                        logging.warning("Token is invalid or revoked, requesting a new token")
                else:
                    raise Exception("Unexpected response to authentication request with existing token")
            
            token_request = {
                "apiName": "VTubeStudioPublicAPI",
                "apiVersion": "1.0",
                "requestID": "token_request",
                "messageType": "AuthenticationTokenRequest",
                "data": {
                    "pluginName": "VTubeLipSync",
                    "pluginDeveloper": "YourName"
                }
            }
            await self.websocket.send(json.dumps(token_request))
            token_response = await self.websocket.recv()
            logging.debug(f"Token request response: {token_response}")
            token_data = json.loads(token_response)
            
            if token_data.get("data", {}).get("authenticationToken"):
                self.auth_token = token_data["data"]["authenticationToken"]
                auth_request["data"]["authenticationToken"] = self.auth_token
                await self.websocket.send(json.dumps(auth_request))
                final_response = await self.websocket.recv()
                logging.debug(f"Final auth response: {final_response}")
                final_data = json.loads(final_response)
                
                if final_data.get("data", {}).get("authenticated") == True:
                    logging.info("Successfully authenticated with VTube Studio")
                else:
                    raise Exception("Failed to authenticate with the newly obtained token")
            else:
                raise Exception("Failed to get a new authentication token")
        except Exception as e:
            logging.error(f"Error during authentication: {str(e)}")
            raise

    async def send_mouth_open_value(self, value):
        smoothed_value = (self.smoothing_factor * value) + ((1 - self.smoothing_factor) * self.last_value)
        self.last_value = smoothed_value
        smoothed_value = np.clip(smoothed_value, 0, 1)

        payload = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": f"mouth_open_{smoothed_value}",
            "messageType": "InjectParameterDataRequest",
            "data": {
                "parameterValues": [{
                    "id": "MouthOpen",
                    "value": smoothed_value
                }]
            }
        }
        
        try:
            await self.websocket.send(json.dumps(payload))
            logging.debug(f"Sent mouth open value: {smoothed_value}")
        except Exception as e:
            logging.error(f"Error sending mouth open value: {str(e)}")

async def process_mouth_open_values(mouth_open_queue, vts_api):
    last_update_time = time.time()
    update_interval = 0.1

    while True:
        current_time = time.time()
        if current_time - last_update_time >= update_interval:
            try:
                if not mouth_open_queue.empty():
                    value = await mouth_open_queue.get()
                    await vts_api.send_mouth_open_value(value)
                last_update_time = current_time
            except Exception as e:
                logging.error(f"Error processing mouth open value: {str(e)}")

async def main():
    vts_api = VTubeStudioAPI()
    try:
        await vts_api.connect()
    except Exception as e:
        logging.error(f"Failed to connect and authenticate: {str(e)}")
        return

    # Read and process audio file
    wav_file = 'output.wav'
    try:
        # Read the audio file
        data, fs = sf.read(wav_file, dtype='float32')
        
        # Check if data is 1D (mono) or 2D (stereo)
        if len(data.shape) == 1:
            logging.info("Audio file is mono.")
        elif len(data.shape) == 2:
            logging.info("Audio file is stereo.")
            # Use only one channel for processing, e.g., left channel
            data = data[:, 0]
        else:
            raise ValueError("Unsupported audio format")

    except Exception as e:
        logging.error(f"Failed to read audio file: {str(e)}")
        return


    # Queue for mouth open values
    mouth_open_queue = asyncio.Queue()

    # Process audio data to set mouth open values
    def process_audio_data():
        window_size = 2048
        step_size = 1024

        for start in range(0, len(data) - window_size, step_size):
            window = data[start:start + window_size]
            rms_value = np.sqrt(np.mean(window**2))
            normalized_value = np.clip(rms_value * 1000, 0, 1)  # Adjust scaling factor as needed
            logging.debug(f"Calculated mouth open value: {normalized_value}")
            mouth_open_queue.put_nowait(normalized_value)

    process_audio_data()

    try:
        with sd.OutputStream(samplerate=fs, channels=1):
            asyncio.create_task(process_mouth_open_values(mouth_open_queue, vts_api))
            await asyncio.sleep(len(data) / fs)
    except Exception as e:
        logging.error(f"Error during audio playback: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
