from processor import *


# filtered_by_date_df = filter_by_date(2025, 6, 1)
# print(filtered_by_date_df)

# filtered_by_date_interval_default_df = filter_by_date_interval()
# print(filtered_by_date_interval_default_df)

# filtered_by_date_interval_df = filter_by_date_interval("2024-05-06", None)
# print(filtered_by_date_interval_df)


# unique_songs_df = get_unique_songs(get_df())
# print(unique_songs_df)


# unique_artists_df = get_unique_artists(get_df())
# print(unique_artists_df)

# unique_albums_df = get_unique_albums(get_df())
# print(unique_albums_df)


# unique_last_dinos_songs = get_unique_songs(filter_by_artist(get_df(), "Last Dinosaurs"))
# print(unique_last_dinos_songs)

# unique_albums_last_dinos = get_unique_albums(filter_by_artist(get_df(), "Last Dinosaurs"))
# print(unique_albums_last_dinos)


# songs_per_hour = get_playcount_by_hours(get_df())
# print(songs_per_hour)

test = get_playcount_by_calendar_day(get_df())
print(test)