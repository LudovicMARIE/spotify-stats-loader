from loader import load_spotify_jsons
import arrow

df = load_spotify_jsons()

# Convert time using arrow 
df['played_at'] = df['ts'].apply(lambda t: arrow.get(t).datetime)

# Sorting df to reduce processing time for time-based operations
sorted_df = df.sort_values(by="played_at")


# Filter df by year, month or/and day
def filter_by_date(yearParam: int = None, monthParam: int = None, dayParam: int = None):
    filtered_df = sorted_df

    if yearParam is not None:
        print("filtering year")
        filtered_df = filtered_df[filtered_df["played_at"].dt.year == yearParam]

    if monthParam is not None:
        print("filtering month")
        filtered_df = filtered_df[filtered_df["played_at"].dt.month == monthParam]
        
    if dayParam is not None:
        print("filtering day")
        filtered_df = filtered_df[filtered_df["played_at"].dt.day == dayParam]

    return filtered_df.reset_index(drop=True)

# Filter df between two dates
def filter_by_date_interval(startDateParam: str = None, endDateParam: str = None):
    if startDateParam is not None:
        startDate = arrow.get(startDateParam)
    else:
        startDate = arrow.get("1975-01-01")

    if endDateParam is not None:
        endDate = arrow.get(endDateParam)
    else:
        endDate = arrow.get(arrow.utcnow())

    filtered_df = sorted_df[(df["played_at"] >= startDate.datetime) &
                            (df["played_at"] < endDate.datetime)]

    return filtered_df.reset_index(drop=True)

### Unique stats and playcount

# Get song list with playcount, time listened, ordered by playcount
def get_unique_songs(dfParam):
    song_stats = dfParam.groupby(["master_metadata_track_name", "master_metadata_album_artist_name"]).agg(
        count=("ms_played", lambda x: (x >= 30000).sum()), # Song not counting if not played for at least 30.000 ms
        total_ms_played=("ms_played", "sum")
    )
    song_stats["total_seconds_played"] = (song_stats["total_ms_played"] / 1000).round().astype(int)
    song_stats = song_stats.sort_values(by="count", ascending=False).reset_index()

    return song_stats

# Get artists list with playcount, time listened, ordered by playcount
def get_unique_artists(dfParam):
    artists_df = dfParam.groupby(["master_metadata_album_artist_name"]).agg(
        count=("ms_played", lambda x: (x >= 30000).sum()),
        total_ms_played=("ms_played", "sum")
    )
    artists_df["total_seconds_played"] = (artists_df["total_ms_played"] / 1000).round().astype(int)
    artists_df = artists_df.sort_values(by="count", ascending=False).reset_index()

    return artists_df

# def get_unique_songs_by_artist():

