import mysql.connector, datetime, re
from flask import session
from lib.user import User

class Group:

    def __init__(self):
        '''
        Constructor
        '''

    @classmethod
    def group_add(cls, user_id, group_name,user_name):
        '''
        新しいグループの追加
        '''
        db=mysql.connector.connect(host="mysql", user="root", password="root", database="tmcit")
        cursor=db.cursor(buffered=True)
        
        # cursor.execute("select group_id from groupinfo where group_name = %s", (group_name,))
        # get1 = cursor.fetchone()
        # print(get1)
        # if get1 is None:
        #     return group_name+'は既に追加されています'
        # else:
        myname=session["name"]
        print('session:'+myname)
        myid=User.get_userID(myname)

        cursor.execute("select group_id from groupinfo where group_name = %s and user_id = %s", (group_name , myid))
        get1 = cursor.fetchone()
        print(type(get1))
        
        # 追加した人自身の追加
        if get1 is None:
            cursor.execute("INSERT INTO groupinfo VALUES ( NULL ,%s, now(), now() , %s)", (int(myid) , group_name))
            db.commit()
            return myname + 'を' + group_name + 'に追加しました'


        cursor.execute("select group_id from groupinfo where group_name = %s and user_id = %s", (group_name , user_id))
        get2 = cursor.fetchone()
        print(get2)
        print(type(get2))
        
        # 追加した人自身の追加
        if get2 is None:
            cursor.execute("INSERT INTO groupinfo VALUES ( NULL ,%s, now(), now() , %s)", (int(user_id) , group_name))
            db.commit()
            return user_name + 'を' + group_name + 'に追加しました'
        
        else:
            return '既に'+ user_name +'はグループに追加されています'

    @classmethod
    def sarch_group(cls, user_id):
        '''
        所属グループの検索
        '''
        db=mysql.connector.connect(host="mysql", user="root", password="root", database="tmcit")
        cursor=db.cursor(buffered=True)

        cursor.execute("select group_name from groupinfo where user_id = %s", (user_id,))
        result = cursor.fetchall()

        # 結果からグループ名を取り出す
        for row in result:
            print(row[0])
            # lists = []
            # lists.append(row[0])

        return result


