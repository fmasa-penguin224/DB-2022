import mysql.connector, datetime, re

class Task:

    def __init__(self):
        '''
        Constructor
        '''

    @classmethod
    def task_add(cls, user_id, group_name,date_limit,task_name,task_content):
        '''
        タスクの追加
        '''
        db=mysql.connector.connect(host="mysql", user="root", password="root", database="tmcit")
        cursor=db.cursor(buffered=True)
        cursor.execute("INSERT INTO taskinfo VALUES (NULL , %s , %s, now() , %s , %s , %s)", (int(user_id) , group_name , date_limit , task_name ,task_content))
        db.commit()

        return True

        