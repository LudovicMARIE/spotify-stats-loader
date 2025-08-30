import matplotlib.pyplot as plt
from processor import *

def plot_songs_per_hour(dfParam):
    songs_per_hour_df = get_playcount_by_hours(dfParam)

    plt.figure(figsize=(10, 5))
    plt.bar(songs_per_hour_df["hour"], songs_per_hour_df["playcount"], color="skyblue", edgecolor="black")

    plt.title("Songs Listened per Hour of the Day")
    plt.xlabel("Hour of the Day (0–23)")
    plt.ylabel("Number of Songs Played")

    # Make x-axis nicer (show 0-23 clearly)
    plt.xticks(range(0, 24))

    plt.grid(axis="y", linestyle="--", alpha=0.7)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    df = get_df()
    plot_songs_per_hour(df)