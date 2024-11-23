from flask import Flask, request
import pymysql
import pandas as pd
app = Flask(__name__)
@app.route('/recommend', methods=['POST'])
def freind_recommend_query():
    request_json = request.get_json()
    cust_input = request_json['userID']
    conn = pymysql.connect(host='localhost', port=3306, user='root',
                        password='', db='melon_final')
    sql_recommend = """
        SELECT IFNULL(tg.`GenreName`,"") as Genre,c.`UserName`, p.`Pic_url`, a.cnt, IFNULL(lh.`Title`,"") as title,IFNULL(ta.`ArtistName`,"") as name,pc.playlist_cnt, tal.`Album_pic`
        FROM (
            SELECT FriendID, count(*) cnt
            FROM T_Friend
            WHERE UserID in (
                SELECT FriendID
                FROM T_Friend
                WHERE UserID = %s)
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
            WHERE UserID = %s)
        HAVING a.cnt >= 5 AND `Title` != ""
        ORDER BY cnt DESC
        LIMIT 3;
        """% (cust_input,cust_input)
    df_recommend = pd.read_sql_query(sql_recommend, conn)
    df_dict = {
        "history": {"favorite genre": df_recommend['Genre'].tolist(), "name": df_recommend['UserName'].tolist(),
                "user_pic_url": df_recommend['Pic_url'].tolist(),"album_pic_url":df_recommend['Album_pic'].tolist(),"title": df_recommend['title'].tolist() ,
                "artist": df_recommend['name'].tolist(), "playlist_count": df_recommend['playlist_cnt'].tolist()
                }
        }
    return df_dict
if __name__ == "__main__":
    app.run()
