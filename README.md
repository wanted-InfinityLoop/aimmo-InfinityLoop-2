# 🎊 Wanted X Wecode PreOnBoarding Backend Course | 무한루프-2팀
원티드 1주차 기업 과제 : Aimmo Assignment Project
  ✅ Aimmo 기업 과제입니다.
  
# 팀 무한루프
- 1팀 : 손희정, 송치헌, 하예준
- 2팀 : (팀장)오지윤, 유동헌

# 역할
- 기능 별로 나누지 않고 모든 API를 함께 Pair Programming으로 구현하였습니다.

# TIL blog
- 오지윤 : https://odreystella.github.io/2021/11/03/TIL_01_django_swagger/
- 유동헌 : https://velog.io/@dhhyy/프리온보딩-1주차-TIL-과제-Aimmo-Assignment

# How to Start

### Required
- Python 3.8
- djongo==1.3.6
- MongoDB

### Add setting file
- Project폴더 안에 my_settings.py 파일 생성 후 내용 추가
- **`my_settings.py`** data structure
```py
(내용 삽입)
```

### 프로젝트 구조
```

├── config
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── utils.py
│   └── views.py
├── postings
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializer.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── users
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializer.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── manage.py
├── my_settings.py
├── README.md
├── requirements.txt
```
### Commnads
```shell
python manage.py makemigration
python manage.py migrate
python manage.py runserver
```

# Skills

### Backend
- Python3
- Djagno
- Django ORM

### Devops
- MongoDB

### Cowork (혹은 Cooperation)
- Git, Github Project
- Swagger2.0 (For API Document)
- Slack
- Google Meeting

# api 명세서

## users
1. 회원가입 API
    - POST : curl -X POST "http://127.0.0.1:8000/users/signup"
    - post 메서드를 사용, Body에 정보를 JSON에 담아 전달.
```python
Request
{
  "name": "이광수",
  "email": "runningman2@gmail.com",
  "password": "12341234aA!"
}
```
```python
Response body
{
  "message": "SUCCESS",
  "username": "이광수"
}
```
2. 로그인 API
    - POST : curl -X POST "http://127.0.0.1:8000/users/signin"
    - post 메서드를 사용, Body에 정보를 JSON에 담아 전달.
    - 기존 가입된 id와 password가 일치하면 향후 게시판 글쓰기 인가용 token 발행.
```python
Request
{
  "email": "runningman2@gmail.com",
  "password": "12341234aA!"
}
```
```python
Response body
{
  "message": "SUCCESS",
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Mn0.K3LT0TtAMaJLcY5jxz_5dwLh5ENBojWSCHkA49e_kgE",
  "username": "이광수"
}
```

## boards
1. board posting API
    - POST : curl -X POST "http://127.0.0.1:8000/postings"
    - title, content, tag 등을 json에 담아 전달.
```python
Request
{
  "title": "test_title",
  "text": "test_content",
  "category": 1
}
```
```python
Response
{
  "message": "test_title has successfully posted"
}
```
2. board detail posting API
    - POST : curl -X GET "http://127.0.0.1:8000/postings/3"
    - 인자로 보내지는 board_id에 해당하는 게시글 조회.
    - 전달하는 값은 board_id만 전달.
```python
Response Body
{
  "result": {
    "id": 3,
    "author": "지석진",
    "title": "testing post_2",
    "text": "testing post text",
    "category": "배송문의",
  }
}
```
3. board posting list API
    - POST : curl -X GET "http://127.0.0.1:8000/postings/list"
```python
Response Body
{
  "result": {
    "count": 4,
    "postings": [
      {
        "id": 6,
        "author": "지석진",
        "title": "testing post_6",
        "text": "testing post text",
        "category": "배송문의",
        "created_at": "2021-11-02T09:06:39.632Z",
        "updated_at": "2021-11-02T09:06:39.633Z"
      },
      {
        "id": 5,
        "author": "지석진",
        "title": "testing post_5",
        "text": "testing post text",
        "category": "배송문의",
        "created_at": "2021-11-02T09:06:32.121Z",
        "updated_at": "2021-11-02T09:06:32.121Z"
      },
      {
        "id": 4,
        "author": "지석진",
        "title": "testing post_4",
        "text": "testing post text",
        "category": "배송문의",
        "created_at": "2021-11-02T09:06:24.499Z",
        "updated_at": "2021-11-02T09:06:24.499Z"
      },
      {
        "id": 3,
        "author": "지석진",
        "title": "testing post_2",
        "text": "testing post text",
        "category": "배송문의",
        "created_at": "2021-11-02T09:02:04.461Z",
        "updated_at": "2021-11-02T09:02:04.461Z"
      }
    ]
  }
}
```
4. board posting list API
    - POST : users/boards/repost/1 HTTP/1.1
    - Host : http://127.0.0.1:8000/
```python
Request
{
    "message": [
    {
        "title"    : "수정 후",
        "content"  : "testing_content",
        "password" : 1234,
        "tag"      : 1
        }
    ]
}
```
```python
Response
{
    "message": "SUCCESS"
}
```
5. board posting delete API
    - POST : curl -X DELETE "http://127.0.0.1:8000/postings/7" 
    - Host : http://127.0.0.1:8000/
```python
Request Body

Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Mn0.K3LT0TtAMaJLcY5jxz_5dwLh5ENBojWSCHkA49e_kgE
(토큰으로 글 작성자 확인)

```
```python
Response
{
    "message": "SUCCESS"
}
```
6. board posting recomment API
    - POST : curl -X POST "http://127.0.0.1:8000/postings/comment/6"
```python
Request Body
(Authorization에 토큰 포함)
{
  "content": "19번에 대한 댓글입니다_1"
}
```
```python
Response
{
    "message": "SUCCESS"
}
```
7. board posing search API
    - curl -X POST "http://127.0.0.1:8000/postings/search
    - 작성자 명, 타이틀 명으로 게시판 내 게시글 검색 기능 구현
```python
Request Body
{
  "author": "지석진"
}
```
```python
Response
{
  "result": {
    "count": 4,
    "postings": [
      {
        "id": 3,
        "author": "지석진",
        "title": "testing post_2",
        "text": "testing post text",
        "category": "배송문의",
        "created_at": "2021-11-02T09:02:04.461Z",
        "updated_at": "2021-11-02T09:02:04.461Z"
      },
      {
        "id": 4,
        "author": "지석진",
        "title": "testing post_4",
        "text": "testing post text",
        "category": "배송문의",
        "created_at": "2021-11-02T09:06:24.499Z",
        "updated_at": "2021-11-02T09:06:24.499Z"
      },
      {
        "id": 5,
        "author": "지석진",
        "title": "testing post_5",
        "text": "testing post text",
        "category": "배송문의",
        "created_at": "2021-11-02T09:06:32.121Z",
        "updated_at": "2021-11-02T09:06:32.121Z"
      },
      {
        "id": 6,
        "author": "지석진",
        "title": "testing post_6",
        "text": "testing post text",
        "category": "배송문의",
        "created_at": "2021-11-02T09:06:39.632Z",
        "updated_at": "2021-11-02T09:06:39.633Z"
      }
    ]
  }
}
```
