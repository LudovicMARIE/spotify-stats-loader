import pandas as pd
import json
from pathlib import Path

def load_spotify_jsons(data_dir="../data"):
    files = Path(data_dir).glob("*.json")

    dfs = []

    # Loads files into list
    for f in files:
        with open(f, "r", encoding="utf-8") as infile:
            data = json.load(infile)
            dfs.append(pd.DataFrame(data))

    if not dfs:
        raise ValueError("No JSON files found in data folder.")


    # Merge all DataFrames
    df = pd.concat(dfs, ignore_index=True)
    print("File gathering finished")
    return df