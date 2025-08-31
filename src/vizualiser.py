import matplotlib.pyplot as plt
from processor import *

def plot_songs_per_hour(dfParam):
    songs_per_hour_df = get_playcount_by_hours(dfParam)

    plt.figure(figsize=(10, 5))
    plt.bar(songs_per_hour_df["hour"], songs_per_hour_df["playcount"], color="skyblue", edgecolor="black")

    plt.title("Songs Listened per Hour of the Day")
    plt.xlabel("Hour of the Day (0-23)")
    plt.ylabel("Number of Songs Played")

    plt.xticks(range(0, 24))

    plt.grid(axis="y", linestyle="--", alpha=0.7)

    plt.tight_layout()
    plt.show()


def plot_playcount_per_calendar_day(dfParam):
    playcount_per_calendar_day_df = get_playcount_by_calendar_day(get_df())

    plt.figure(figsize=(12,5))
    plt.plot(playcount_per_calendar_day_df.index, 
             playcount_per_calendar_day_df["count"], 
             marker=".", 
             linestyle="-", 
             markersize=0)

    plt.title("Spotify Play Count per Day")
    plt.xlabel("Date")
    plt.ylabel("Play Count")
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    plt.show()

if __name__ == "__main__":
    df = get_df()
    # plot_songs_per_hour(df)
    plot_playcount_per_calendar_day(df)