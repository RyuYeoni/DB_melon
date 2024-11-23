from flask import Flask, request
import pymysql
import pandas as pd
app = Flask(__name__)
@app.route('/record_update', methods=['POST'])
def user_record_update_query():
    request_json = request.get_json()
    update_time_input = request_json['update_time']
    conn = pymysql.connect(host='localhost', port=3306, user='root',
                        password='', db='melon_final')
    sql = """
        SELECT a.UserID,a.SongID,a.`requestTime` FROM (
        SELECT urtv.`UserID`,urtv.`SongID`,`songTime`,urtv.duration ,urtv.`requestTime`,urtv.nextRequest,urtv.`songStatus`,
        IF(duration<=TIMEDIFF(TIME(urtv.nextRequest),TIME(urtv.`requestTime`)),1,0) as valid 
        FROM user_request_time_view as urtv
        WHERE `songTime` = '0' AND `songStatus` = 1 AND `requestTime` BETWEEN '%s' AND DATE_ADD('%s',INTERVAL 1 HOUR)
        ORDER BY urtv.`UserID`,urtv.`requestTime`
    ) a
    WHERE valid = 1
    ORDER BY `requestTime`;
    """% (update_time_input,update_time_input)
    df2 = pd.read_sql_query(sql,conn)
    with conn.cursor() as cursor:
        if len(df2)>0:
            for i in range(len(df2)):
                sql = "INSERT INTO T_usersongRecord (UserID,SongID,requestTime) VALUES (%s,%s,'%s')"% (df2['UserID'].to_list()[i], df2['SongID'].to_list()[i],df2['requestTime'].to_list()[i])
                cursor.execute(sql)
                conn.commit()
        df_dict = {"userID": df2['UserID'].tolist(), "songID": df2['SongID'].tolist(), "requestTime": df2['requestTime'].tolist()}
        return df_dict
if __name__ == "__main__":
    app.run()