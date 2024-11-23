SELECT fsv.`UserID`,fsv.`Album_pic`,fsv.`Title`,fsv.`ArtistName` ,sc.`NumOfSong`,ac.`NumOfArtist`,sc.`listenTime`
FROM favorite_song_view fsv
JOIN song_count_view sc ON fsv.`UserID` = sc.`UserID`
JOIN artist_count_view ac ON fsv.`UserID` = ac.`UserID`
WHERE fsv.`UserID` = 1
LIMIT 1;
