-- Создание таблицы Исполнители (Artists)
CREATE TABLE IF NOT EXISTS Artists (
    artist_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Создание таблицы Жанры (Genres)
CREATE TABLE IF NOT EXISTS Genres (
    genre_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

-- Создание таблицы Альбомы (Albums)
CREATE TABLE IF NOT EXISTS Albums (
    album_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    release_year INTEGER NOT NULL
);

-- Создание таблицы Треки (Tracks)
CREATE TABLE IF NOT EXISTS Tracks (
    track_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    duration INTEGER NOT NULL,
    album_id INTEGER NOT NULL REFERENCES Albums(album_id)
);

-- Создание таблицы Сборники (Collections)
CREATE TABLE IF NOT EXISTS Collections (
    collection_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    release_year INTEGER NOT NULL
);

-- Создание промежуточной таблицы для связи Исполнители-Жанры
CREATE TABLE IF NOT EXISTS ArtistGenre (
    artist_id INTEGER NOT NULL REFERENCES Artists(artist_id),
    genre_id INTEGER NOT NULL REFERENCES Genres(genre_id),
    PRIMARY KEY (artist_id, genre_id)
);

-- Создание промежуточной таблицы для связи Исполнители-Альбомы
CREATE TABLE IF NOT EXISTS ArtistAlbum (
    artist_id INTEGER NOT NULL REFERENCES Artists(artist_id),
    album_id INTEGER NOT NULL REFERENCES Albums(album_id),
    PRIMARY KEY (artist_id, album_id)
);

-- Создание промежуточной таблицы для связи Сборники-Треки
CREATE TABLE IF NOT EXISTS CollectionTrack (
    collection_id INTEGER NOT NULL REFERENCES Collections(collection_id),
    track_id INTEGER NOT NULL REFERENCES Tracks(track_id),
    PRIMARY KEY (collection_id, track_id)
);