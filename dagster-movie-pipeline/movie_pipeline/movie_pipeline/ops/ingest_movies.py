import pandas as pd
import ast
from sqlalchemy import create_engine
from dagster import op, get_dagster_logger
import os
from dotenv import load_dotenv

load_dotenv()  # Load DATABASE_URL from .env

@op
def ingest_movies():
    logger = get_dagster_logger()

    # Load dataset
    df = pd.read_csv("movies_metadata.csv", low_memory=False)
    logger.info(f"Loaded {len(df)} rows from CSV")

    # Clean and filter
    df = df[["id", "title", "release_date", "vote_average", "vote_count", "genres"]]
    df = df[df["id"].apply(lambda x: str(x).isdigit())]  # Keep only numeric IDs
    df["id"] = df["id"].astype(str)

    # Parse genres
    genre_map = {}
    movie_genres = []

    for _, row in df.iterrows():
        movie_id = row["id"]
        try:
            genres = ast.literal_eval(row["genres"])
            for genre in genres:
                gid, name = genre["id"], genre["name"]
                genre_map[gid] = name
                movie_genres.append((movie_id, gid))
        except (ValueError, SyntaxError):
            continue

    # Build genre and movie DataFrames
    genre_df = pd.DataFrame(list(genre_map.items()), columns=["id", "name"])
    movie_df = df[["id", "title", "release_date", "vote_average", "vote_count"]].copy()
    movie_genre_df = pd.DataFrame(movie_genres, columns=["movie_id", "genre_id"])

    # Connect to Postgres
    engine = create_engine(os.getenv("DATABASE_URL"))

    genre_df.to_sql("genres", engine, if_exists="append", index=False)
    movie_df.to_sql("movies", engine, if_exists="append", index=False)
    movie_genre_df.to_sql("movie_genres", engine, if_exists="append", index=False)

    logger.info("Ingested data into Postgres")
