from loader import load_spotify_jsons
import arrow

df = load_spotify_jsons()

# Convert time using arrow 
df['played_at'] = df['ts'].apply(lambda t: arrow.get(t).datetime)

# Sorting df to reduce processing time for time-based operations
sorted_df = df.sort_values(by="played_at")


### Unique stats

# Get song list with playcount, time listened, ordered by playcount
def get_unique_songs():
    
    song_stats = df.groupby(["master_metadata_track_name", "master_metadata_album_artist_name"]).agg(
        count=("ms_played", lambda x: (x >= 30000).sum()), # Song not counting if not played for at least 30.000 ms
        total_ms_played=("ms_played", "sum")
    )
    song_stats["total_seconds_played"] = (song_stats["total_ms_played"] / 1000).round().astype(int)
    song_stats = song_stats.sort_values(by="count", ascending=False).reset_index()

    return song_stats

# Get artists list with playcount, time listened, ordered by playcount
def get_unique_artists():
    artists_df = df.groupby(["master_metadata_album_artist_name"]).agg(
        count=("ms_played", lambda x: (x >= 30000).sum()),
        total_ms_played=("ms_played", "sum")
    )
    artists_df["total_seconds_played"] = (artists_df["total_ms_played"] / 1000).round().astype(int)
    artists_df = artists_df.sort_values(by="count", ascending=False).reset_index()

    return artists_df