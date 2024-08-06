import os
import instaloader
from datetime import datetime

def download_instagram_media(post_url):
    L = instaloader.Instaloader()

    # Create downloads directory if it doesn't exist
    download_dir = 'downloads'
    os.makedirs(download_dir, exist_ok=True)

    shortcode = post_url.split("/")[-2]
    post = instaloader.Post.from_shortcode(L.context, shortcode)

    # Check if the post is a video or an image
    if post.is_video:
        print("Downloading video...")
        video_dir = os.path.join(download_dir, 'mp4')
        os.makedirs(video_dir, exist_ok=True)  # Create video directory if it doesn't exist
        L.download_post(post, target=video_dir)
    else:
        print("Downloading image...")
        image_dir = os.path.join(download_dir, 'jpg')
        os.makedirs(image_dir, exist_ok=True)  # Create image directory if it doesn't exist
        
        # Use the post's image URL to download the image
        image_url = post.url  # Get the URL of the image
        image_filename = os.path.join(image_dir, f"{post.owner_username}.jpg")
        
        # Download the image using the URL
        L.download_pic(image_filename, image_url, mtime=datetime.now())
        
        rename_jpg_files(image_dir)
        
def rename_jpg_files(directory):
    # Iterate through all files in the specified directory
    for filename in os.listdir(directory):
        if filename.endswith('.jpg.jpg'):
            # Create the new filename by removing the extra .jpg
            new_filename = filename[:-4]  # Remove the last 4 characters (.jpg)
            # Rename the file
            os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))
            print(f'\nRenamed: {filename} to {new_filename}\n')

        
# Example usage
post_url = 'https://www.instagram.com/reel/C9NfWKIPPHg/?utm_source=ig_web_copy_link'
download_instagram_media(post_url)
