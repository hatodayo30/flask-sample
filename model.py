import pymysql  # type: ignore
import os
from DB import DB

   

class PostModel:
    @staticmethod
    def insert_post(content):
        conn = DB.getConnection()
        if conn is None:
            return False
        
        try:
            with conn.cursor() as cursor:
                cursor.execute('INSERT INTO posts (content) VALUES (%s)', (content,))
            conn.commit()
            return True
        except pymysql.MySQLError as e:
            print(f"投稿の挿入エラーです: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def get_all_posts():
        conn = DB.getConnection()
        if conn is None:
            return []

        try:
            with conn.cursor() as cursor:
                cursor.execute('SELECT email, password FROM posts')
                return cursor.fetchall()
        except pymysql.MySQLError as e:
            print(f"投稿の取得エラーです: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def insert_user(email, password):
        conn = DB.getConnection()
        if conn is None:
            return False
        
        try:
            with conn.cursor() as cursor:
                cursor.execute('INSERT INTO posts (email, password) VALUES (%s, %s)', (email, password))
            conn.commit()
            return True
        except pymysql.MySQLError as e:
            print(f"ユーザーの挿入エラーです: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def get_user_by_email(email):
        conn = DB.getConnection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)  # ディクショナリ形式で返す
        query = "SELECT * FROM posts WHERE email = %s"
        cursor.execute(query, (email,))
        
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user