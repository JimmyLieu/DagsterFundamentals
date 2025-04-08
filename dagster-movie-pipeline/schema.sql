CREATE TABLE genres (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE movies (
    id TEXT PRIMARY KEY,
    title TEXT,
    release_date DATE,
    vote_average FLOAT,
    vote_count INT
);

CREATE TABLE movie_genres (
    movie_id TEXT REFERENCES movies(id),
    genre_id INT REFERENCES genres(id),
    PRIMARY KEY (movie_id, genre_id)
);
