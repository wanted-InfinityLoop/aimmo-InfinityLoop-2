# 🎊 Wanted X Wecode PreOnBoarding Backend Course | 무한루프-2팀
원티드 1주차 기업 과제 : Aimmo Assignment Project
  ✅ Aimmo 기업 과제입니다.
- [에이모 사이트](https://en.aimmo.ai/)
- [에이모 채용공고 링크](https://www.wanted.co.kr/wd/16937)
<br>
<br>

# 🔖 목차

- Team 소개
- 과제 내용
- 서버 주소
- 기술 환경 및 Tools
- 프로젝트 구조
- API 명세서 및 기능 설명
- 설치 및 실행 방법
<br>  
<br>  

# 🧑‍🤝‍🧑 Team 소개
- 팀 무한루프
  - 1팀 : 손희정, 송치헌, 하예준
  - 2팀 : (팀장)오지윤, 유동헌

| 이름 | 담당 기능 | 블로그 |
| :----------: | :-------------------------------: | :----: |
| 공통 | 초기환경 설정, DB 모델링, UnitTest, 배포, swagger 문서 작성, README.md 작성 | X |
| [유동헌](https://github.com/dhhyy)       | 게시글 카테고리, 검색, 대댓글 생성, 대댓글 조회(pagination), 조회수 | [1차 과제 TIL](https://velog.io/@dhhyy/프리온보딩-1주차-TIL-과제-Aimmo-Assignment) |            
| [오지윤](https://github.com/Odreystella) | 게시글 카테고리, 검색, 대댓글 생성, 대댓글 조회(pagination), 조회수 | [1차 과제 TIL](https://odreystella.github.io/2021/11/03/TIL_01_django_swagger/) |

- 기능 별로 나누지 않고 모든 API를 함께 Pair Programming으로 구현하였습니다.
<br>
<br>

# 📖 과제 내용

### **[필수 포함 사항]**

- README 작성
  - 프로젝트 빌드, 자세한 실행 방법 명시
  - 구현 방법과 이유에 대한 간략한 설명
  - 완료된 시스템이 배포된 서버의 주소
  - `Swagger`나 `Postman`을 통한 API 테스트할때 필요한 상세 방법
  - 해당 과제를 진행하면서 회고 내용 블로그 포스팅
- `Swagger`나 `Postman`을 이용하여 API 테스트 가능하도록 구현

### **[개발 요구 사항]**

- 에이모 선호 기술스택: `python flask`, `mashmallow`, `mongoengine`
- 필수 사용 데이터베이스: `mongodb`

### **[기능 개발]**

✔️ **REST API 기능**

- 원티드 지원 과제 내용 포함(게시판 CRUD API)
- 게시글 카테고리
- 게시글 검색
- 대댓글 (1 depth)
    - 대댓글 pagination
- 게시글 읽힘 수
    - 같은 User가 게시글을 읽는 경우 count 수 증가하면 안 됨
- Rest API 설계
- Unit Test
- 1000만건 이상의 데이터를 넣고 성능테스트 진행 결과 필요
<br>
<br>

# ➡️ Build(AWS EC2)

API URL: http://3.35.218.65:8000/

<br>

# ⚒️ 기술 환경 및 Tools

- Back-End: `Python 3.9.7`, `Django 3.2.9`
- Database: `mongodb` 
- Deploy: `AWS EC2`, `Docker`
- ETC: `Git`, `Github`, `Swagger`

<br>

# 🌲 프로젝트 구조
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
├── Dockerfile
├── my_settings.py
├── README.md
├── requirements.txt
```
<br>

# 🔖 API 명세서

[Swagger API Document 보러가기](http://3.35.218.65:8000/swagger/)


### 👉 회원가입 / 로그인

[ 회원가입 API ]

1. 유저 인증 처리를 위해 회원가입 API
2. 유저의 이름과 이메일, 비밀번호를 요청 본문에 담으면 가입된다.

- Method: POST

```python
"http://3.35.218.65:8000/users/signup"
```

- parameter : request_body

```python
{
    "name": "이광수",
    "email": "runningman2@gmail.com",
    "password": "12341234aA!"
}
```

- response
```python
{
    "message": "SUCCESS",
    "username": "이광수"
}
```
<br>

[ 로그인 API ]

1. 유저의 이메일과 비밀번호를 통해서 User Auth 검증 한다.
2. 로그인 성공 시, 인가용 access_token을 반환한다.

- Method: POST

```python
"http://3.35.218.65:8000/users/signin"
```

- parameter : request_body

```python
{
    "email": "runningman2@gmail.com",
    "password": "12341234aA!"
}
```

- response
```python
{
    "message": "SUCCESS",
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Mn0.OLjKxY1ipx6vU8RSSkPtwE_d-0S9_qMVPg9syryaDQA",
    "username": "이광수"
}
```

### 👉 게시판 CRUD API

#### [ 게시글 작성 API] 

1. 헤더로 user의 access_token을 전달한다.
2. 요청 본문에 글 제목, 내용, 카테고리를 작성하여 요청한다.

- Method: POST

```python
"http://3.35.218.65:8000/postings"
```
- header : Bearer token
- parameter : request_body

```python
{
    "title": "test_title",
    "text": "test_content",
    "category": 1
}
```

- response
```python
{
    "message": "test_title has successfully posted"
}
```
<br>

#### [ 게시글 상세 조회 API]

1. 헤더로 user의 access_token을 전달한다.
2. path_parameter에 해당하는 게시글이 조회된다.
3. access_token으로 같은 유저가 게시글의 읽는 경우 조회수가 증가하지 않는다.

- Method: GET

```python
"http://3.35.218.65:8000/postings/13"
```
- header : Bearer token
- parameter : path_parameter

- response
```python
{
  "result": {
    "id": 13,
    "author": "이광수",
    "title": "test_title",
    "text": "test_content",
    "category": "공지사항",
    "created_at": "2021-12-23 07:30",
    "updated_at": "2021-12-23 07:38",
    "count": 4
  }
}
```
<br>

#### [ 게시글 목록 조회 API]

1. 기본적으로 10개의 게시글을 조회한다. 

- Method: GET

```python
"http://3.35.218.65:8000/postings/list"
```

- response
```python
{
  "result": {
    "count": 10,
    "postings": [
      {
        "id": 13,
        "author": "이광수",
        "title": "test_title",
        "text": "test_content",
        "category": "공지사항",
        "created_at": "2021-12-23T07:30:52.607Z",
        "updated_at": "2021-12-23T07:38:16.072Z"
      },
      {
        "id": 12,
        "author": "에이모1",
        "title": "docker success",
        "text": "good",
        "category": "공지사항",
        "created_at": "2021-12-22T06:37:32.229Z",
        "updated_at": "2021-12-22T06:47:57.548Z"
      },
      ...
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
<br>

#### [ 게시글 수정 API]

1. 헤더로 user의 access_token을 전달한다.
2. 요청 본문에 제목, 수정할 내용, 카테고리를 전달한다.
3. path_parameter에 해당하는 게시글의 내용이 수정된다.

- Method: PUT

```python
"http://3.35.218.65:8000/postings/13"
```
- header : Bearer token
- parameter : request_body, path_parameter

```python
{
    "title": "test_title",
    "text": "test_content_change",
    "category": 1
}
```

- response
```python
{
  "result": {
    "id": 13,
    "author": "이광수",
    "title": "test_title",
    "text": "test_content_change",
    "category": "공지사항",
    "created_at": "2021-12-23 07:30",
    "updated_at": "2021-12-23 07:47",
    "count": 5
  }
}
```
<br>

#### [ 게시글 삭제 API]

1. 헤더로 user의 access_token을 전달한다.
2. path_parameter에 해당하는 게시글이 삭제된다.

- Method: DELETE

```python
"http://3.35.218.65:8000/postings/13"
```
- header : Bearer token
- parameter : path_parameter

- response
```python
{
    "message": "test_title has successfully deleted"
}
```
<br>

### 👉 대댓글 생성 API

1. 헤더로 user의 access_token을 전달한다.
2. path_parameter로 게시글 id를 전달한다.
3. query_parameter인 comment_id가 없으면 댓글이 생성되고, 댓글의 id를 전달하면 해당 댓글에 대댓글이 생성된다.

- Method: POST

```python
"http://3.35.218.65:8000/postings/12/comment?comment_id=41"
```
- header : Bearer token
- parameter : request_body, path_parameter, query_parameter

```python
{
  "content": "12번에 게시글 41번 댓글에 대한 대댓글입니다_1"
}
```

- response
```python
{
    "message": "CREATE_RECOMMENT"
}
```
<br>

### 👉 대댓글 조회 API

1. path_parameter로 조회할 게시글 id를 전달한다.
2. query_parameter인 parent_comment_id가 없으면 해당 게시글의 댓글이 조회되고, 댓글 id를 전달하면 해당 댓글의 대닷글을 조회할 수 있다.
3. query_parameter로 limit, offset를 전달하면 페이징 처리 후 조회된다.

- Method: GET

```python
"http://3.35.218.65:8000/postings/12/commentlist?parent_comment_id=41&limit=10&offset=0"
```
- parameter : path_parameter, query_parameter

- response
```python
{
  "message": [
    {
      "content": "도커 짱",
      "user": "runningman2@gmail.com",
      "posting_title": "docker success",
      "parent_comment_id": 41
    },
    {
      "content": "도커 짱",
      "user": "aimmo@naver.com",
      "posting_title": "docker success",
      "parent_comment_id": 41
    },
    {
      "content": "댓글 댓글",
      "user": "aimmo@naver.com",
      "posting_title": "docker success",
      "parent_comment_id": 41
    }
  ]
}
```
<br>

### 👉 게시글 검색 API

1. query_parameter로 검색할 키워드를 전달한다(키워드: post).
2. 게시글 작성자, 제목, 내용으로 검색이 가능하다.

- Method: GET

```python
"http://3.35.218.65:8000/postings/search?keyword=post"
```
- parameter : query_parameter

- response
```python
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
        "created_at": "2021-11-02 09:02",
        "updated_at": "2021-11-02 09:02"
      },
      {
        "id": 4,
        "author": "지석진",
        "title": "testing post_4",
        "text": "testing post text",
        "category": "배송문의",
        "created_at": "2021-11-02 09:06",
        "updated_at": "2021-11-02 09:06"
      },
      {
        "id": 5,
        "author": "지석진",
        "title": "testing post_5",
        "text": "testing post text",
        "category": "배송문의",
        "created_at": "2021-11-02 09:06",
        "updated_at": "2021-11-02 09:06"
      },
      {
        "id": 6,
        "author": "지석진",
        "title": "testing post_6",
        "text": "testing post text",
        "category": "배송문의",
        "created_at": "2021-11-02 09:06",
        "updated_at": "2021-11-02 09:06"
      }
    ]
  }
}
```

<br>

# 🔖 설치 및 실행 방법

### 로컬 및 테스트용

1. 해당 프로젝트를 clone하고, 프로젝트로 들어간다.

```bash
$ https://github.com/wanted-InfinityLoop/aimmo-InfinityLoop-2.git .
```

2. 가상환경으로 miniconda를 설치한다. [Go](https://docs.conda.io/en/latest/miniconda.html)

```bash
$ conda create -n aimmo python=3.9
$ conda actvate aimmo
```

3. 가상환경 생성 후, requirements.txt를 설치한다.

```bash
$ pip install -r requirements.txt

Django==3.2.9
django-cors-headers==3.10.0
bcrypt==3.2.0
PyJWT==2.3.0
djangorestframework==3.12.4
drf-yasg==1.20.0
djongo==1.3.6
whitenoise==5.3.0
gunicorn==20.1.0
django-extensions==3.1.5
```

4. migrate 후 로컬 서버 가동

```bash
$ python manage.py migrate
$ python manage.py runserver
```

### 배포용

1. 배포 서버에서 이미지를 pull 받는다.
```bash
$ sudo docker pull ojo1001/aimmo:0.1.0 
```

2. 이미지가 잘 받아졌는지 확인한다.
```bash
$ sudo docker images 
```

3. 컨테이너 실행하기
```bash
$ sudo docker run --name aimmo -d -p 8000:8000 ojo1001/aimmo:0.1.0 
```

4. 실행중인 컨테이너 확인하기
```bash
$ sudo docker ps 
```

5. Swagger API 문서 들어가서 API 테스트하기
```bash
http://3.35.218.65:8000/swagger/
```
