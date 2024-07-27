from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from datetime import datetime
import json
import urllib.parse

class MyHandler(SimpleHTTPRequestHandler):

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query = parse_qs(parsed_path.query)

        if path == '/':
            self.send_file('public/index.html')
        elif path == '/current_time':
            self.send_dynamic_content(self.get_current_time())
        elif path == '/counter':
            self.send_dynamic_content(self.get_counter())
        else:
            super().do_GET()

    def do_POST(self):
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

    def send_file(self, filename):
        # ファイルを送信する処理
        self.send_response(200)
        self.send_header('Counter-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as file:
            self.wfile.write(file.read())
    
    def send_dynamic_content(self, content):
        # 動的コンテンツを送信する処理
        self.send_response(200)
        self.send_header('Counter-type', 'text/html')
        self.end_headers()
        self.wfile.write(content.encode())

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


