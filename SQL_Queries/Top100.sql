SELECT ta.Album_pic,ts.Title,ar.ArtistName FROM (
    SELECT `SongID`,COUNT(*) as cnt FROM `T_usersongRecord` tc
    WHERE `requestTime` BETWEEN "2023-11-26 17:00:00" AND DATE_ADD('2023-11-26 17:00:00',INTERVAL 1 HOUR)
    GROUP BY `SongID`
    ) a 
JOIN `T_SongInformation` ts ON a.SongID = ts.`SongID`
JOIN `T_Album` ta ON ts.`AlbumID` = ta.`AlbumID`
JOIN `T_Artist` ar ON ts.`ArtistID` = ar.`ArtistID`
ORDER BY a.cnt DESC
LIMIT 100;
