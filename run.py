import sys
import os
from hoyo_daily_post import select_daily_post
from image_proccesses import (
    process_wallpapers_16_9,
    classify_mobile_wallpapers,
    copy_mobile_wallpapers,
    delete_excluded_wallpapers
)
from index import (
    run_download_wallpapers,
    run_get_hoyo_launcher_bg
)

def menu():
    print("\n=== Genshin BG Downloader Task Runner ===")
    print("Select a task:")
    print("1. Select daily post (random wallpaper)")
    print("2. Process wallpapers for 16:9 aspect ratio")
    print("3. Classify mobile wallpapers (landscape/portrait)")
    print("4. Copy mobile portrait wallpapers to theme directory")
    print("5. Delete excluded wallpapers")
    print("6. Download wallpapers (API)")
    print("7. Download Hoyoverse launcher backgrounds")
    print("0. Exit")
    choice = input("Enter choice: ")
    return choice

def prompt_dir(default):
    val = input(f"Enter directory [{default}]: ")
    return val.strip() or default

def main():
    while True:
        choice = menu()
        if choice == '1':
            select_daily_post()
        elif choice == '2':
            wallpaper_output = prompt_dir("D:/projects/Genshin_BG_Downloader/output")
            wallpaper_mihoyo = prompt_dir("D:/games/WallPaper/MiHoYo")
            wallpaper_16_9 = prompt_dir("D:/games/WallPaper/wallpaper_16_9")
            wallpaper = prompt_dir("D:/games/WallPaper")
            process_wallpapers_16_9(wallpaper_output, wallpaper_mihoyo, wallpaper_16_9, wallpaper)
        elif choice == '3':
            wallpaper_mobile = prompt_dir("D:/games/WallPaper/mobile")
            wallpaper_mobile_l = prompt_dir("D:/games/WallPaper/mobile_l")
            wallpaper_mobile_p = prompt_dir("D:/games/WallPaper/mobile_p")
            classify_mobile_wallpapers(wallpaper_mobile, wallpaper_mobile_l, wallpaper_mobile_p)
        elif choice == '4':
            wallpaper_mobile_p = prompt_dir("D:/games/WallPaper/mobile_p")
            mobile_wallpaper_theme = prompt_dir("D:/games/WallPaper/mobile_mihoyo_processed")
            copy_mobile_wallpapers(wallpaper_mobile_p, mobile_wallpaper_theme)
        elif choice == '5':
            wallpaper_mihoyo = prompt_dir("D:/games/WallPaper/MiHoYo")
            delete_excluded_wallpapers(wallpaper_mihoyo)
        elif choice == '6':
            count = input("Enter number of wallpapers to download [10]: ")
            try:
                count = int(count) if count else 10
            except ValueError:
                count = 10
            res_w = input("Enter resolution width [2560]: ")
            res_h = input("Enter resolution height [1440]: ")
            try:
                res_w = int(res_w) if res_w else 2560
                res_h = int(res_h) if res_h else 1440
            except ValueError:
                res_w, res_h = 2560, 1440
            run_download_wallpapers(count, [res_w, res_h])
        elif choice == '7':
            run_get_hoyo_launcher_bg()
        elif choice == '0':
            print("Exiting.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
