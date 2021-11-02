# Simple Blog CRUD APIs 

##  About the Project <br>

### Built with
- Python
- Django
- SQLite3
  
<br>


# API Spec

## User APIs

### User Schema
``` Text
{
    id: int,       
    name: string,      // 이름
    email: string,     // 이메일
    password: string   // 비밀번호 
}
```
<br>

## 회원가입 
새로운 회원 정보를 생성한다. 비밀번호는 숫자, 문자, 특수문자의 조합이며, 8자리 이상이어햐 한다.

### URL
``` Text
POST /users/signup
Host: localhost
Content-type: application/json
```

### Parameter
``` Json
{
    "name": "string" 
    "email": "string"
    "password" : "string"
}
```

### Response
``` Json
{
    "message" : "SUCCESS",
    "username" : "username"
}
```

<br>

## 로그인 
회원 정보를 통해 접속한다. 로그인 성공 시, 유저의 이름과 토큰을 반환받는다.

### URL
``` Text
POST /users/signin
Host: localhost
Content-type: application/json
```

### Parameter
``` Json
{
    "email": "string"
    "password" : "string"
}
```

### Response
``` Json
{
    "message" : "SUCCESS",
    "token" : "token-example",
    "username": "username"
}
```
## Posting APIs

### Posting Schema
``` Text
{
    id: int,       
    title: string,          // 제목
    text: string,           // 내용
    created_time: datetime  // 생성 시간
    updated_at: datetime    // 수정 시간
    author: int             // 작성 정보 참조
}
```
<br>

## 포스팅 작성
새로운 프스팅을 생성한다.

### URL
``` Text
POST /postings
Host: localhost
Authorization: Bearer {ACCESS_TOKEN}
Content-type: application/json
```

### Parameter
``` Json
{
    "title": "post title",
    "text": "post text",
}
```

### Response
``` Json
{
    "message" : "post title has successfully posted"
}
```
<br>

## 포스팅 불러오기
포스팅 정보를 불러온다.

### URL
``` Text
POST /postings/{posting_id}
Host: localhost
```

### Response
``` Json
{
    "result": {
        "id": 1,
        "author": "username",
        "title": "posting title",
        "text": "posting text",
        "created_time": "2021-10-20T08:32:18.134Z",
        "updated_at": "2021-10-20T08:32:18.135Z"
    }
}
```

<br>

## 포스팅 수정하기
포스팅 본문을 수정한다.

### URL
``` Text
POST /postings/{posting_id}
Host: localhost
Authorization: Bearer {ACCESS_TOKEN}
Content-type: application/json
```

### Parameter
``` Json
{
    "text": "post text",
}
```

### Response
``` Json
{
  "message" : "post title has successfully updated"
}
```

<br>

## 포스팅 삭제하기
포스팅 정보를 삭제한다.

### URL
``` Text
POST /postings/{posting_id}
Host: localhost
Authorization: Bearer {ACCESS_TOKEN}
```

### Response
``` Json
{
  "message" : "post title has successfully deleted"
}
```

<br>

## 포스팅 목록 불러오기
포스팅 데이터 목록을 불러온다. 불러온 포스팅 정보의 개수와 포스팅 정보가 반환된다. <br> 
Offset과 limit을 통해 pagination 구현이 가능하다.

### URL
``` Text
POST /postings/list
Host: localhost
```

### Response
``` Json
{
    "result": {
        "count": 1,
        "postings": [
            {
                "id": 1,
                "author": "username",
                "title": "posting title",
                "text": "posting text",
                "created_time": "2021-10-20T08:32:18.134Z",
                "updated_at": "2021-10-20T08:32:18.135Z"
            }
        ]
    }
}
```
