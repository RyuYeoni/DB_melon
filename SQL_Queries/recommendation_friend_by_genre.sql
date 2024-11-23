-- Recommendation friend by genre
SELECT IFNULL(tg.`GenreName`,"") as Genre,c.`UserName`, p.`Pic_url`, a.cnt, IFNULL(lh.`Title`,"") as title,IFNULL(ta.`ArtistName`,"") as name,pc.playlist_cnt, tal.`Album_pic`
FROM (
      SELECT FriendID, count(*) cnt
      FROM T_Friend
      WHERE UserID in (
            SELECT FriendID
            FROM T_Friend
            WHERE UserID = 1)
      GROUP BY FriendID
) a
JOIN T_User c on a.FriendID = c.UserID
JOIN user_pic_update_view pu on c.UserID = pu.UserID
JOIN T_User_pic p on pu.max_pic_id = p.`PicID`
LEFT JOIN favorite_genre_view fg ON fg.`UserID` = c.`UserID`
LEFT JOIN `T_Genre` tg ON tg.`GenreID` = fg.`GenreID`
LEFT JOIN latest_heart_song lh ON lh.`UserID` = c.`UserID`
LEFT JOIN `T_SongInformation` ts ON ts.`SongID` = lh.`SongID`
LEFT JOIN `T_Artist` ta ON ta.`ArtistID` = ts.`ArtistID`
LEFT JOIN `T_Album` tal ON tal.`AlbumID` = ts.`AlbumID`
LEFT JOIN playlist_count pc ON pc.`UserID` = c.`UserID`
WHERE a.FriendID not in (
      SELECT FriendID
      FROM T_Friend
      WHERE UserID = 1)
HAVING a.cnt >= 5 AND `Title` != ""
ORDER BY cnt DESC
LIMIT 3;
