from loader import load_spotify_jsons
import arrow

df = load_spotify_jsons()

# Convert time using arrow 
df['played_at'] = df['ts'].apply(lambda t: arrow.get(t).datetime)

# Sorting df to reduce processing time for time-based operations
sorted_df = df.sort_values(by="played_at")


### Getters + filters

# Get dataframe
def get_raw_df():
    return df

# Get sorted dataframe
def get_df():
    return sorted_df

# Filter df by year, month or/and day
def filter_by_date(dfParam, yearParam: int = None, monthParam: int = None, dayParam: int = None):
    filtered_df = dfParam

    if yearParam is not None:
        filtered_df = filtered_df[filtered_df["played_at"].dt.year == yearParam]

    if monthParam is not None:
        filtered_df = filtered_df[filtered_df["played_at"].dt.month == monthParam]
        
    if dayParam is not None:
        filtered_df = filtered_df[filtered_df["played_at"].dt.day == dayParam]

    return filtered_df.reset_index(drop=True)

# Filter df between two dates
def filter_by_date_interval(dfParam, startDateParam: str = None, endDateParam: str = None):
    df_to_filter = dfParam
    if startDateParam is not None:
        startDate = arrow.get(startDateParam)
    else:
        startDate = arrow.get("1975-01-01")

    if endDateParam is not None:
        endDate = arrow.get(endDateParam)
    else:
        endDate = arrow.get(arrow.utcnow())

    filtered_df = df_to_filter[(df_to_filter["played_at"] >= startDate.datetime) &
                            (df_to_filter["played_at"] < endDate.datetime)]

    return filtered_df.reset_index(drop=True)

# Filter df with artist
def filter_by_artist(dfParam, artistParam: str):
    return dfParam[dfParam["master_metadata_album_artist_name"] == artistParam]

# Filter df with album
def filter_by_album(dfParam, albumParam: str):
    return dfParam[dfParam["master_metadata_album_album_name"] == albumParam]


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

# Get albums list with playcount, time listened, ordered by playcount
def get_unique_albums(dfParam):
    album_df = dfParam.groupby(["master_metadata_album_album_name"]).agg(
        count=("ms_played", lambda x: (x >= 30000).sum()),
        total_ms_played=("ms_played", "sum")
    )
    album_df["total_seconds_played"] = (album_df["total_ms_played"] / 1000).round().astype(int)
    album_df = album_df.sort_values(by="count", ascending=False).reset_index()

    return album_df

# Get playcount by hours
def get_playcount_by_hours(dfParam):
    dfParam["hour"] = dfParam["played_at"].dt.hour

    songs_per_hour = dfParam[dfParam["ms_played"] >= 30000].groupby("hour").size().reset_index(name="playcount")

    return songs_per_hour




# Get playcount by calendar day
def get_playcount_by_calendar_day(dfParam):
    dfParam["date"] = dfParam["played_at"].dt.date

    playcount_per_calendar_day = dfParam.groupby(["date"]).agg(
        count=("ms_played", lambda x: (x >= 30000).sum()),
        total_ms_played=("ms_played", "sum")
    )
    playcount_per_calendar_day["total_seconds_played"] = (playcount_per_calendar_day["total_ms_played"] / 1000).round().astype(int)

    return playcount_per_calendar_day

# Get playcount by week
def get_playcount_by_week(dfParam):
    playcount_per_week = (
        dfParam.groupby(dfParam["played_at"].dt.to_period("W"))
        .agg(
            count=("ms_played", lambda x: (x >= 30000).sum()),
            total_ms_played=("ms_played", "sum")
        )
    )

    playcount_per_week["total_seconds_played"] = (
        (playcount_per_week["total_ms_played"] / 1000).round().astype(int)
    )

    return playcount_per_week

# Get playcount by month
def get_playcount_by_month(dfParam):
    playcount_per_month = (
        dfParam.groupby(dfParam["played_at"].dt.to_period("M"))
        .agg(
            count=("ms_played", lambda x: (x >= 30000).sum()),
            total_ms_played=("ms_played", "sum")
        )
    )

    playcount_per_month["total_seconds_played"] = (
        (playcount_per_month["total_ms_played"] / 1000).round().astype(int)
    )

    return playcount_per_month

# Get playcount by year
def get_playcount_by_year(dfParam):
    playcount_per_year = (
        dfParam.groupby(dfParam["played_at"].dt.to_period("Y"))
        .agg(
            count=("ms_played", lambda x: (x >= 30000).sum()),
            total_ms_played=("ms_played", "sum")
        )
    )

    playcount_per_year["total_seconds_played"] = (
        (playcount_per_year["total_ms_played"] / 1000).round().astype(int)
    )

    return playcount_per_year