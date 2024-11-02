from ast import Return
from flask import Flask, render_template, request, redirect, url_for, make_response  # type: ignore
import mysql.connector  # type: ignore
import os
from model import PostModel  # model.pyをインポート
from DB import DB

app = Flask(__name__)

# ホームページでデータを投稿・表示
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['user_input']
        # 入力データをデータベースに挿入
        PostModel.insert_post(user_input)
        # Cookieに保存
        resp = make_response(redirect(url_for('index')))
        resp.set_cookie('last_post', user_input)
        return resp

    # データベースから投稿データを取得
    posts = PostModel.get_all_posts()
    
    last_post = request.cookies.get('last_post')

    return render_template('index.html', posts=posts, last_post=last_post)

# 新規登録画面
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # 入力データをデータベースに挿入
        PostModel.insert_user(email, password)
        # Cookieに保存
        resp = make_response(redirect(url_for('index')))
        resp.set_cookie('last_post', email)
        return resp

    return render_template('create.html')

# ログイン画面
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # ユーザーの認証
        user = PostModel.get_user_by_email(email)
        if user and user['password'] == password:
            # ログイン成功
            resp = make_response(redirect(url_for('index')))
            resp.set_cookie('user_email', email)  # Cookieにユーザーのメールを保存
            return resp
        else:
            # ログイン失敗
            error_message = 'メールアドレスまたはパスワードが間違っています。'
            return render_template('login.html', error=error_message)
    
    return render_template('login.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002)