import mysql.connector, datetime, re
from flask import session
    
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
        id = cursor.fetchone()[0]
        print(id,type(id))
        return int(id)


    @classmethod
    def get_username(cls, user_id):
        '''
        useridからusernameを取得
        '''
        db=mysql.connector.connect(host="mysql", user="root", password="root", database="tmcit")
        cursor=db.cursor(buffered=True)
        # conn = DatabaseConnection.get_connection()
        cursor.execute("SELECT user_name FROM userinfo WHERE user_id=%s", (user_id,))
        name = cursor.fetchone()[0]
        print(name,type(name))
        return name

    @classmethod
    def loginjudge(cls, name):
        '''
        ログイン判定
        '''
        print(name)
        if str(name)=='None':
            session["flag"]=False
            return 'False'
        else:
            session["flag"]=True
            return 'True'
