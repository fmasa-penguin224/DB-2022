import mysql.connector, datetime, re

class Group:

    def __init__(self):
        '''
        Constructor
        '''

    @classmethod
    def group_add(cls, user_id, group_name):
        '''
        新しいグループの追加
        '''
        db=mysql.connector.connect(host="mysql", user="root", password="root", database="tmcit")
        cursor=db.cursor(buffered=True)
        
        cursor.execute("select group_id from groupinfo where group_name = %s and user_id = %s", (group_name , user_id))
        get1 = cursor.fetchone()
        print(get1)
        print(type(get1))
        
        # 追加した人自身の追加
        if get1 is None:
            cursor.execute("INSERT INTO groupinfo VALUES (%s, NULL , now(), now() , %s)", (int(user_id) , group_name))
            db.commit()
            return 'グループに追加しました'
        
        else:
            return '既にユーザが追加されています'
