-- user_pic_update_view (latest picture for each user) 
CREATE VIEW user_pic_update_view AS
SELECT UserID, max(PicID) max_pic_id
FROM T_User_pic
GROUP BY UserID
ORDER BY UserID;

-- favorite_genre_view (each user’s favorite genre)
CREATE VIEW favorite_genre_view AS
SELECT `UserID`,`GenreID`, favorite
FROM (
    SELECT usr.UserID,si.GenreID,COUNT(si.GenreID) AS favorite,
    ROW_NUMBER() OVER (PARTITION BY usr.UserID ORDER BY COUNT(si.GenreID) DESC) AS genre_rank
    FROM `T_usersongRecord` usr
    LEFT JOIN `T_SongInformation` si ON usr.SongID = si.songID
    GROUP BY usr.UserID, si.GenreID
) ranked
WHERE genre_rank = 1;

-- latest_heart (each user’s latest like time)
create view latest_heart as
select sh.UserID, max(sh.`Heart_Update_time`) update_heart from `T_SongHeart` sh
where heart = 1
group by sh.UserID;

-- latest_heart_song (song that each user liked within 10 days)
create view latest_heart_song as
select sh.UserID, sh.`Heart_Update_time`, si.SongID, si.Title from `T_SongHeart` sh
left join latest_heart lh on lh.UserID = sh.UserID
left join `T_SongInformation` si on si.SongID = sh.SongID
where lh.update_heart = sh.`Heart_Update_time` AND DATEDIFF(CURDATE(),`Heart_Update_time`) < 10
group by sh.UserID, si.SongID;

-- playlist_count (the number of playlists that each user made)
CREATE VIEW playlist_count as
select u.userID, count(pl.playlistID) playlist_cnt FROM T_user u
LEFT JOIN T_playlist pl ON u.userID = pl.userID
group by u.userID;

-- each_song_count_view (count songs each user listened)
CREATE VIEW each_song_count_view AS
SELECT `UserID`,`SongID`,COUNT(*) cnt FROM `T_usersongRecord`
GROUP BY `UserID`,`SongID`; 

-- Favorite_song_view (the most listend song)
CREATE View favorite_song_view AS
SELECT escv.`UserID`,ta.`Album_pic`,ts.`Title`,ar.`ArtistName` 
FROM each_song_count_view escv
JOIN (
    SELECT `UserID`,MAX(cnt) maxSongcnt FROM each_song_count_view
    GROUP BY `UserID`
)b ON escv.`UserID` = b.`UserID` AND escv.cnt = b.maxSongcnt
JOIN `T_SongInformation` ts ON ts.`SongID` = escv.`SongID`
JOIN `T_Album` ta ON ts.`AlbumID` = ta.`AlbumID`
JOIN `T_Artist` ar ON ts.`ArtistID` = ar.`ArtistID`;

-- artist_count_view(count how many artists a user has listened)
CREATE View artist_count_view AS
SELECT a.`UserID`,COUNT(*) as NumOfArtist FROM (
    SELECT sc.`UserID`,tc.`ArtistID`,COUNT(*) as artistCnt FROM `T_usersongRecord` sc
    JOIN `T_SongInformation` tc ON sc.`SongID` = tc.`SongID`
    JOIN `T_Album` ta ON tc.`AlbumID` = ta.`AlbumID`
    GROUP BY sc.`UserID`,tc.`ArtistID`
    ORDER BY sc.`UserID`
) a
GROUP BY a.`UserID`;

-- song_count_view(count how many songs a user has listened to, how long they've been listening to them)
CREATE View song_count_view AS
SELECT s.`UserID`,COUNT(*) as NumOfSong, FLOOR(SUM(s.songCnt*TIME_TO_SEC(s.`Duration`))/60) as listenTime FROM (
    SELECT sc.`UserID`,sc.`SongID`,COUNT(*) as songCnt,tc.`Duration` FROM `T_usersongRecord` sc
    JOIN `T_SongInformation` tc ON sc.`SongID` = tc.`SongID`
    JOIN `T_Album` ta ON tc.`AlbumID` = ta.`AlbumID`
    GROUP BY sc.`UserID`,sc.`SongID`,tc.`Duration`
    ORDER BY sc.`UserID`
) s
GROUP BY s.`UserID`;

-- User_request_time_view(view to compare time between requests)
CREATE VIEW user_request_time_view AS
SELECT `UserID`,tur.`SongID`,ts.`Duration`,`songTime`,`songStatus`,`requestTime`,
LEAD(`requestTime`,1,ADDTIME(`requestTime`,`Duration`)) OVER (
    PARTITION BY `UserID`
    ORDER BY `UserID`,`requestTime`
) as nextRequest
FROM `T_usersongRequest` as tur
JOIN `T_SongInformation` as ts ON tur.`SongID` = ts.`SongID`;

