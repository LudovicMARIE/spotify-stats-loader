from loader import load_spotify_jsons
import arrow

df = load_spotify_jsons()

# Convert time using arrow 
df['played_at'] = df['ts'].apply(lambda t: arrow.get(t).datetime)
df['minutes_played'] = df['ms_played'] / 60000

print(df.count())