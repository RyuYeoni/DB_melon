-- CREATE DATABASE melon_final;
-- use melon_final;

CREATE TABLE T_User (
    UserID INT PRIMARY KEY NOT NULL,
    UserName VARCHAR(255) NOT NULL
);

CREATE TABLE T_Friend (
    UserID INT,
    FriendID INT,
    PRIMARY KEY (UserID, FriendID),
    FOREIGN KEY (UserID) REFERENCES T_User(UserID),
    FOREIGN KEY (FriendID) REFERENCES T_User(UserID)
);

CREATE TABLE T_User_pic (
    PicID INT PRIMARY KEY NOT NULL,
    UserID INT,
    Pic_url VARCHAR(255),
    Update_time TIMESTAMP NOT NULL,
    FOREIGN KEY (UserID) REFERENCES T_User(UserID)
);

CREATE TABLE T_Artist (
    ArtistID INT PRIMARY KEY NOT NULL,
    ArtistName VARCHAR(255) NOT NULL
);

CREATE TABLE T_Genre (
    GenreID INT PRIMARY KEY NOT NULL,
    GenreName VARCHAR(255) NOT NULL
);

CREATE TABLE T_Album (
    AlbumID INT PRIMARY KEY NOT NULL,
    AlbumName VARCHAR(255) NOT NULL,
    ArtistID INT,
    Album_pic VARCHAR(255) NOT NULL,
    FOREIGN KEY (ArtistID) REFERENCES T_Artist(ArtistID)
);

CREATE TABLE T_SongInformation (
    SongID INT PRIMARY KEY NOT NULL,
    Title VARCHAR(255) NOT NULL,
    ArtistID INT,
    GenreID INT,
    Duration TIME NOT NULL,
    AlbumID INT,
    FOREIGN KEY (ArtistID) REFERENCES T_Artist(ArtistID),
    FOREIGN KEY (GenreID) REFERENCES T_Genre(GenreID),
    FOREIGN KEY (AlbumID) REFERENCES T_Album(AlbumID)
);

CREATE TABLE T_SongHeart (
    UserID INT,
    Heart_Update_time TIMESTAMP,
    SongID INT,
    Heart INT NOT NULL,
    PRIMARY KEY (UserID, Heart_Update_time, SongID),
    FOREIGN KEY (UserID) REFERENCES T_User(UserID),
    FOREIGN KEY (SongID) REFERENCES T_SongInformation(SongID)
);

CREATE TABLE T_usersongRecord (
    recordID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    UserID INT,
    SongID INT,
    requestTime TIMESTAMP NOT NULL,
    FOREIGN KEY (UserID) REFERENCES T_User(UserID),
    FOREIGN KEY (SongID) REFERENCES T_SongInformation(SongID)
);

CREATE TABLE T_usersongRequest (
    requestID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    UserID INT,
    SongID INT,
    songTime TIME NOT NULL,
    requestTime TIMESTAMP NOT NULL,
    songStatus INT NOT NULL,
    FOREIGN KEY (UserID) REFERENCES T_User(UserID),
    FOREIGN KEY (SongID) REFERENCES T_SongInformation(SongID)
);

CREATE TABLE T_Playlist (
    PlaylistID INT PRIMARY KEY NOT NULL,
    UserID INT,
    Title VARCHAR(255) NOT NULL,
    FOREIGN KEY (UserID) REFERENCES T_User(UserID)
);