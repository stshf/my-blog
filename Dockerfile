FROM python:3.9-slim

WORKDIR /app

RUN pip install --no-chache-dir django

# copy file in current folder -> /app
COPY . /app

# コンテナ起動時に実行されるコマンドを指定
CMD ["python", "-m", "http.server", "8000"]