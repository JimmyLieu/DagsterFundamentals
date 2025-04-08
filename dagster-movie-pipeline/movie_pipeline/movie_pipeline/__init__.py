from dagster import job
from movie_pipeline.ops.ingest_movies import ingest_movies

@job
def ingest_movies_job():
    ingest_movies()

