import tkinter as tk
from tkinter import filedialog, Listbox
import os
from mutagen.mp3 import MP3
from yt_dlp import YoutubeDL
import random
from pypresence import Presence
import time
import pygame
import config
import json
from collections import defaultdict

# Pygame mixer init
pygame.mixer.init()

if not os.path.exists("config.py"):
    exit("config.py doesnt exists.")
else:
    print("Successfull")

by = config.by

# Global variables
playlist = []
current_index = 0
repeat_mode = False
is_playing = False
bgcolor = config.bgcolor
default_folder = config.default_folder
shuffle_mode = False
start_time = 0
rich_presence_enabled = config.default_discord_rich_presence
original_playlist = []
last_activity_time = time.time()
sjksaahd = by
record_actions = config.record_actions
error_message = config.error_message
show_repeat_shuffle = config.show_repeat_shuffle
playing_presence = config.playing_presence
paused_presence = config.paused_presence
idle_presence = config.idle_presence
hardcoded_presence = config.hardcoded_presence
hardcoded_icon_path = config.hardcoded_icon_path
hardcoded_root_title = config.hardcoded_root_title
default_discord_rich_presence = config.default_discord_rich_presence
hardcoded_geometry = config.hardcoded_geometry
hardcoded_resizeable = config.hardcoded_resizeable

only_custom_rpc = config.only_custom_rpc
custom_rpc_text = config.custom_rpc_text

playing_custom_text_behind = config.playing_custom_text_behind
paused_custom_text_behind = config.paused_custom_text_behind
idle_custom_text_behind = config.idle_custom_text_behind

CLIENT_ID = config.hardcoded_client_id
RPC = Presence(CLIENT_ID)
try:
    RPC.connect()
    print("Successfully connected with discord.")
except Exception as e:
    print(f"Error while connecting with discord: {e}")

# saves
song_playtimes = defaultdict(int)

if record_actions == True:
    print("Actions are getting Recorded!")

    def load_playtimes():
        global song_playtimes
        if os.path.exists("song_playtimes.json"):
            with open("song_playtimes.json", "r") as f:
                song_playtimes = defaultdict(int, json.load(f))

    def save_playtimes():
        with open("song_playtimes.json", "w") as f:
            json.dump(song_playtimes, f)
else:
    print("Actions are NOT getting Recorded!")

    def load_playtimes():
        pass

    def save_playtimes():
        pass

if default_discord_rich_presence == True:
    at_start_rich_button = "ON"
else:
    at_start_rich_button = "OFF"

def reconnect_rpc():
    global last_activity_time
    last_activity_time = time.time()
    try:
        RPC.connect()
        print("Successfully reconnected with Discord.")
    except Exception as e:
        print(f"Error while reconnecting with Discord: {e}")

if not os.path.exists(default_folder):
    os.makedirs(default_folder)

def load_songs():
    global playlist, original_playlist, last_activity_time
    last_activity_time = time.time()
    folder_path = filedialog.askdirectory(initialdir=default_folder)
    if folder_path:
        song_list.delete(0, tk.END)
        playlist = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith((".mp3", ".wav")):
                    full_path = os.path.join(root, file)
                    playlist.append(full_path)
                    song_list.insert(tk.END, file)
        original_playlist = list(playlist)

def delete_selected_song():
    global current_index, playlist, last_activity_time
    last_activity_time = time.time()
    current_selection = song_list.curselection()
    if current_selection:
        selected_index = current_selection[0]
        file_to_delete = playlist[selected_index]
        song_list.delete(selected_index)
        del playlist[selected_index]
        if os.path.exists(file_to_delete):
            os.remove(file_to_delete)
        if selected_index < current_index:
            current_index -= 1
        elif selected_index == current_index:
            stop_sound()
            if playlist:
                play_next_song()

def download_youtube_mp3():
    global last_activity_time
    last_activity_time = time.time()
    url = url_entry.get()
    if url:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(default_folder, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
            'ffmpeg_location': 'ffmpeg-7.1-essentials_build/bin/ffmpeg.exe'
        }
        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            load_songs()
        except Exception as e:
            print(f"Error during download or processing: {e}")

def track_playtime():
    global start_time
    if is_playing:
        current_song = os.path.basename(playlist[current_index])
        elapsed_time = int(time.time()) - start_time
        song_playtimes[current_song] += elapsed_time
        save_playtimes()
        start_time = int(time.time())
    root.after(1000, track_playtime)

def update_presence(song_name=None, start_time=0, duration=0):
    global last_activity_time
    if rich_presence_enabled:
        try:
            if song_name and is_playing:
                mode = []
                if show_repeat_shuffle == True:
                    if repeat_mode:
                        mode.append("Repeat")
                    if shuffle_mode:
                        mode.append("Shuffle")
                    mode_str = " & ".join(mode) if mode else ""
                else:
                    if repeat_mode:
                        mode.append("")
                    if shuffle_mode:
                        mode.append("")
                    mode_str = "".join(mode) if mode else ""

                max_details_length = 128
                # listning
                if only_custom_rpc == False:
                    details_message = f"{playing_presence}{song_name[:64]} ({mode_str}){hardcoded_presence}{playing_custom_text_behind}"
                    details_message = details_message[:max_details_length]
                else:
                    details_message = f"{custom_rpc_text}{hardcoded_presence}"
                    details_message = details_message[:max_details_length]
                elapsed_time = int(time.time()) - start_time

                if elapsed_time < duration:
                    RPC.update(
                        details=details_message,
                        start=start_time,
                        end=start_time + duration,
                        large_image="play.png",
                        large_text="MusiEz - tamino1230"
                    )
                else:
                    RPC.clear()
            elif song_name and not is_playing:
                # paused
                if only_custom_rpc == False:
                    details_message = f"{paused_presence}{song_name[:64]}{hardcoded_presence}{paused_custom_text_behind}"
                else:
                    details_message = f"{custom_rpc_text}{hardcoded_presence}"
                RPC.update(
                    details=details_message,
                    large_image="paused.png",
                    large_text="MusiEz - tamino1230"
                )
            elif (time.time() - last_activity_time) >= 900:
                RPC.update(
                    # idling
                    details=f"{idle_presence}{hardcoded_presence}{idle_custom_text_behind}",
                    large_image="musi_ez_large_image",
                    large_text="MusiEz - tamino1230"
                )
            else:
                RPC.clear()
        except Exception as e:
            pass
    else:
        RPC.clear()

def play_sound():
    global is_playing, start_time, last_activity_time
    last_activity_time = time.time()
    if playlist:
        pygame.mixer.music.load(playlist[current_index])
        pygame.mixer.music.play(loops=0)
        song_length = get_song_length(playlist[current_index])
        time_slider.config(to=song_length)
        is_playing = True
        update_song_info()

        song_name = os.path.basename(playlist[current_index])
        start_time = int(time.time())

        update_presence(song_name, start_time, song_length)

        # loads spy
        load_playtimes()

        # starts spy
        root.after(1000, track_playtime)

def play_selected_song(event):
    global current_index, is_playing, start_time, last_activity_time
    last_activity_time = time.time()
    if playlist:
        current_selection = song_list.curselection()
        if current_selection:
            current_index = current_selection[0]
            play_sound()

def pause_sound():
    global is_playing, start_time, last_activity_time
    last_activity_time = time.time()
    if is_playing:
        current_song = os.path.basename(playlist[current_index])
        elapsed_time = int(time.time()) - start_time
        song_playtimes[current_song] += elapsed_time
        save_playtimes()
        
    pygame.mixer.music.pause()
    is_playing = False
    update_presence(os.path.basename(playlist[current_index]))

def unpause_sound():
    global is_playing, start_time, last_activity_time
    last_activity_time = time.time()
    if not is_playing:
        pygame.mixer.music.unpause()
        is_playing = True
        song_name = os.path.basename(playlist[current_index])
        song_length = get_song_length(playlist[current_index])
        elapsed_time = int(time.time()) - start_time
        start_time = int(time.time()) - elapsed_time
        update_presence(song_name, start_time, song_length - elapsed_time)

def stop_sound():
    global is_playing, last_activity_time
    last_activity_time = time.time()
    pygame.mixer.music.stop()
    is_playing = False
    time_slider.set(0)
    update_presence()

def skip_forward():
    global current_index, last_activity_time
    last_activity_time = time.time()
    if playlist:
        current_index = (current_index + 1) % len(playlist)
        play_sound()

def skip_backwards():
    global current_index, last_activity_time
    last_activity_time = time.time()
    if playlist:
        current_index = (current_index - 1) % len(playlist)
        if current_index < 0:
            current_index = len(playlist) - 1
        play_sound()

def set_volume(val):
    global last_activity_time
    last_activity_time = time.time()
    volume = float(val) / 100
    pygame.mixer.music.set_volume(volume)

def toggle_repeat():
    global repeat_mode, last_activity_time
    last_activity_time = time.time()
    repeat_mode = not repeat_mode
    repeat_button.config(text="Repeat: ON" if repeat_mode else "Repeat: OFF")

def toggle_shuffle():
    global shuffle_mode, playlist, original_playlist, last_activity_time
    last_activity_time = time.time()
    shuffle_mode = not shuffle_mode
    shuffle_button.config(text="Shuffle: ON" if shuffle_mode else "Shuffle: OFF")
    if shuffle_mode:
        random.shuffle(playlist)
    else:
        playlist = list(original_playlist)
        song_list.delete(0, tk.END)
        for file in playlist:
                    song_list.insert(tk.END, os.path.basename(file))

def toggle_rich_presence():
    global rich_presence_enabled, last_activity_time
    last_activity_time = time.time()
    rich_presence_enabled = not rich_presence_enabled
    rich_presence_button.config(text="Rich Presence: ON" if rich_presence_enabled else "Rich Presence: OFF")
    if not rich_presence_enabled:
        RPC.clear()

def play_next_song():
    global current_index, is_playing, start_time, last_activity_time
    last_activity_time = time.time()
    is_playing = False
    if playlist:
        if repeat_mode:
            play_sound()
        else:
            current_index = (current_index + 1) % len(playlist)
            play_sound()

def jump_to_position(val):
    global last_activity_time
    last_activity_time = time.time()
    if playlist:
        new_time = int(val)
        pygame.mixer.music.rewind()
        pygame.mixer.music.set_pos(new_time)
        if new_time >= time_slider.cget("to"):
            play_next_song()

def update_song_info():
    if playlist:
        current_file = os.path.basename(playlist[current_index])
        song_name_label.config(text=current_file)

def get_song_length(song_path):
    try:
        audio = MP3(song_path)
        return int(audio.info.length)
    except Exception as e:
        print(f"Error retrieving song length: {e}")
        return 0

def check_song_end():
    global is_playing, start_time
    if is_playing and not pygame.mixer.music.get_busy():
        play_next_song()
    else:
        if is_playing:
            current_song = os.path.basename(playlist[current_index])
            song_length = get_song_length(playlist[current_index])
            elapsed_time = int(time.time()) - start_time
            update_presence(current_song, start_time, song_length - elapsed_time)
        elif (time.time() - last_activity_time) >= 900:
            update_presence()
    root.after(1000, check_song_end)

def periodic_update():
    global start_time
    if is_playing:
        current_song = os.path.basename(playlist[current_index])
        song_length = get_song_length(playlist[current_index])
        elapsed_time = int(time.time()) - start_time
        update_presence(current_song, start_time, song_length - elapsed_time)
    root.after(15000, periodic_update)

def checker(check, text, custom_error_message):
    if not check == text:
        exit(f"Not Sucessfull: {custom_error_message}")
    else:
        print("Successfull")

# Main window
root = tk.Tk()
root.title(hardcoded_root_title)
root.geometry(hardcoded_geometry)
root.configure(bg=bgcolor)
root.iconbitmap(hardcoded_icon_path)
root.resizable(hardcoded_resizeable, hardcoded_resizeable)

checker(hardcoded_resizeable, False, f"Wrong Resizeable is on {hardcoded_resizeable} and not on \"True\"")
checker(hardcoded_geometry, "800x600", "Wrong Geometry in Config.py")
checker(hardcoded_root_title, "MusiEz - @tamino1230", "Wrong RootTitle in Config.py")
checker(hardcoded_icon_path, "icon/babToma.ico", "Wrong Icon Path in config.py file")
checker(sjksaahd, "Tamino1230", "Wrong Owner in Config.py File")
checker(hardcoded_presence, " | made by tamino1230 on GitHub <3", "Wrong hardcoded Presence in Config.py File")
checker(CLIENT_ID, "1309941984407977996", "Wrong client-id in config.py")

# Rich Presence and Reconnect Buttons
button_frame = tk.Frame(root)
button_frame.pack(anchor="nw", pady=10)

rich_presence_button = tk.Button(button_frame, text=f"Rich Presence: {at_start_rich_button}", command=toggle_rich_presence)
rich_presence_button.pack(side=tk.LEFT, padx=5)

reconnect_button = tk.Button(button_frame, text="Reconnect", command=reconnect_rpc)
reconnect_button.pack(side=tk.LEFT, padx=5)

# Load Songs Button
load_button = tk.Button(root, text="Load Songs", command=load_songs)
load_button.pack(pady=10)

# Song List
song_list = Listbox(root)
song_list.pack(pady=10, fill=tk.BOTH, expand=True)
song_list.bind("<Double-1>", play_selected_song)

# Controls Frame
controls_frame = tk.Frame(root)
controls_frame.pack(pady=10)

# Control Buttons
pause_button = tk.Button(controls_frame, text="Pause", command=pause_sound)
pause_button.grid(row=0, column=1, padx=5)

unpause_button = tk.Button(controls_frame, text="Unpause", command=unpause_sound)
unpause_button.grid(row=0, column=2, padx=5)

stop_button = tk.Button(controls_frame, text="Stop", command=stop_sound)
stop_button.grid(row=0, column=3, padx=5)

skip_backwards_button = tk.Button(controls_frame, text="Back", command=skip_backwards)
skip_backwards_button.grid(row=0, column=4, padx=5)

skip_forward_button = tk.Button(controls_frame, text="Next", command=skip_forward)
skip_forward_button.grid(row=0, column=5, padx=5)

repeat_button = tk.Button(controls_frame, text="Repeat: OFF", command=toggle_repeat)
repeat_button.grid(row=0, column=6, padx=5)

shuffle_button = tk.Button(controls_frame, text="Shuffle: OFF", command=toggle_shuffle)
shuffle_button.grid(row=0, column=7, padx=5)

# Volume Frame
volume_frame = tk.Frame(root)
volume_frame.pack(pady=10, anchor="w")

volume_label = tk.Label(volume_frame, text="Volume")
volume_label.pack(side=tk.LEFT, padx=5)

volume_slider = tk.Scale(volume_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=set_volume)
volume_slider.set(50)
volume_slider.pack(side=tk.LEFT, padx=5)

# Time Slider
time_frame = tk.Frame(root)
time_frame.pack(pady=10)

time_slider = tk.Scale(time_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=jump_to_position)
time_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

# Song Name Label
song_name_label = tk.Label(root, text="No Song Loaded", font=("Helvetica", 14))
song_name_label.pack(pady=10)

# URL Entry
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=10)

# Download Button
download_button = tk.Button(root, text="Download MP3", command=download_youtube_mp3)
download_button.pack(pady=10)

print("YOU CAN HIDE THIS WINDOW.")

# Check if song ends
check_song_end()

# Start periodic update
periodic_update()

# load times when started
load_playtimes()

# Mainloop
root.mainloop()
