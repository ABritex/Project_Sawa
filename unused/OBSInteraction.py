import asyncio
from OBSwebsocket import OBSWebsocketsManager

class ObsInteractions:
    def __init__(self, obs: OBSWebsocketsManager):
        self.obs = obs
        self.screen_width = 1920  # Assuming a 1920x1080 resolution
        self.screen_height = 1080
        
    async def update_subtitle(self, scene_name: str, text_source: str, new_text: str):
        print(f"[green]OBS: Updating scene to '{scene_name}' and setting subtitle...")

        # Set the scene
        self.obs.set_scene(scene_name)

        # Set the larger font size
        font_size = 48  # Increased font size for more visibility
        max_width = self.screen_width * 0.9  # 90% of the screen width for padding

        # Estimate the width of the text
        estimated_text_width = len(new_text) * (font_size // 2)

        # If text exceeds screen width, reduce font size
        if estimated_text_width > max_width:
            scaling_factor = max_width / estimated_text_width
            font_size = int(font_size * scaling_factor)
            estimated_text_width = max_width

        # Center the text horizontally
        positionX = (self.screen_width - estimated_text_width) // 2

        # Get current transform
        current_transform = self.obs.get_source_transform(scene_name, text_source)
        
        # Apply new transform for subtitle positioning
        new_transform = {
            "positionX": positionX,
            "positionY": 1000,  # Near bottom of the screen
            "scaleX": 1,
            "scaleY": 1,
            "width": current_transform["sourceWidth"],
            "height": current_transform["sourceHeight"],
        }
        self.obs.set_source_transform(scene_name, text_source, new_transform)

        # Set the adjusted text style (with larger font size)
        self.obs.set_text_style(text_source, font_size, 0xFFFFFFFF)  # White color

        # Update the text
        self.obs.set_text(text_source, new_text)
        
        await asyncio.sleep(5)
        print("[green]OBS: Subtitle update complete.")

