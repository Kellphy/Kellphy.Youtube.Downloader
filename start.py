import yt_dlp
import json
import os

# Define the path for the stored data
data_file = 'download_info.json'

# Function to read the stored data for all playlists
def get_all_download_info():
    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            return json.load(f)
    return {"playlists": []}

# Function to get the last video ID for a specific playlist by ID
def get_last_video_id(playlist_id):
    data = get_all_download_info()
    for playlist in data["playlists"]:
        if playlist["id"] == playlist_id:
            return playlist.get("video_id")
    return None

# Function to set the last video ID for a specific playlist by ID
def set_last_video_id(playlist_id, video_id):
    data = get_all_download_info()
    # Find the playlist and update its last video ID
    for playlist in data["playlists"]:
        if playlist["id"] == playlist_id:
            playlist["video_id"] = video_id
            break
    else:
        # If the playlist isn't in the list, add it
        data["playlists"].append({"id": playlist_id, "video_id": video_id})
    
    with open(data_file, 'w') as f:
        json.dump(data, f, indent=4)

# Function to generate the playlist URL from the playlist ID
def generate_playlist_url(playlist_id):
    return f"https://www.youtube.com/playlist?list={playlist_id}"

# Function to download audio from videos in a playlist
def download_audio(playlist_id):
    playlist_url = generate_playlist_url(playlist_id)
    
    # Retrieve the last downloaded video ID for this playlist
    last_video_id = get_last_video_id(playlist_id)

    entries = []
    with yt_dlp.YoutubeDL({'extract_flat': True, "quiet": True}) as ydl:
        # Get the playlist info
        print(f"Getting playlist info ...")
        try:
            playlist_info = ydl.extract_info(playlist_url, download=False)
            entries_all = playlist_info.get('entries', [])
            
            # Loop through the videos in the playlist
            for entry in entries_all:
                video_id = entry['id']
                # Stop if the last video ID is reached
                if last_video_id and video_id == last_video_id:
                    print(f"All new videos up to [{video_id}] have been downloaded for playlist {playlist_url}.")
                    break
                entries.append(entry)
                
            entries.reverse()
        except Exception as e:
            print(f"Failed to extract playlist info for {playlist_url}: {e}")
            return

    new_videos_downloaded = False

    # Configure yt-dlp options for audio extraction in M4A format
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'outtmpl': './Downloads/%(channel)s - %(title)s.%(ext)s',
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }],
        'quiet': True
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print(f"Downloading {entries.count} videos ...")
        # Loop through the videos in the playlist
        for entry in entries:
            video_id = entry['id']
            video_title = entry['title']
            # Download the audio from the video
            print(f"Downloading audio for [{video_id}] {video_title} ...")
            try:
                ydl.download([entry['url']])
                new_videos_downloaded = True
                # Update the last downloaded video ID after each successful download
                set_last_video_id(playlist_id, video_id)
            except Exception as e:
                print(f"Failed to download [{video_id}] {video_title}: {e}")

    if not new_videos_downloaded:
        print(f"No new videos to download for playlist {playlist_url}.")

# Main execution block to process playlists from the download_info.json file
if __name__ == "__main__":
    download_info = get_all_download_info()
    playlists = download_info.get("playlists", [])

    if playlists:
        for playlist in playlists:
            playlist_id = playlist["id"]
            download_audio(playlist_id)
    else:
        print("No playlists found in download_info.json. Exiting.")
