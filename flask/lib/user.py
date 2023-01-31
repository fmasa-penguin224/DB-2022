import mysql.connector, datetime, re
    
class User:

    def __init__(self):
        '''
        Constructor
        '''

    @classmethod
    def get_userID(cls, user_name):
        '''
        usernameからuseridを取得
        '''
        db=mysql.connector.connect(host="mysql", user="root", password="root", database="tmcit")
        cursor=db.cursor(buffered=True)
        # conn = DatabaseConnection.get_connection()
        cursor.execute("SELECT user_id FROM userinfo WHERE user_name=%s", (user_name,))
        id = int(cursor.fetchone()[0])
        print(id,type(id))
        return int(id)

    def loginjudge(cls, name):
        '''
        ログイン判定
        '''
        print(name)
        if str(name)=='None':
            session["flag"]=False
        else:
            session["flag"]=True
