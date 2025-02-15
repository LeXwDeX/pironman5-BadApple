# 需要进入虚拟环境 source /opt/pironman5/venv/
import os
import time
from pm_auto.oled import OLED
from PIL import Image, ImageSequence

def process_gif(input_path, output_path, size=(128, 64)):
    """
    Process a GIF file to resize and convert it to 1-bit mode.

    Args:
        input_path (str): Path to the input GIF file.
        output_path (str): Path to save the processed GIF file.
        size (tuple): Target size (width, height) for the GIF.
    """
    frames = []

    # Open the input GIF
    with Image.open(input_path) as gif:
        for frame in ImageSequence.Iterator(gif):
            # Resize and convert each frame
            processed_frame = frame.convert("1").resize(size)
            frames.append(processed_frame)

        # Save the processed frames as a new GIF
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            loop=0,
            duration=gif.info.get("duration", 100),
        )
        print(f"Processed GIF saved to {output_path}")

def main():
    oled = OLED()
    if oled.is_ready():
        print("OLED is ready")

        input_gif = "/opt/pironman5/mgunnp.gif"
        output_gif = "/opt/pironman5/mgunnp_optimized.gif"

        # Check if the optimized GIF already exists
        if not os.path.exists(output_gif):
            print("Processing GIF...")
            process_gif(input_gif, output_gif)
        else:
            print("Optimized GIF already exists. Skipping processing.")

        # Display the optimized GIF
        with Image.open(output_gif) as gif:
            for frame in ImageSequence.Iterator(gif):
                oled.oled.image(frame.convert("1"))
                oled.oled.display()
    else:
        print("OLED is not ready")

if __name__ == "__main__":
    main()