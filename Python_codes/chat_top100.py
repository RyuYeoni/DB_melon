from flask import Flask, request
import pymysql
import pandas as pd
app = Flask(__name__)
@app.route('/chart', methods=['POST'])
def chart_query():
    request_json = request.get_json()
    update_time_input = request_json['update_time']
    conn = pymysql.connect(host='localhost', port=3306, user='root',
                        password='', db='melon_final')
    sql_chart = """
        SELECT ta.Album_pic,ts.Title,ar.ArtistName FROM (
        SELECT `SongID`,COUNT(*) as cnt FROM `T_usersongRecord` tc
        WHERE `requestTime` BETWEEN '%s' AND DATE_ADD('%s',INTERVAL 1 HOUR)
        GROUP BY `SongID`
        ) a 
        JOIN `T_SongInformation` ts ON a.SongID = ts.`SongID`
        JOIN `T_Album` ta ON ts.`AlbumID` = ta.`AlbumID`
        JOIN `T_Artist` ar ON ts.`ArtistID` = ar.`ArtistID`
        ORDER BY a.cnt DESC
        LIMIT 100;
        """% (update_time_input,update_time_input)
    df_chart = pd.read_sql_query(sql_chart, conn)
    df_dict = {
        "chart": {
                "images": df_chart['Album_pic'].tolist(), 
                "title": df_chart['Title'].tolist(),
                "artist": df_chart['ArtistName'].tolist()
                }
        }
    return df_dict
if __name__ == "__main__":
    app.run()
