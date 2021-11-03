import json

from django.test import TestCase, Client

from postings.models import Posting
from users.models import User


class PostingCRUDTest(TestCase):
    def setUp(self):
        User.objects.create(id=1, name="Ted", email="hayejun1013@naver.com", password="abcd1234"),
        User.objects.create(id=2, name="Ted", email="hayejun1013@naver.co.kr", password="abcd1234")
        
        Posting.objects.create(id=1, title="Title", text="text", author_id=1)

    def tearDown(self):
        Posting.objects.all().delete()
        User.objects.all().delete()

    def test_get_posting_success(self):
        client = Client()
        response = client.get("/postings/1")

        posting = Posting.objects.get(id=1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "result": {
                    "id": posting.id,
                    "author": posting.author.name,
                    "title": posting.title,
                    "text": posting.text,
                    "created_time": posting.created_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
                    "updated_at": posting.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]+ "Z",
                }
            },
        )

    def test_get_posting_not_found(self):
        client = Client()
        response = client.get("/postings/10")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"message": "POSTING_10_NOT_FOUND"})

    def test_create_post_success(self):
        client = Client()
        data = {
            "title": "title",
            "text": "text",
        }
        header = {
            "HTTP_Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.DiY2YcXuu_5bwMbFqlTe_x4-0Msg6_Lmq3YVhsDr4LU"
        }

        response = client.post(
            "/postings", json.dumps(data), content_type="application/json", **header
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"message": "title has successfully posted"})

    def test_create_post_auth_error(self):
        client = Client()
        data = {
            "title": "title",
            "text": "text",
        }
        header = {
            "HTTP_Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.DiY2YcXuu_5bwMbFqlTe_x4-0Msg6_Lmq3YVhsDr4LU"
        }

        response = client.post(
            "/postings", json.dumps(data), content_type="application/json", **header
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"message": "AUTH_ERROR"})

    def test_create_post_invalid_token(self):
        client = Client()
        data = {
            "title": "title",
            "text": "text",
        }
        header = {
            "HTTP_Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.DiY2YcXuu_5bwMbFqlTe_x4-0Msg6_Lmq3YVhsDr4L"
        }

        response = client.post(
            "/postings", json.dumps(data), content_type="application/json", **header
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"message": "INVALID_TOKEN"})

    def test_create_post_key_error(self):
        client = Client()
        data = {
            "title": "title",
        }
        header = {
            "HTTP_Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.DiY2YcXuu_5bwMbFqlTe_x4-0Msg6_Lmq3YVhsDr4LU"
        }

        response = client.post(
            "/postings", json.dumps(data), content_type="application/json", **header
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "KEY_ERROR"})

    def test_put_post_success(self):
        client = Client()
        data = {
            "text": "text updated!",
        }
        header = {
            "HTTP_Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.DiY2YcXuu_5bwMbFqlTe_x4-0Msg6_Lmq3YVhsDr4LU"
        }

        response = client.put(
            "/postings/1", json.dumps(data), content_type="application/json", **header
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Title has successfully updated"})

    def test_put_post_forbidden(self):
        client = Client()
        data = {
            "text": "text updated!",
        }
        header = {
            "HTTP_Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Mn0.OLjKxY1ipx6vU8RSSkPtwE_d-0S9_qMVPg9syryaDQA"
        }

        response = client.put(
            "/postings/1", json.dumps(data), content_type="application/json", **header
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {"message": "FORBIDDEN"})

    def test_put_post_key_error(self):
        client = Client()
        data = {}
        header = {
            "HTTP_Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.DiY2YcXuu_5bwMbFqlTe_x4-0Msg6_Lmq3YVhsDr4LU"
        }

        response = client.put(
            "/postings/1", json.dumps(data), content_type="application/json", **header
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "KEY_ERROR"})

    def test_delete_post_success(self):
        client = Client()

        header = {
            "HTTP_Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.DiY2YcXuu_5bwMbFqlTe_x4-0Msg6_Lmq3YVhsDr4LU"
        }

        response = client.delete("/postings/1", **header)

        self.assertEqual(response.status_code, 204)

    def test_delete_post_forbidden(self):
        client = Client()

        header = {
            "HTTP_Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Mn0.OLjKxY1ipx6vU8RSSkPtwE_d-0S9_qMVPg9syryaDQA"
        }

        response = client.put("/postings/1", **header)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {"message": "FORBIDDEN"})

    def test_get_post_list_success(self):
        client = Client()

        response = client.get("/postings/list")

        posting = Posting.objects.get(id=1)

        result = {
            "result": {
                "count": 1,
                "postings": [
                    {
                        "id": posting.id,
                        "author": posting.author.name,
                        "title": posting.title,
                        "text": posting.text,
                        "created_time": posting.created_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
                        "updated_at": posting.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
                    }
                ],
            }
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), result)
