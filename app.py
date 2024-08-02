from http.server import HTTPServer, SimpleHTTPRequestHandler
from http.cookies import SimpleCookie
from urllib.parse import urlparse, parse_qs
from datetime import datetime
import json
import urllib.parse
import os
import uuid
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

class MyHandler(SimpleHTTPRequestHandler):
    sessions = {}

    def do_GET(self):
        self.load_session()
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query = parse_qs(parsed_path.query)

        if path == '/':
            self.send_file('public/index.html')
        elif path == '/current_time':
            self.send_dynamic_content(self.get_current_time())
        elif path == '/counter':
            self.send_dynamic_content(self.get_counter())
        elif path == '/visit-count':
            content = self.get_visit_count()
            self.send_dynamic_content(content)
        else:
            super().do_GET()

    def do_POST(self):
        self.load_session()
        if self.path == '/submit-form':
            # コンテンツの長さを取得
            content_length = int(self.headers['Content-Length'])
            # POSTデータを読み取る
            post_data = self.rfile.read(content_length).decode('utf-8')
            # フォームデータをパース
            form = urllib.parse.parse_qs(post_data)
            
            # フォームデータを処理
            name = form.get('name', [''])[0]
            email = form.get('email', [''])[0]
            message = form.get('message', [''])[0]

            # データをファイルに保存
            self.save_inquiry(name, email, message)
            
            # レスポンスを送信
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            response = f"""
            <html>
            <head>
            <meta charset="utf-8">
            </head>
            <body>
            <h1>お問い合わせ受付完了</h1>
            <p>以下の内容で受け付けました：</p>
            <ul>
                <li>お名前: {name}</li>
                <li>メールアドレス: {email}</li>
                <li>メッセージ: {message}</li>
            </ul>
            <a href="/">トップページに戻る</a>
            </body>
            </html>
            """
            self.wfile.write(response.encode('utf-8'))
        else:
            self.send_error(404, "Not Found")

    def load_session(self):
        self.cookie = SimpleCookie(self.headers.get('Cookie'))
        session_id = self.cookie.get('session_id')
        if session_id is None:
            session_id = str(uuid.uuid4())
            self.sessions[session_id] = {}
        else:
            session_id = session_id.value
            if session_id not in self.sessions:
                self.sessions[session_id] = {}
        self.session_id = session_id
        self.session = self.sessions[session_id]

    def send_response(self, code, message=None):
        super().send_response(code, message)
        self.send_header('Set-Cookie', f'session_id={self.session_id}')

    def get_visit_count(self):
        count = self.session.get('visit_count', 0) + 1
        self.session['visit_count'] = count
        content = f"<html><body><h1>訪問回数</h1><p>あなたは{count}回目の訪問です.</p></body></html>"
        print(f"Content encoding: {content.encode('utf-8')}")  # デバッグ用

        return content

    def send_file(self, filename):
        # ファイルを送信する処理
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as file:
            self.wfile.write(file.read())
    
    def send_dynamic_content(self, content):
        # 動的コンテンツを送信する処理
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(content.encode('utf-8'))

    def save_inquiry(self, name, email, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = f"Timestamp: {timestamp}\nName: {name}\nEmail: {email}\nMessage: {message}\n\n"

        log_dir = 'log'

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        with open(os.path.join(log_dir, 'inquiries.txt'), 'a') as f:
            f.write(data)

    def get_current_time(self):
        # 現在時刻を取得する処理
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"<html><body><h1>Current Time</h1><p>{current_time}</p></body></html>"

    def get_counter(self):
        # アクセスカウンターの処理
        try:
            with open('counter.json', 'r') as f:
                counter = json.load(f)
        except FileNotFoundError:
            counter = {'count': 0}

        counter['count'] += 1

        with open('counter.json', 'w') as f:
            json.dump(counter, f)

        return f"<html><body><h1>Visiter Count></h1><p>This page has been Visited {counter['count']} times.</p></body></html>"

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHandler)
    print('Server running on port 8000...')
    httpd.serve_forever()


