from wsgiref.simple_server import make_server

import falcon

import json

app = falcon.App()


class HelloResource:
    def on_get(self, req, resp):
        """Handles GET requests"""
        # data = req.media
        # print("on_get", data)
        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_TEXT
        resp.text = "Hello World"

    def on_post(self, req, resp):
        data = req.media
        print("post", data)
        nm = data["name"]
        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_TEXT
        resp.text = "Hello " + nm


hello = HelloResource()

app.add_route("/hello", hello)

if __name__ == "__main__":
    with make_server("", 8000, app) as httpd:
        print("Serving on port 8000...")
        # Serve until process is killed
        httpd.serve_forever()
