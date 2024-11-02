from flask import Flask, render_template, request, redirect, url_for, make_response  # type: ignore
import mysql.connector  # type: ignore
import os

app = Flask(__name__)

# MySQLの設定
db_config = {
    'host': os.getenv('MYSQL_HOST', 'db'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', 'password'),
    'database': os.getenv('MYSQL_DATABASE', 'flaskapp')
}

# データベースに接続する関数
def get_db_connection():
    return mysql.connector.connect(**db_config)

# ホームページでデータを投稿・表示
@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        user_input = request.form['user_input']
        # 入力データをデータベースに挿入
        cursor.execute('INSERT INTO posts (content) VALUES (%s)', (user_input,))
        conn.commit()
        # Cookieに保存
        resp = make_response(redirect(url_for('index')))
        resp.set_cookie('last_post', user_input)
        return resp

    # データベースから投稿データを取得
    cursor.execute('SELECT content FROM posts')
    posts = cursor.fetchall()
    
    last_post = request.cookies.get('last_post')

    cursor.close()
    conn.close()

    return render_template('index.html', posts=posts, last_post=last_post)

# 新規作成画面
@app.route('/create', methods=['GET', 'POST'])
def create():
    message = ''
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['bpdy']
        # 入力データをデータベースに挿入
        cursor.execute('INSERT INTO posts (content) VALUES (%s)', (title,))
        conn.commit()
        # Cookieに保存
        resp = make_response(redirect(url_for('index')))
        resp.set_cookie('last_post', title)
        return resp

    # データベースから投稿データを取得
    cursor.execute('SELECT content FROM posts')
    posts = cursor.fetchall()
    
    last_post = request.cookies.get('last_post')

    cursor.close()
    conn.close()

    return render_template('create.html', posts=posts, last_post=last_post)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002)
