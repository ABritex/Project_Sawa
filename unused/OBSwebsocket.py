import configparser
from obswebsocket import obsws, requests
from rich import print

class OBSWebsocketsManager:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        obs_config = config['OBS']
        host = obs_config.get('HOST', 'localhost')
        port = obs_config.getint('PORT', 4444)
        password = obs_config.get('PASSWORD', '')
        
        print(f"Connecting to OBS Websockets on {host}:{port}...")
        self.client = obsws(host, port, password)
        try:
            self.client.connect()
            print(f"[green]Connected to OBS Websockets! OBS version: {self.client.call(requests.GetVersion()).getObsVersion()}")
        except Exception as e:
            print(f"[red]COULD NOT CONNECT TO OBS!\n{e}")
            self.client = None

    def disconnect(self):
        if self.client:
            self.client.disconnect()

    def set_scene(self, new_scene):
        if self.client:
            self.client.call(requests.SetCurrentProgramScene(sceneName=new_scene))

    def set_text(self, source_name, new_text):
        if self.client:
            self.client.call(requests.SetInputSettings(
                inputName=source_name, 
                inputSettings={"text": new_text}
            ))

    def get_source_transform(self, scene_name, source_name):
        try:
            response = self.client.call(
                requests.GetSceneItemId(sceneName=scene_name, sourceName=source_name)
            )
            myItemID = response.datain.get("sceneItemId")
            if myItemID is None:
                raise ValueError("Failed to get scene item ID.")
            
            response = self.client.call(
                requests.GetSceneItemTransform(sceneName=scene_name, sceneItemId=myItemID)
            )
            
            scene_item_transform = response.datain.get("sceneItemTransform", {})
            transform = {
                "positionX": scene_item_transform.get("positionX", 0),
                "positionY": scene_item_transform.get("positionY", 0),
                "scaleX": scene_item_transform.get("scaleX", 1),
                "scaleY": scene_item_transform.get("scaleY", 1),
                "rotation": scene_item_transform.get("rotation", 0),
                "sourceWidth": scene_item_transform.get("sourceWidth", 0),
                "sourceHeight": scene_item_transform.get("sourceHeight", 0),
                "width": scene_item_transform.get("width", 0),
                "height": scene_item_transform.get("height", 0),
                "cropLeft": scene_item_transform.get("cropLeft", 0),
                "cropRight": scene_item_transform.get("cropRight", 0),
                "cropTop": scene_item_transform.get("cropTop", 0),
                "cropBottom": scene_item_transform.get("cropBottom", 0)
            }
            return transform

        except Exception as e:
            print(f"Error getting source transform: {e}")
            return {}

    def set_source_transform(self, scene_name, source_name, new_transform):
        try:
            response = self.client.call(
                requests.GetSceneItemId(sceneName=scene_name, sourceName=source_name)
            )
            myItemID = response.datain.get("sceneItemId")
            if myItemID is None:
                raise ValueError("Failed to get scene item ID.")
            
            self.client.call(
                requests.SetSceneItemTransform(
                    sceneName=scene_name,
                    sceneItemId=myItemID,
                    sceneItemTransform=new_transform,
                )
            )

        except Exception as e:
            print(f"Error setting source transform: {e}")

    def set_text_style(self, source_name, font_size, color):
        if self.client:
            self.client.call(requests.SetInputSettings(
                inputName=source_name, 
                inputSettings={
                    "font": {"size": font_size},
                    "color": color
                }
            ))

if __name__ == "__main__":
    # Test the connection
    obs_manager = OBSWebsocketsManager()
    obs_manager.disconnect()