import os
import json
import httpx
import traceback
from PIL import Image

BASE_DIR = os.path.dirname(__file__)

def get_img_name_from_url(img_url:str) -> str:
    url = img_url.split("/")
    return url[-1]

# Image download history
def read_img_download_history() -> list[str]:
    with open('download_history.json', 'r') as f:
        data = json.load(f)
        img_downloads = data.get("IMG_DOWNLOADS", [])
    return img_downloads

def update_img_download_history(img_downloads:list[str]) -> None:
    with open('download_history.json', 'r+') as f:
        data = json.load(f)

        old_img_urls: set[str] = set(data.get("IMG_DOWNLOADS", []))
        new_img_urls = set(img_downloads)
        all_img_urls = old_img_urls.union(new_img_urls)

        data["IMG_DOWNLOADS"] = list(all_img_urls)

        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

# Video download history
def read_vid_download_history() -> list[str]:
    with open('download_history.json', 'r') as f:
        data = json.load(f)
        vid_downloads = data.get("VID_DOWNLOADS", [])
    return vid_downloads

def update_vid_download_history(vid_downloads:list[str]) -> None:
    with open('download_history.json', 'r+') as f:
        data = json.load(f)

        old_vid_urls: set[str] = set(data.get("VID_DOWNLOADS", []))
        new_vid_urls = set(vid_downloads)
        all_vid_urls = old_vid_urls.union(new_vid_urls)

        data["VID_DOWNLOADS"] = list(all_vid_urls)

        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

# Image file methods
def get_webp_files(directory: str|None = None) -> list[str]:
    """
    Returns a list of all .webp file paths in the given directory.
    
    Parameters:
    directory (str): The path to the directory.
    """
    if not directory: directory = os.path.join(BASE_DIR, 'output')
    # List to store .webp file paths
    webp_files:list[str] = []
    
    # Loop through all files in the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if the file has a .webp extension
            if file.lower().endswith('.webp'):
                # Get the full path of the file and add it to the list
                webp_files.append(os.path.join(root, file))
    
    return webp_files

def convert_webp_to_jpg(webp_path: str) -> None:
    """
    Convert a .webp image to .jpg with the same name.
    
    Parameters:
    webp_path (str): The path to the .webp image file.
    """
    try:
        # Open the .webp image
        img = Image.open(webp_path)

        # Convert the image to RGB mode (JPEG does not support transparency)
        rgb_img = img.convert('RGB')

        # Get the base name (without extension) and change the extension to .jpeg
        output_file = os.path.splitext(webp_path)[0] + '.jpeg'

        # Save the image with the new extension
        rgb_img.save(output_file, 'JPEG')

        print(f"Image converted and saved as {output_file}")
    except Exception as e:
        print(f"Error: {e}")

def exists_jpg(webp_filename: str) -> bool:
    return os.path.isfile(webp_filename) and webp_filename.lower().endswith('.jpg')

def convert_filename_to_dotjpg(webp_filename:str) -> str:
    return os.path.splitext(webp_filename)[0] + '.jpg'

# Download images(wallpapers)
def download_img(img_url:str, output:str|None=None) -> bool:
    download_success = False
    if not output: output = os.path.join(BASE_DIR, 'output')
    img_downloads = read_img_download_history()
    if img_url not in img_downloads:
        img_name = get_img_name_from_url(img_url)
        with open(os.path.join(output, img_name), 'wb') as f:
            try:
                conn = httpx.get(img_url)
                f.write(conn.content)
                img_downloads.append(img_url)
                update_img_download_history(img_downloads)
                download_success = True
            except Exception as e:
                download_success = False
                traceback.print_exc()
    else:
        download_success = False
        print("Image already downloaded!")
    print("-----")
    return download_success

# Download video(live wallpaper)
def download_vid(vid_url:str, output:str|None=None) -> bool:
    download_success = False
    if not output: output = os.path.join(BASE_DIR, 'video')
    vid_downloads = read_vid_download_history()
    if vid_url not in vid_downloads:
        img_name = get_img_name_from_url(vid_url)
        with open(os.path.join(output, img_name), 'wb') as f:
            try:
                conn = httpx.get(vid_url)
                f.write(conn.content)
                vid_downloads.append(vid_url)
                update_vid_download_history(vid_downloads)
                download_success = True
            except Exception as e:
                download_success = False
                traceback.print_exc()
    else:
        download_success = False
        print("Video already downloaded!")
    print("-----")
    return download_success

def download_wallpapers(count:int, resolution:list[int, int]) -> None:
    """
    Downloads wallpaper images for genshin
    Parameters:
    count: Number of new images to download
    resolution: Resolution of the image [width, height]
    """
    url = "https://hk4e-api.mihoyo.com/event/contenthub/v1/wall_papers?page={page_number}&size=100&type={type}&lang=en-us"
    # url = "https://hk4e-api.mihoyo.com/event/contenthub/v1/wall_papers?page=1&size=100&type=0&lang=en-us"

    wallpaper_type_list = [
        {"type": "0", "name": "Patch Wallpapers"},
        {"type": "1", "name": "Event Wallpapers"},
        {"type": "2", "name": "Character Wallpapers"},
    ]

    hasMore = True
    download_count = 0
    page_number = 1
    while hasMore and download_count<count:
        try:
            this_url = url.format(page_number=page_number, type=0)
            response = httpx.get(this_url).json()
            response_data = response['data']
            hasMore = response_data.get('has_more')
            wallpaper_list = response_data['wallpapers']

            for wallpaper in wallpaper_list:
                print(f"Downloading {wallpaper.get('title')}...")

                wallpaper_pic_list = wallpaper.get("pic_list")
                for wallpaper_pic in wallpaper_pic_list:
                    if wallpaper_pic.get("width") == resolution[0] and wallpaper_pic.get("height") == resolution[1]:
                        wallpaper_pic_url = wallpaper_pic.get("url")
                        download_success = download_img(wallpaper_pic_url)
                        if download_success: download_count += 1
            page_number += 1
        except Exception as e:
            traceback.print_exc()
            hasMore = False

def get_hoyo_launcher_bg() -> None:
    url1 = "https://sg-hyp-api.hoyoverse.com/hyp/hyp-connect/api/getGames?launcher_id=VYTpXlbWo8&language=en-us"
    try:
        data = httpx.get(url1).json()
        data = data["data"]["games"]
        for game in data:
            background_url = game["display"]["background"]["url"]
            if background_url:
                print(f"Downloading BG from {game['display']['name']}...")
                download_img(background_url)
    except Exception as e:
        traceback.print_exc()

    url2 = "https://sg-hyp-api.hoyoverse.com/hyp/hyp-connect/api/getAllGameBasicInfo?launcher_id=VYTpXlbWo8&language=en-us"
    try:
        data = httpx.get(url2).json()
        data = data["data"]["game_info_list"]
        for game in data:
            background_list = game["backgrounds"]
            for bg in background_list:
                background_url = bg["background"]["url"]
                if background_url:
                    print(f"Downloading BG from gameid:{game['game']['id']} bgid:{bg['id']}...")
                    print(f"\tDownloading wallpaper: {background_url}")
                    download_img(background_url)

                vid_url = bg["video"]["url"]
                if vid_url:
                    print(f"Downloading BG from gameid:{game['game']['id']} bgid:{bg['id']}...")
                    print(f"\tDownloading video (live wallpaper): {vid_url}")
                    download_vid(vid_url)
    except Exception as e:
        traceback.print_exc()

def main() -> None:
    # print(BASE_DIR)``
    # 16:9 => 1920x1080, 2560x1440
    download_wallpapers(10, [2560, 1440])
    get_hoyo_launcher_bg()

    # for webp in get_webp_files():
    #     if not exists_jpg(convert_filename_to_dotjpg(webp)):
    #         convert_webp_to_jpg(webp)


if __name__ == "__main__":
    main()
