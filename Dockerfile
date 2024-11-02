# Python 3.9ベースイメージ
FROM --platform=linux/amd64 python:3.9-slim


# 作業ディレクトリの設定
WORKDIR /app

# 必要なファイルをコンテナにコピー
COPY requirements.txt requirements.txt
COPY . .

# 依存パッケージをインストール
RUN pip install --no-cache-dir -r requirements.txt

# Flaskアプリを起動
CMD ["python", "app.py"]
