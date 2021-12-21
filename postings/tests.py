import json
import bcrypt
import jwt

from django.test      import TestCase, Client
from django.db.models import Q

from postings.models import Posting, Category, Comment
from users.models    import User
from my_settings     import MY_SECRET_KEY, ALGORITHM


class PostingView(TestCase):
    def setUp(self):
        self.client = Client()

        User.objects.create(id=1, name="Stella", email="jun10@naver.com", password="abcd1234"),

        self.access_token1 = jwt.encode({"id": 1}, MY_SECRET_KEY, ALGORITHM)

        Category.objects.create(id=1, name="python")

        Posting.objects.bulk_create(
            [
                Posting(id=1, title="Title1", text="text", author_id=1, category_id=1),
                Posting(id=2, title="Title1", text="text", author_id=1, category_id=1),
            ]
        )

    def tearDown(self):
        Posting.objects.all().delete()
        Category.objects.all().delete()
        User.objects.all().delete()

    def test_get_posting_success(self):
        header = {"HTTP_Authorization": f"Bearer {self.access_token1}"}

        response = self.client.get("/postings/1", content_type="application/json", **header)

        posting = Posting.objects.get(id=1)

        result = {
            "id": posting.id,
            "author": posting.author.name,
            "title": posting.title,
            "text": posting.text,
            "category": posting.category.name,
            "created_at": posting.created_at.strftime("%Y-%m-%d %H:%M"),
            "updated_at": posting.updated_at.strftime("%Y-%m-%d %H:%M"),
            "count": posting.count
        }

        self.assertEqual(response.json(), {"result": result})
        self.assertEqual(response.status_code, 200)

    def test_get_posting_not_found(self):
        header = {"HTTP_Authorization": f"Bearer {self.access_token1}"}

        posting_id = 3
        response = self.client.get(f"/postings/{posting_id}", content_type="application/json", **header)
        
        self.assertEqual(response.json(), {"message" : f"POSTING_{posting_id}_NOT_FOUND"})
        self.assertEqual(response.status_code, 404)


class SearchView(TestCase):
    def setUp(self):
        self.client = Client()

        User.objects.create(id=1, name="Stella", email="jun10@naver.com", password="abcd1234"),
        User.objects.create(id=2, name="Stella", email="jun10@naver.co.kr", password="abcd1234")
        
        Category.objects.create(id=1, name="python")
        Category.objects.create(id=2, name="mysql")

        Posting.objects.bulk_create(
            [
                Posting(id=1, title="Title1", text="text", author_id=1, category_id=1),
                Posting(id=2, title="Title1", text="text", author_id=1, category_id=1),
                Posting(id=3, title="Title3", text="text", author_id=2, category_id=2),
                Posting(id=4, title="Title4", text="text4", author_id=2, category_id=2),
                Posting(id=5, title="Title5", text="text5", author_id=1, category_id=2),
            ]
        )

    def tearDown(self):
        Posting.objects.all().delete()
        Category.objects.all().delete()
        User.objects.all().delete()

    def test_get_search_success(self):
        keyword = "Title1"

        response = self.client.get(f"/postings/search?keyword={keyword}", content_type="application/json")

        postings = Posting.objects.filter(Q(author__name=keyword)|Q(title__icontains=keyword)|Q(text__icontains=keyword))

        result = {
            "count": len(postings),
            "postings": [
                {
                    "id": posting.id,
                    "author": posting.author.name,
                    "title": posting.title,
                    "text": posting.text,
                    "category": posting.category.name,
                    "created_at": posting.created_at.strftime("%Y-%m-%d %H:%M"),
                    "updated_at": posting.updated_at.strftime("%Y-%m-%d %H:%M"),
                }
                for posting in postings
            ]
        }

        self.assertEqual(response.json(), {"result": result})
        self.assertEqual(response.status_code, 200)
    
    def test_get_posting_not_found(self):
        keyword = "post"
        
        response = self.client.get(f"/postings/search?keyword={keyword}", content_type="application/json")

        self.assertEqual(response.json(), {"message" : "NOT_FOUND_POSTING"})
        self.assertEqual(response.status_code, 400)


class CommentViewTest(TestCase):
    def setUp(self):
        self.client      = Client()
        password        = "12341234aA!"
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        
        User.objects.create(
            id       = 1, 
            name     = "지석진", 
            email    = "test1@gmail.com", 
            password = hashed_password
            )
        
        Category.objects.create(
            id   = 1,
            name = "공지사항"
        )
        
        Posting.objects.create(
            id        = 1, 
            title     = "testing_title", 
            text      = "testing_content", 
            author_id = 1
            )
        
        Comment.objects.create(
            id                = 1,
            content           = "1번 글에 대한 댓글",
            user              = User.objects.get(id=1),
            posting           = Posting.objects.get(id=1),
            parent_comment_id = 0
        )
        
        self.user_token_1 = jwt.encode(
            {
                "id" : 1
            }, 
            MY_SECRET_KEY,
            ALGORITHM
        )

    def tearDown(self):
        Comment.objects.all().delete()
        Posting.objects.all().delete()
        Category.objects.all().delete()
        User.objects.all().delete()
        
    def test_post_create_comment_success(self):
        header = {"HTTP_Authorization":f"Bearer {self.user_token_1}"}
        data   = {
            "content" : "posting_1번 글에 대한 댓글"
        }
        
        response = self.client.post(
            "/postings/1/comment",
            json.dumps(data),
            content_type="application/json",
            **header
            )
        
        self.assertEqual(response.json(), {"message" : "CREATE_COMMENT"})
        self.assertEqual(response.status_code, 201)

    def test_post_create_comment_not_content_fail(self):
        header = {"HTTP_Authorization":f"Bearer {self.user_token_1}"}
        data   = {
            "content" : ""
        }
        
        response = self.client.post(
            "/postings/1/comment",
            json.dumps(data),
            content_type="application/json",
            **header
            )
        
        self.assertEqual(response.json(), {"message" : "CHECK_YOUR_INPUT"})
        self.assertEqual(response.status_code, 400)

    def test_post_create_comment_not_posting_id_fail(self):
        header = {"HTTP_Authorization":f"Bearer {self.user_token_1}"}
        data   = {
            "content" : "posting_1번 글에 대한 댓글"
        }
        
        response = self.client.post(
            "/postings/10/comment",
            json.dumps(data),
            content_type="application/json",
            **header
            )
        
        self.assertEqual(response.json(), {"message" : "NOT_POSTING_ID"})
        self.assertEqual(response.status_code, 400)

    def test_post_create_recomment_success(self):
        header = {"HTTP_Authorization":f"Bearer {self.user_token_1}"}
        data   = {
            "content" : "posting_1번 글에 대한 댓글"
        }
        
        response = self.client.post(
            "/postings/1/comment?comment_id=1",
            json.dumps(data),
            content_type="application/json",
            **header
            )
        
        self.assertEqual(response.json(), {"message" : "CREATE_RECOMMENT"})
        self.assertEqual(response.status_code, 201)
        
        
class CommentListViewTest(TestCase):
    def setUp(self):
        self.client     = Client()
        password        = "12341234aA!"
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        
        User.objects.create(
            id       = 1, 
            name     = "지석진", 
            email    = "test1@gmail.com", 
            password = hashed_password
            )
        
        Category.objects.create(
            id   = 1,
            name = "공지사항"
        )
        
        posting_1 = Posting.objects.create(
            id        = 1, 
            title     = "testing_title", 
            text      = "testing_content", 
            author_id = 1
            )
        
        Comment.objects.create(
            id                = 1,
            content           = "1번 글에 대한 댓글",
            user              = User.objects.get(id=1),
            posting           = posting_1,
            parent_comment_id = 0
        )

    def tearDown(self):
        Comment.objects.all().delete()
        Posting.objects.all().delete()
        Category.objects.all().delete()
        User.objects.all().delete()
        
    def test_comment_list_view_success(self):
        
        comment_list = [
            {
                "content"           : "1번 글에 대한 댓글",
                "user"              : "test1@gmail.com",
                "posting_title"     : "testing_title",
                "parent_comment_id" : 0
                }
            ]
        
        response = self.client.get(
            "/postings/1/commentlist?parent_comment_id=0&limit=5&offset=0"
            )
        
        self.assertEqual(response.json(), {"message" : comment_list}) 
        self.assertEqual(response.status_code, 200)
