-- 1. Удаление данных и таблиц
-- Это необходимо для перезапуска скрипта с "чистого листа"
DROP TABLE IF EXISTS CollectionTrack;
DROP TABLE IF EXISTS ArtistAlbum;
DROP TABLE IF EXISTS ArtistGenre;
DROP TABLE IF EXISTS Tracks;
DROP TABLE IF EXISTS Collections;
DROP TABLE IF EXISTS Albums;
DROP TABLE IF EXISTS Artists;
DROP TABLE IF EXISTS Genres;

-- 2. Создание таблиц с учетом всех связей

-- Создание таблицы Исполнители
CREATE TABLE IF NOT EXISTS Artists (
    artist_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Создание таблицы Жанры
CREATE TABLE IF NOT EXISTS Genres (
    genre_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

-- Создание таблицы Альбомы
CREATE TABLE IF NOT EXISTS Albums (
    album_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    release_year INTEGER NOT NULL
);

-- Создание таблицы Треки
CREATE TABLE IF NOT EXISTS Tracks (
    track_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    duration INTEGER NOT NULL,
    album_id INTEGER NOT NULL REFERENCES Albums(album_id)
);

-- Создание таблицы Сборники
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

-- 3. Заполнение таблиц данными

-- Жанры
INSERT INTO genres (genre_id, name) VALUES
(1, 'Rock'),
(2, 'Pop'),
(3, 'Hip-Hop');

-- Исполнители
INSERT INTO artists (artist_id, name) VALUES
(1, 'Queen'),
(2, 'Adele'),
(3, 'Eminem'),
(4, 'BTS');

-- Связь исполнителей и жанров (many-to-many)
INSERT INTO ArtistGenre (artist_id, genre_id) VALUES
(1, 1), -- Queen - Rock
(2, 2), -- Adele - Pop
(3, 3), -- Eminem - Hip-Hop
(4, 2), -- BTS - Pop
(4, 3); -- BTS - Hip-Hop

-- Альбомы
INSERT INTO albums (album_id, title, release_year) VALUES
(1, 'Greatest Hits', 2019),
(2, '25', 2020),
(3, 'Revival', 2018);

-- Связь исполнителей и альбомов (many-to-many)
INSERT INTO ArtistAlbum (album_id, artist_id) VALUES
(1, 1), -- Queen
(2, 2), -- Adele
(3, 3); -- Eminem

-- Треки
INSERT INTO tracks (track_id, title, duration, album_id) VALUES
(1, 'Bohemian Rhapsody', 354, 1),
(2, 'Another One Bites the Dust', 215, 1),
(3, 'Hello', 295, 2),
(4, 'Someone Like You', 285, 2),
(5, 'Lose Yourself', 326, 3),
(6, 'My Name Is', 270, 3);

-- Сборники
INSERT INTO Collections (collection_id, title, release_year) VALUES
(1, 'Best of 2019', 2019),
(2, 'Love Songs', 2020),
(3, 'Hip-Hop Stars', 2018),
(4, 'Rock Legends', 2020);

-- Связь треков и сборников (many-to-many)
INSERT INTO CollectionTrack (collection_id, track_id) VALUES
(1, 3),
(1, 5),
(2, 4),
(2, 6),
(3, 5),
(3, 6),
(4, 1),
(4, 2);