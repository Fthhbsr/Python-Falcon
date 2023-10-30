import falcon
import json
from wsgiref.simple_server import make_server

# from waitress import serve
students = [
    {"id": 1, "name": "Ravi", "percent": 75.50},
    {"id": 2, "name": "Mona", "percent": 80.00},
    {"id": 3, "name": "Mathews", "percent": 65.25},
]


class StudentResource:
    def on_get(self, req, resp):
        resp.text = json.dumps(students)
        resp.status = falcon.HTTP_OK
        resp.content_type = falcon.MEDIA_JSON

    def on_post(self, req, resp):
        student = json.load(req.bounded_stream)
        students.append(student)
        resp.text = "Student added successfully."
        resp.status = falcon.HTTP_OK
        resp.content_type = falcon.MEDIA_TEXT

    def on_get_student(self, req, resp, id):
        resp.text = json.dumps(students[id - 1])
        resp.status = falcon.HTTP_OK
        resp.content_type = falcon.MEDIA_JSON

    def on_put_student(self, req, resp, id):
        student = students[id - 1]
        data = json.load(req.bounded_stream)

        student.update(data)

        resp.text = json.dumps(student)
        resp.status = falcon.HTTP_OK
        resp.content_type = falcon.MEDIA_JSON

    def on_delete_student(self, req, resp, id):
        students.pop(id - 1)
        print(students)
        resp.text = json.dumps(students)
        resp.status = falcon.HTTP_OK
        resp.content_type = falcon.MEDIA_JSON


app = falcon.App()
app.add_route("/students", StudentResource())
app.add_route("/students/{id:int}", StudentResource(), suffix="student")
# if __name__ == '__main__':
#     serve(app, host='0.0.0.0', port=8000)

if __name__ == "__main__":
    with make_server("", 8000, app) as httpd:
        print("Serving on port 8000...")
        # Serve until process is killed
        httpd.serve_forever()
