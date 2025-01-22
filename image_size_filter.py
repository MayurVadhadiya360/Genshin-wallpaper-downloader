import os
import shutil
from PIL import Image

def filter_images_by_aspect_ratio(input_dir:str, output_dir:str, aspect_ratio:tuple[int,int]):
    """
    Filters images by aspect ratio and copies the matching images to the output directory.

    input_dir: Path to the input directory containing images.
    output_dir: Path to the output directory to store filtered images.
    aspect_ratio (tuple): Target aspect ratio as (width, height).
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"{output_dir} created!")
    
    target_ratio = aspect_ratio[0] / aspect_ratio[1]

    for filename in os.listdir(input_dir):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)

        # Check if it's a file (not a directory)
        if not os.path.isfile(input_path):
            print(f"Skipped: {filename} (not a file)")
            continue

        # Check if the file already exists in the output directory
        if os.path.exists(output_path):
            print(f"Skipped: {filename} (already exists in output directory)")
            continue

        try:
            with Image.open(input_path) as img:
                width, height = img.size
                img_ratio = width / height
                
                if abs(img_ratio - target_ratio) < 1e-2:  # Allowing a small tolerance
                    shutil.copy(input_path, output_dir)
                    print(f"Copied: {filename}")
        except Exception as e:
            print(f"Skipped: {filename}, Error: {e}")
    print("<----------------->|Completed|<----------------->")

if __name__ == "__main__":
    wallpaper = "D:/games/WallPaper"
    wallpaper_mobile = "D:/games/WallPaper/mobile"
    wallpaper_mihoyo = "D:/games/WallPaper/MiHoYo"
    wallpaper_output = "D:/projects/Genshin_BG_Downloader/output"

    wallpaper_16_9 = "D:/games/WallPaper/wallpaper_16_9"

    filter_images_by_aspect_ratio(wallpaper_output, wallpaper_mihoyo, (16, 9))
    filter_images_by_aspect_ratio(wallpaper_mihoyo, wallpaper_16_9, (16, 9))
    filter_images_by_aspect_ratio(wallpaper, wallpaper_16_9, (16, 9))

