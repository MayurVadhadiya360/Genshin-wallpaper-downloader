import json
import random
from index import read_img_download_history

def read_daily_post_history() -> list[str]:
    with open('daily_post_history.json', 'r') as f:
        data = json.load(f)
        image_urls = data.get("IMAGE_URLS", [])
    return image_urls

def update_daily_post_history(todays_url: str) -> None:
    with open('daily_post_history.json', 'r+') as f:
        data = json.load(f)

        image_urls: set[str] = set(data.get("IMAGE_URLS", []))
        image_urls.add(todays_url)
        data["IMAGE_URLS"] = list(image_urls)

        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

def read_excluded_image() -> list[str]:
    with open('image_exclusion.json', 'r') as f:
        data = json.load(f)
        image_urls = data.get("EXCLUDED_IMGS", [])
    return image_urls

def main():
    # Load download_history.json
    # Get the list of links
    links = read_img_download_history()
    if not links:
        print("No links found in download_history.json")
        return
    
    links_used = read_daily_post_history()
    link_names_excluded = read_excluded_image()
    links_excluded = list(map(lambda x: x + '.jpg', link_names_excluded)) + list(map(lambda x: x + '.webp', link_names_excluded))

    # Randomly select one link
    selected_link = random.choice(links)
    while selected_link in links_used or selected_link.split('/')[-1] in links_excluded:
        selected_link = random.choice(links)

    print(f"Today's wallpaper is: {selected_link}")

    confirm = input("Confirm today's wallpaper? y/n: ").lower()
    if confirm == 'y':
        # Save the selected link to post_history.json
        update_daily_post_history(selected_link)
        print("Saved!")

if __name__ == "__main__":
    main()
