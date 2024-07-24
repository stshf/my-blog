from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from datetime import datetime
import json

class MyHandler(SimpleHTTPRequestHandler):

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query = parse_qs(parsed_path.query)

        if path == '/':
            self.send_file('public/index.html')
        elif path == '/current/time':
            self.send_dynamic_content(self.get_current_time())
        elif path == '/greet':
            name = query.get('name', ['Guest'][0])
            self.send_dynamic_content(self.get_greeting(name))
        elif path == '/counter':
            self.send_dynamic_content(self.get_counter())
        else:
            super().do_GET()
    
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

    def get_greeting(self, name):
        # 挨拶メッセージを生成する処理
        return f"<html><body><h1>Hello, {name}!</h1></body></html>"

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


