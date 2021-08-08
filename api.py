import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from urllib.parse import parse_qs
import json

import dat

model = dat.Model("glove.6B.300d.txt", "words.txt")


class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    def do_GET(self):
      if self.path.startswith('/api/calculate'):
          self._set_headers()
          print(self.path)
          parsed = urlparse(self.path)
          body = parse_qs(parsed.query)

          print(body)
          
          try:
            distance = model.distance(body['word1'][0], body['word2'][0])
            self.wfile.write(bytes(json.dumps({ "score": distance }), "utf-8"))
          except:
            self.wfile.write(bytes(json.dumps({ "error": 'Invalid word' }), "utf-8"))


def run(server_class=HTTPServer, handler_class=S, addr="localhost", port=8000):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)

    print(f"Starting httpd server on {addr}:{port}")
    httpd.serve_forever()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Run a simple HTTP server")
    parser.add_argument(
        "-l",
        "--listen",
        default="localhost",
        help="Specify the IP address on which the server listens",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=8000,
        help="Specify the port on which the server listens",
    )
    args = parser.parse_args()
    run(addr=args.listen, port=args.port)