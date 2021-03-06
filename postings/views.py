import json

from django.core import paginator

from rest_framework.views import APIView
from drf_yasg.utils       import swagger_auto_schema
from drf_yasg             import openapi

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q

from users.models import User
from .models      import Category, Posting, Comment
from core.utils   import login_decorator
from .serializer  import PostingSerializer, CommentSerializer
from django.core.paginator import Paginator


class PostingCreateView(APIView):
    '''
    # 게시글 작성
    '''

    parameter_token = openapi.Parameter(
        "Authorization",
        openapi.IN_HEADER,
        description = "access_token",
        type = openapi.TYPE_STRING
    )
    @swagger_auto_schema(request_body = PostingSerializer, manual_parameters = [parameter_token])
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = request.user

            posting      = Posting.objects.create(
                title    = data["title"],
                text     = data["text"],
                category = Category.objects.get(id=data["category"]),
                author   = user,
            )

            posting.count += 1
            posting.save()

            return JsonResponse(
                {"message": f"{posting.title} has successfully posted"}, status=201
            )
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)


class PostingView(APIView):
    
    '''
    # 게시글 불러오기 / 게시글 detail view
    '''

    parameter_token = openapi.Parameter(
        "Authorization",
        openapi.IN_HEADER,
        description = "access_token",
        type = openapi.TYPE_STRING
    )

    @swagger_auto_schema(manual_parameters = [parameter_token])
    @login_decorator
    def get(self, request, posting_id):
        if not Posting.objects.filter(id=posting_id).exists():
            return JsonResponse(
                {"message": f"POSTING_{posting_id}_NOT_FOUND"}, status=404
            )

        posting = Posting.objects.get(id=posting_id)

        if request.user != posting.author:
            posting.count += 1

        else:
            posting.count = posting.count

        posting.save()

        result = {
            "id"         : posting.id,
            "author"     : posting.author.name,
            "title"      : posting.title,
            "text"       : posting.text,
            "category"   : posting.category.name,
            "created_at" : posting.created_at.strftime("%Y-%m-%d %H:%M"),
            "updated_at" : posting.updated_at.strftime("%Y-%m-%d %H:%M"),
            "count"      : posting.count
        }
        return JsonResponse({"result": result}, status=200)
    
    '''
    # 게시글 수정
    '''
    
    parameter_token = openapi.Parameter(
        "Authorization",
        openapi.IN_HEADER,
        description = "access_token",
        type = openapi.TYPE_STRING
    )

    @swagger_auto_schema(request_body = PostingSerializer, manual_parameters = [parameter_token])
    @login_decorator
    def put(self, request, posting_id):
        try:
            if not Posting.objects.filter(id=posting_id).exists():
                return JsonResponse(
                    {"message": f"POSTING_{posting_id}_NOT_FOUND"}, status=404
                )

            posting = Posting.objects.get(id=posting_id)

            if request.user.id != posting.author_id:
                return JsonResponse({"message": "FORBIDDEN"}, status=403)

            data         = json.loads(request.body)
            posting.text = data["text"]
            
            posting.save()

            return JsonResponse(
                {"message": f"{posting.title} has successfully updated"}, status=200
            )
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)


    '''
    # 게시글 삭제
    '''

    @swagger_auto_schema(manual_parameters = [parameter_token])
    @login_decorator
    def delete(self, request, posting_id):
        try:
            if not Posting.objects.filter(id=posting_id).exists():
                return JsonResponse(
                    {"message": f"POSTING_{posting_id}_NOT_FOUND"}, status=404
                )

            posting = Posting.objects.get(id=posting_id)

            if request.user.id != posting.author_id:
                return JsonResponse({"message": "FORBIDDEN"}, status=403)

            posting.delete()
            

            return JsonResponse(
                {"message": f"{posting.title} has successfully deleted"}, status=204
            )

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)


class PostingListView(APIView):
    '''
    # 게시글 목록 불러오기
    '''

    def get(self, request):
        try:
            OFFSET = int(request.GET.get("offset", 0))
            LIMIT  = int(request.GET.get("limit", 10))

            postings = Posting.objects.all().order_by("-created_at")[
                OFFSET : OFFSET + LIMIT
            ]

            result = {
                "count": len(postings),
                "postings": [
                    {
                        "id"         : posting.id,
                        "author"     : posting.author.name,
                        "title"      : posting.title,
                        "text"       : posting.text,
                        "category"   : posting.category.name,
                        "created_at" : posting.created_at,
                        "updated_at" : posting.updated_at,
                    }
                    for posting in postings
                ],
            }

            return JsonResponse({"result": result}, status=200)
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)


class CommentView(APIView):

    '''
    # 댓글, 대댓글 생성하기
    '''

    parameter_token = openapi.Parameter(
        "Authorization",
        openapi.IN_HEADER,
        description = "access_token",
        type = openapi.TYPE_STRING
    )
    
    query_comment_id = openapi.Parameter(
        "comment_id",
        openapi.IN_QUERY,
        description = "댓글 ID를 넣어주세요",
        type = openapi.TYPE_INTEGER
    )
    
    error_field = openapi.Schema(
        'error', # 제목 
        description = '입력 부분을 수정해주세요', # 설명
        type=openapi.TYPE_STRING # 타입
    )
    
    @swagger_auto_schema(request_body = CommentSerializer, 
                        manual_parameters = [parameter_token, query_comment_id],
                        responses = {
                            400 : error_field # responses 
                            }
                        )
    @login_decorator
    def post(self, request, posting_id):
        data       = json.loads(request.body)
        user       = request.user
        content    = data.get("content", None)
        comment_id = int(request.GET.get("comment_id", 0))
        
        if not content:
            return JsonResponse({"message" : "CHECK_YOUR_INPUT"}, status=400)
        
        if not Posting.objects.filter(id=posting_id).exists():
            return JsonResponse({"message" : "NOT_POSTING_ID"}, status=400)
        
        posting = Posting.objects.get(id=posting_id)
        
        if not comment_id:
            
            Comment.objects.create(
                content           = content,
                user              = user,
                posting           = posting,
                parent_comment_id = 0
            )
            
            return JsonResponse({"message" : "CREATE_COMMENT"}, status=201)
            
        Comment.objects.create(
            content           = content,
            user              = user,
            posting           = posting,
            parent_comment_id = Comment.objects.get(id=comment_id).id
        )
        
        return JsonResponse({"message" : "CREATE_RECOMMENT"}, status=201)


class CommentListView(APIView):

    '''
    # 댓글, 대댓글 조회하기
    '''

    query_parent_comment_id = openapi.Parameter(
        "parent_comment_id",
        openapi.IN_QUERY,
        description = "parent_comment_id",
        type = openapi.TYPE_INTEGER
    )
    query_limit = openapi.Parameter(
        "limit",
        openapi.IN_QUERY,
        description = "limit",
        type = openapi.TYPE_INTEGER
    )
    query_offset = openapi.Parameter(
        "offset",
        openapi.IN_QUERY,
        description = "offset",
        type = openapi.TYPE_INTEGER
    )
    
    @swagger_auto_schema(manual_parameters = [query_parent_comment_id, query_limit, query_offset])
    def get(self, request, posting_id):
        parent_comment_id = request.GET.get("parent_comment_id",0)
        offset            = int(request.GET.get("offset", 0))
        limit             = int(request.GET.get("limit", 10))
        
        if parent_comment_id == 0:
            all_comments = Comment.objects.filter(posting_id=posting_id, parent_comment_id=0).select_related("user")
            
        else:
            all_comments = Comment.objects.filter(posting_id=posting_id, parent_comment_id=parent_comment_id).select_related("user")
        
        comments = all_comments[offset:offset+limit]
        
        comment_list = [
            {
                "content"           : comment.content,
                "user"              : comment.user.email,
                "posting_title"     : comment.posting.title,
                "parent_comment_id" : comment.parent_comment_id
                } for comment in comments
            ]
        return JsonResponse({"message" : comment_list}, status=200)


class SearchView(APIView):
    '''
    # 작성자 또는 제목으로 검색하기
    '''

    query_keyword = openapi.Parameter(
        "keyword",
        openapi.IN_QUERY,
        description = "검색할 작성자 또는 제목 또는 내용을 입력하세요",
        type = openapi.TYPE_STRING
    )

    @swagger_auto_schema(operation_description="검색하기", manual_parameters = [query_keyword])
    def get(self, request):
            try:
                keyword = request.GET.get("keyword")

                postings = Posting.objects.filter(Q(author__name=keyword)|\
                    Q(title__icontains=keyword)|\
                        Q(text__icontains=keyword))\
                    .select_related("category", "author")

                if not postings:
                    return JsonResponse({"message" : "NOT_FOUND_POSTING"}, status=400)

                result = {
                    "count": len(postings),
                    "postings": [
                        {
                            "id"         : posting.id,
                            "author"     : posting.author.name,
                            "title"      : posting.title,
                            "text"       : posting.text,
                            "category"   : posting.category.name,
                            "created_at" : posting.created_at.strftime("%Y-%m-%d %H:%M"),
                            "updated_at" : posting.updated_at.strftime("%Y-%m-%d %H:%M"),
                        } 
                        for posting in postings
                    ],
                }

                return JsonResponse({"result": result}, status=200)

            except ValueError:
                return JsonResponse({"message" : "VALUE_ERROR"}, status=400)
