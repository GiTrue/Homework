-- 1. Самый длинный трек
SELECT title, duration FROM tracks
ORDER BY duration DESC
LIMIT 1;

-- 2. Треки длиннее 3,5 минут (210 сек)
SELECT title FROM tracks
WHERE duration >= 210;

-- 3. Сборники 2018–2020 гг.
SELECT title FROM Collections
WHERE release_year BETWEEN 2018 AND 2020;

-- 4. Исполнители с одним словом в имени
SELECT name FROM artists
WHERE name NOT LIKE '% %';

-- 5. Треки, содержащие "мой" или "my"
SELECT title FROM tracks
WHERE LOWER(title) LIKE '%my%'
   OR LOWER(title) LIKE '%мой%';

-- 1. Количество исполнителей в каждом жанре
SELECT g.name, COUNT(ag.artist_id) 
FROM genres g
JOIN ArtistGenre ag ON g.genre_id = ag.genre_id
GROUP BY g.name;

-- 2. Количество треков из альбомов 2019–2020 гг.
SELECT COUNT(*) 
FROM tracks t
JOIN albums a ON t.album_id = a.album_id
WHERE a.release_year BETWEEN 2019 AND 2020;

-- 3. Средняя продолжительность треков по альбомам
SELECT a.title, AVG(t.duration) 
FROM albums a
JOIN tracks t ON a.album_id = t.album_id
GROUP BY a.title;

-- 4. Исполнители, не выпустившие альбомы в 2020 г.
SELECT ar.name 
FROM artists ar
WHERE ar.artist_id NOT IN (
  SELECT aa.artist_id 
  FROM ArtistAlbum aa
  JOIN albums a ON aa.album_id = a.album_id
  WHERE a.release_year = 2020
);

-- 5. Сборники, где есть конкретный исполнитель (например Eminem)
SELECT DISTINCT c.title 
FROM Collections c
JOIN CollectionTrack ct ON c.collection_id = ct.collection_id
JOIN tracks t ON ct.track_id = t.track_id
JOIN albums a ON t.album_id = a.album_id
JOIN ArtistAlbum aa ON a.album_id = aa.album_id
JOIN artists ar ON aa.artist_id = ar.artist_id
WHERE ar.name = 'Eminem';

-- 1. Альбомы, где исполнители более чем одного жанра
SELECT a.title
FROM albums a
JOIN ArtistAlbum aa ON a.album_id = aa.album_id
JOIN ArtistGenre ag ON aa.artist_id = ag.artist_id
GROUP BY a.title
HAVING COUNT(DISTINCT ag.genre_id) > 1;

-- 2. Треки, которые не входят в сборники
SELECT t.title
FROM tracks t
LEFT JOIN CollectionTrack ct ON t.track_id = ct.track_id
WHERE ct.collection_id IS NULL;

-- 3. Исполнители с самым коротким треком
SELECT ar.name, t.title, t.duration
FROM tracks t
JOIN albums a ON t.album_id = a.album_id
JOIN ArtistAlbum aa ON a.album_id = aa.album_id
JOIN artists ar ON aa.artist_id = ar.artist_id
WHERE t.duration = (SELECT MIN(duration) FROM tracks);

-- 4. Альбомы с наименьшим количеством треков
SELECT a.title
FROM albums a
JOIN tracks t ON a.album_id = t.album_id
GROUP BY a.title
HAVING COUNT(t.track_id) = (
  SELECT MIN(track_count)
  FROM (
    SELECT COUNT(*) AS track_count
    FROM tracks
    GROUP BY album_id
  ) q
);