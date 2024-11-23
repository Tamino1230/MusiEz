import pygame
import tkinter as tk
from tkinter import filedialog, Listbox
import os
from mutagen.mp3 import MP3
from yt_dlp import YoutubeDL
import random

# pygame mixer init
pygame.mixer.init()

by = "tamino1230"

# global variables
playlist = []
current_index = 0
repeat_mode = False
is_playing = False
default_folder = "downloaded_music"
shuffle_mode = False

if not os.path.exists(default_folder):
    os.makedirs(default_folder)

def load_songs():
    global playlist
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

def delete_selected_song():
    global current_index, playlist
    current_selection = song_list.curselection()
    if current_selection:
        selected_index = current_selection[0]
        file_to_delete = playlist[selected_index]
        song_list.delete(selected_index)
        del playlist[selected_index]
        # delete
        if os.path.exists(file_to_delete):
            os.remove(file_to_delete)
        # update if wanted
        if selected_index < current_index:
            current_index -= 1
        elif selected_index == current_index:
            stop_sound()
            if playlist:
                play_next_song()
        
def download_youtube_mp3():
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
            'ffmpeg_location': 'ffmpeg-7.1-essentials_build/bin/ffmpeg.exe'  # ffmpeg path
        }
        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            load_songs()
        except Exception as e:
            print(f"Error during download or processing: {e}")

def play_sound():
    global is_playing
    if playlist:
        pygame.mixer.music.load(playlist[current_index])
        pygame.mixer.music.play(loops=0)
        song_length = get_song_length(playlist[current_index])
        time_slider.config(to=song_length)
        is_playing = True
        update_song_info()
        root.after(1000, check_song_end)

def play_selected_song(event):
    global current_index, is_playing
    if playlist:
        current_selection = song_list.curselection()
        if current_selection:
            current_index = current_selection[0]
        play_sound()

def pause_sound():
    global is_playing
    pygame.mixer.music.pause()
    is_playing = False

def unpause_sound():
    global is_playing
    pygame.mixer.music.unpause()
    is_playing = True

def stop_sound():
    global is_playing
    pygame.mixer.music.stop()
    is_playing = False
    time_slider.set(0)

def skip_forward():
    global current_index
    if playlist:
        current_index = (current_index + 1) % len(playlist)
        play_sound()

def skip_backwards():
    global current_index
    if playlist:
        current_index = (current_index - 1) % len(playlist)
        if current_index < 0:
            current_index = len(playlist) - 1
        play_sound()

def set_volume(val):
    volume = float(val) / 100
    pygame.mixer.music.set_volume(volume)

def toggle_repeat():
    global repeat_mode
    repeat_mode = not repeat_mode
    repeat_button.config(text="Repeat: ON" if repeat_mode else "Repeat: OFF")

def toggle_shuffle():
    global shuffle_mode
    shuffle_mode = not shuffle_mode
    shuffle_button.config(text="Shuffle: ON" if shuffle_mode else "Shuffle: OFF")
    if shuffle_mode:
        random.shuffle(playlist)

def play_next_song():
    global current_index, is_playing
    is_playing = False
    if playlist:
        if repeat_mode:
            play_sound()
        elif shuffle_mode:
            current_index = (current_index + 1) % len(playlist)
            play_sound()
        else:
            current_index = (current_index + 1) % len(playlist)
            play_sound()

def jump_to_position(val):
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
    global is_playing
    if is_playing and not pygame.mixer.music.get_busy():
        play_next_song()
    root.after(1000, check_song_end)

# mainn window
root = tk.Tk()
root.title("MusiEz - @tamino1230")
root.geometry("800x600")
root.configure(bg="#F791C1")
root.iconbitmap("babToma.ico")
root.resizable(False, False)

load_button = tk.Button(root, text="Load Songs", command=load_songs)
load_button.pack(pady=10)

# delete_button = tk.Button(root, text="Delete Selected Song", command=delete_selected_song)
# delete_button.pack(pady=10)

song_list = Listbox(root)
song_list.pack(pady=10, fill=tk.BOTH, expand=True)
song_list.bind("<Double-1>", play_selected_song)

controls_frame = tk.Frame(root)
controls_frame.pack(pady=10)

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

volume_frame = tk.Frame(root)
volume_frame.pack(pady=10, anchor="w")

volume_label = tk.Label(volume_frame, text="Volume")
volume_label.pack(side=tk.LEFT, padx=5)

volume_slider = tk.Scale(volume_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=set_volume)
volume_slider.set(50)
volume_slider.pack(side=tk.LEFT, padx=5)

time_frame = tk.Frame(root)
time_frame.pack(pady=10)

time_slider = tk.Scale(time_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=jump_to_position)
time_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

song_name_label = tk.Label(root, text="No Song Loaded", font=("Helvetica", 14))
song_name_label.pack(pady=10)

url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=10)

download_button = tk.Button(root, text="Download MP3", command=download_youtube_mp3)
download_button.pack(pady=10)

# check if song ends
check_song_end()

root.mainloop()
