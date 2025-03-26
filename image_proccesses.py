import os
import shutil
from PIL import Image

from index import convert_filename_to_dotjpg, convert_webp_to_jpg, exists_jpg, get_webp_files

def filter_images_by_aspect_ratio(input_dir:str, output_dir:str, aspect_ratio:tuple[int,int], exclude_exts:list[str] = ['.webp'], log:bool = True) -> None:
    """
    Filters images by aspect ratio and copies the matching images to the output directory.

    input_dir: Path to the input directory containing images.
    output_dir: Path to the output directory to store filtered images.
    aspect_ratio (tuple): Target aspect ratio as (width, height).
    exclude_exts (list): List of file extensions to exclude from filtering.
    """
    valid_image_exts = ('.png', '.jpg', '.jpeg', '.webp', '.gif', '.tiff', '.bmp')

    copied = 0
    excluded = 0
    skipped = 0

    print(f"\n<{'>|Started Filtering Images|<':-^63}>")
    print(f"Copying from {input_dir} to {output_dir}")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        if log: print(f"{output_dir} created!")
    
    target_ratio = aspect_ratio[0] / aspect_ratio[1]

    for filename in os.listdir(input_dir):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)

        # Check if it's a image file
        if not os.path.isfile(input_path) or os.path.splitext(input_path)[1] not in valid_image_exts:
            if log: print(f"Skipped (not a image file): {filename}")
            continue

        if os.path.splitext(input_path)[1] in exclude_exts:
            excluded += 1
            if log: print(f"Skipped (excluded extension): {filename}")
            continue

        # Check if the file already exists in the output directory
        if os.path.exists(output_path):
            skipped += 1
            if log: print(f"Skipped (already exists in output directory): {filename}")
            continue

        with Image.open(input_path) as img:
            width, height = img.size
            img_ratio = width / height
            
            if abs(img_ratio - target_ratio) < 1e-2:  # Allowing a small tolerance
                try:
                    shutil.copy(input_path, output_dir)
                    copied += 1
                    if log: print(f"Copied: {filename}")
                except Exception as e:
                    skipped += 1
                    if log: print(f"Skipped: {filename}, Error: {e}")

    print(f"<{'':-^63}>")
    print(f"{ f'{skipped = }':^20} | {f'{excluded = }':^20} | {f'{copied = }':^20}")
    print(f"<{'':-^63}>")
    print(f"<{'>|Completed|<':-^63}>")


def delete_images(target_dir:str, file_names:list[str] = [], exts:list[str] = [], log:bool = True) -> None:
    print(f"\n<{'>|Started Deleting Images|<':-^63}>")
    print(f"Deleting images from {target_dir}")

    if not os.path.exists(target_dir):
        print(f"Target directory {target_dir} does not exist.")
        return
    
    removed = 0
    removed_file_names = 0
    removed_exts = 0

    for filename in file_names:
        file_path = os.path.join(target_dir, filename)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            try:
                os.remove(file_path)
                removed_file_names += 1
                if log: print(f"Removed: {file_path}")
            except Exception as e:
                if log: print(f"Error removing {file_path}: {e}")
    
    for filename in os.listdir(target_dir):
        file_path = os.path.join(target_dir, filename)
        if os.path.isfile(file_path) and os.path.splitext(file_path)[1] in exts:
            try:
                os.remove(file_path)
                removed_exts += 1
                if log: print(f"Removed: {file_path}")
            except Exception as e:
                if log: print(f"Error removing {file_path}: {e}")

    print(f"<{' Removed Summary ':-^63}>")
    print(f"{ f'{removed_file_names = }':^20} | {f'{removed_exts = }':^20} | {f'{removed = }':^20}")
    print(f"<{'':-^63}>")
    print(f"<{'>|Completed|<':-^63}>")

def convert_image(image_path: str, output_dir: str, output_img_ext: str = '.jpeg', log: bool = True) -> bool:
    """
    Convert a .webp image to .jpg with the same name.
    
    Parameters:
    webp_path (str): The path to the .webp image file.
    """
    try:
        # Open the .webp image
        img = Image.open(image_path)

        # Convert the image to RGB mode (JPEG does not support transparency)
        rgb_img = img.convert('RGB')

        # Get the base name (without extension) and change the extension to .jpeg
        base_name = os.path.basename(image_path)
        base_name = os.path.splitext(base_name)[0]
        output_file = os.path.join(output_dir, base_name) + output_img_ext

        # Save the image with the new extension
        rgb_img.save(output_file, 'JPEG')

        if log: print(f"Image converted and saved as {output_file}")
        return True
    except Exception as e:
        if log: print(f"Error converting image: {e}")
        return False

def copy_images(input_dir:str, output_dir:str, exts:list[str] = ['.png', '.jpg', '.jpeg', '.webp'], convert_exts:list[str] = ['.webp'], convert_to:str = '.jpeg', log:bool = True) -> None:
    print(f"\n<{'>|Started Copying Images|<':-^60}>")
    print(f"Copying from {input_dir} to {output_dir}")
    copied = 0
    skipped = 0

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        if log: print(f"{output_dir} created!")
    
    for filename in os.listdir(input_dir):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)

        # Check if it's a image file
        if not os.path.isfile(input_path) or os.path.splitext(input_path)[1] not in exts:
            if log: print(f"Skipped (not a valid image file): {filename}")
            continue

        # Check if the file already exists in the output directory
        if os.path.exists(output_path):
            skipped += 1
            if log: print(f"Skipped (already exists in output directory): {filename}")
            continue
        
        if os.path.splitext(input_path)[1] in convert_exts:
            if convert_image(input_path, output_dir, convert_to, log):
                copied += 1
                if log: print(f"Copied: {filename}")
        else:
            with Image.open(input_path) as img:
                try:
                    shutil.copy(input_path, output_dir)
                    copied += 1
                    if log: print(f"Copied: {filename}")
                except Exception as e:
                    skipped += 1
                    if log: print(f"Skipped: {filename}, Error: {e}")

    print(f"<{'':-^60}>")
    print(f"{f'{skipped = }':^30} | {f'{copied = }':^30}")
    print(f"<{'':-^60}>")
    print(f"<{'>|Completed|<':-^60}>")


def main() -> None:
    wallpaper = "D:/games/WallPaper"
    wallpaper_mobile = "D:/games/WallPaper/mobile"
    wallpaper_mihoyo = "D:/games/WallPaper/MiHoYo"
    wallpaper_output = "D:/projects/Genshin_BG_Downloader/output"
    wallpaper_16_9 = "D:/games/WallPaper/wallpaper_16_9"
    mobile_wallpaper_theme = "D:/games/WallPaper/mobile_mihoyo_processed"

    filter_images_by_aspect_ratio(wallpaper_output, wallpaper_mihoyo, (16, 9), log=False)
    filter_images_by_aspect_ratio(wallpaper_mihoyo, wallpaper_16_9, (16, 9), log=False)
    filter_images_by_aspect_ratio(wallpaper, wallpaper_16_9, (16, 9), log=False)

    for webp in get_webp_files(wallpaper_16_9):
        if not exists_jpg(convert_filename_to_dotjpg(webp)):
            convert_webp_to_jpg(webp)

    delete_images(wallpaper_16_9, exts=['.webp'])

    # copy_images(wallpaper_mobile, mobile_wallpaper_theme, log=False)

if __name__ == "__main__":
    main()

