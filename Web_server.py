import http.server
import socketserver
import os
import json

PORT = 2008
STATIC_PAPKA = "static"


class WebHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        # 🔹 Обробка API запитів
        if self.path.startswith("/api"):
            self.handle_api()
        else:
            # 🔹 Статичні файли
            self.handle_static()

    def do_POST(self):
        if self.path.startswith("/api"):
            self.handle_api_post()
        else:
            self.send_error(404, "Not found")

    def create_data(self, achki):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        try:
            item = json.loads(body)
            data = self.get_json(achki)
            id = self.next_id(data)
            item["id"] = id
            data.append(item)
            self.save_json(achki, data)
            self.send_json(item)

        except json.JSONDecodeError:
            data = {"raw": body.decode()}
            self.send_json({"Wrong data": data})

    def handle_api_post(self):
        if self.path == "/api/tema":
            self.create_data("temachki")
        else:
            self.send_error(404, "System error")


    def get_json(self, name):
        if not os.path.exists(f"danye/{name}.json"):
            return []
        with open( f"danye/{name}.json", "r", encoding="utf-8") as f:
            response = json.load(f)
        return  response

    def save_json(self, name, data):
        with open(f"danye/{name}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def next_id(self, data):
        if not data:
            return 1
        return max(item["id"] for item in data) + 1


    def handle_api(self):
        if self.path == "/api/tema":
           response = self.get_json("temachki")
        elif self.path == "/api/time":
            import datetime
            response = {"time": datetime.datetime.now().isoformat()}
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"API endpoint not found")
            return

        # Відправка JSON
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    def handle_static(self):
        # Змінюємо директорію на static
        if self.path == "/":
            self.path = "/index.html"

        file_path = os.path.join(STATIC_PAPKA, self.path.lstrip("/"))

        if os.path.exists(file_path) and os.path.isfile(file_path):
            self.send_response(200)

            # Простий Content-Type
            if file_path.endswith(".html"):
                self.send_header("Content-Type", "text/html")
            elif file_path.endswith(".css"):
                self.send_header("Content-Type", "text/css")
            elif file_path.endswith(".js"):
                self.send_header("Content-Type", "application/javascript")
            else:
                self.send_header("Content-Type", "application/octet-stream")

            self.end_headers()

            with open(file_path, "rb") as f:
                self.wfile.write(f.read())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"File not found")

    def send_json(self, data):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())


# Запуск сервера
with socketserver.TCPServer(("", PORT), WebHandler) as httpd:
    print(f"Server running at http://localhost:{PORT}")
    httpd.serve_forever()