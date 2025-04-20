import json
from collections import defaultdict
import os
import time

def load_playtimes():
    if os.path.exists("song_playtimes.json"):
        with open("song_playtimes.json", "r", encoding='utf-8') as f:
            song_playtimes = defaultdict(int, json.load(f))
        return song_playtimes
    else:
        return defaultdict(int)

def generate_wrapped_report():
    song_playtimes = load_playtimes()

    sorted_songs = sorted(song_playtimes.items(), key=lambda x: x[1], reverse=True)
    top_songs = sorted_songs[:10]

    with open("wrapped_report.txt", "w", encoding='utf-8') as f:
        f.write("Your Top 10 Songs:\n")
        for i, (song, duration) in enumerate(top_songs, 1):
            f.write(f"{i}. {song} - {duration // 60} Minuten\n")

        total_playtime = sum(song_playtimes.values())
        total_minutes = total_playtime // 60
        total_hours = total_minutes // 60

        f.write("\nTotal Playtime:\n")
        f.write(f"{total_hours} hours and {total_minutes % 60} minutes\n")

        f.write("\nSongs Played Less Than 5 Minutes (Top 5):\n")
        less_than_5_minutes = [(song, duration) for song, duration in song_playtimes.items() if duration < 300]
        top_5_less_than_5_minutes = sorted(less_than_5_minutes, key=lambda x: x[1], reverse=True)[:5]
        for song, duration in top_5_less_than_5_minutes:
            f.write(f"- {song} ({duration // 60} Minuten)\n")

        least_played_songs = sorted_songs[-5:]
        f.write("\nYour Least Played 5 Songs:\n")
        for i, (song, duration) in enumerate(reversed(least_played_songs), 1):
            f.write(f"{i}. {song} - {duration // 60} Minuten\n")

        unique_songs_count = len(song_playtimes)
        f.write("\nUnique Songs Played:\n")
        f.write(f"{unique_songs_count} unique songs\n")

if __name__ == "__main__":
    generate_wrapped_report()
print("Finished! with your Wrapped")
