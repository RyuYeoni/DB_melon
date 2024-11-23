from datetime import datetime
from flask import Flask, request
import pymysql
import pandas as pd
app = Flask(__name__)
@app.route('/songRequest', methods=['POST'])
def song_request_query():
    request_json = request.get_json()
    cust_input = request_json['userID']
    song_input = request_json['songID']
    time_input = request_json['songTime']
    status_input = request_json['status']
    now = datetime.now()
    curTime = now.strftime('%Y-%m-%d %H:%M:%S')

    conn = pymysql.connect(host='localhost', port=3306, user='root',
                        password='', db='melon_final')
    
    sql = """
    SELECT ti.`Title`,ta.`ArtistName` 
    FROM `T_SongInformation` ti
    JOIN `T_Artist` ta
    ON ti.`ArtistID` = ta.`ArtistID`
    WHERE `SongID`= %s;
    """% (song_input)
    df = pd.read_sql_query(sql,conn)
    with conn.cursor() as cursor:
        if status_input == 1:
            sql = "INSERT INTO T_usersongRequest (UserID,SongID,songTime,requestTime,songStatus) VALUES (%s,%s,'%s','%s',%s);"% (cust_input,song_input,time_input,curTime,status_input)
            cursor.execute(sql)
            conn.commit()
            toast = '1곡을 재생목록에 담았습니다'
            df_dict = { "response" : toast,"title" : df['Title'].tolist(),"artist":df['ArtistName'].tolist(),"status":status_input}

        else:
            sql = "INSERT INTO T_usersongRequest (UserID,SongID,songTime,requestTime,songStatus) VALUES (%s,%s,'%s','%s',%s);"% (cust_input,song_input,time_input,curTime,status_input)
            cursor.execute(sql)
            conn.commit()
            df_dict = {"title" : df['Title'].tolist(),"artist":df['ArtistName'].tolist(),"status":status_input}
    return df_dict
if __name__ == "__main__":
    app.run()