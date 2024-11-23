from flask import Flask, request
import pymysql
import pandas as pd
app = Flask(__name__)
#student query
@app.route('/history', methods=['POST'])
def user_history_query():
    request_json = request.get_json()
    cust_input = request_json['userID']
    conn = pymysql.connect(host='localhost', port=3306, user='root',
                        password='', db='melon_final')
    sql_history = """
        SELECT fsv.`UserID`,fsv.`Album_pic`,fsv.`Title`,fsv.`ArtistName` ,sc.`NumOfSong`,ac.`NumOfArtist`,sc.`listenTime`
        FROM favorite_song_view fsv
        JOIN song_count_view sc ON fsv.`UserID` = sc.`UserID`
        JOIN artist_count_view ac ON fsv.`UserID` = ac.`UserID`
        WHERE fsv.`UserID` = %s
        LIMIT 1;
        """% (cust_input)
    df_history = pd.read_sql_query(sql_history, conn)
    df_dict = {
        "history": {"time": df_history['listenTime'].tolist(), "numArtists": df_history['NumOfArtist'].tolist(),
                "numSongs": df_history['NumOfSong'].tolist(),"image": df_history['Album_pic'].tolist() ,
                "title": df_history['Title'].tolist(), "artist": df_history['ArtistName'].tolist()
                }
        }
    return df_dict
if __name__ == "__main__":
    app.run()
