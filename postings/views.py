import json

from django.db.models.fields import PositiveIntegerField

from rest_framework.views import APIView
from drf_yasg.utils       import swagger_auto_schema
from drf_yasg             import openapi

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q

from users.models import User
from .models      import Category, Posting, Comment
from core.utils   import login_decorator
from .serializer  import PostingSerializer, CommentSerializer, SearchSerializer

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

            return JsonResponse(
                {"message": f"{posting.title} has successfully posted"}, status=201
            )
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        
class PostingView(APIView):
    
    '''
    # 게시글 불러오기 / 게시글 detail view
    '''

    def get(self, request, posting_id):
        if not Posting.objects.filter(id=posting_id).exists():
            return JsonResponse(
                {"message": f"POSTING_{posting_id}_NOT_FOUND"}, status=404
            )

        posting = Posting.objects.get(id=posting_id)

        result = {
            "id"         : posting.id,
            "author"     : posting.author.name,
            "title"      : posting.title,
            "text"       : posting.text,
            "category"   : posting.category.name,
            "created_at" : posting.created_at,
            "updated_at" : posting.updated_at,
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
            
            # 확인 필요
            return JsonResponse(
                {"message": f"{posting.title} has successfully deleted"}, status=204
            )
            
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

class PostingListView(APIView):
    '''
    # 게시글 목록 불러오기
    '''
    
    # pasination 확인 필요 in swagger
     
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
    @swagger_auto_schema(request_body = CommentSerializer, manual_parameters = [parameter_token])
    @login_decorator
    def post(self, request, posting_id):
        try:
            data       = json.loads(request.body)
            user       = request.user
            content    = data.get("content", None)
            comment_id = data.get("comment_id", None)
            
            if not (content and posting_id):
                return JsonResponse({"message" : "CHECK_YOUR_INPUT"}, status=400)
            
            if not Posting.objects.filter(id=posting_id).exists():
                return JsonResponse({"message" : "NOT_POSTING_ID"}, status=400)
            
            posting = Posting.objects.get(id=posting_id)
            
            if not comment_id:
                
                Comment.objects.create(
                    content        = content,
                    user           = user,
                    posting        = posting,
                    parent_comment_id = 0
                )
                
                return JsonResponse({"message" : "POST COMMENT"}, status=200)
                
            Comment.objects.create(
                content           = content,
                user              = user,
                posting           = posting,
                parent_comment_id = Comment.objects.get(id=comment_id).id
            )
            
            return JsonResponse({"message" : "POST RECOMMENT"}, status=200)
            
        except KeyError:
            return JsonResponse({"key error" : "KEY_ERROR"}, status=400)


class CommentListView(APIView):
    
    '''
    # 댓글, 대댓글 조회하기
    '''
    
    # CommentView, 
    
    
    # comment, parent_comment_id를 식별해서 이에 속하는 글을 조회할 수 있게 한다
    # comment   = parent_id = 0
    # recomment = parent_id = comment_id
    # posting_id
    
    # CommentView 클래스에 하나로 하는 것 알아보기
    # Pagination 
    # drf - yasg, parameter 설정 알아보기
    
    parameter_token = openapi.Parameter(
        "parent_comment_id",
        openapi.IN_QUERY,
        description = "parent_comment_id",
        type = openapi.TYPE_STRING
    )
    @swagger_auto_schema(manual_parameters = [parameter_token])
    def get(self, request, posting_id):
        parent_comment_id = int(request.GET.get("parent_comment_id","0"))
        
        if parent_comment_id == 0:
            all_comments = Comment.objects.filter(posting_id=posting_id, parent_comment_id=0)
            
        else:
            all_comments = Comment.objects.filter(posting_id=posting_id, parent_comment_id=parent_comment_id)
        
        comments = all_comments
        
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
    #1. 검색어를 가져온다.
    #2. 검색어를 해당 모델에서 필터링한다.
    #3. 결과에 따라 응답한다.
    @swagger_auto_schema(operation_description="검색하기", request_body = SearchSerializer)
    def post(self, request):
            try:
                data    = json.loads(request.body)
                keyword = data.get("author", None)
                
                if not keyword:
                    return JsonResponse({"message" : "CHECK_YOUR_INPUT"}, status=400)
                
                if not Posting.objects.filter(Q(author__name=keyword)|Q(title__icontains=keyword)|Q(text__icontains=keyword)).exists():
                    return JsonResponse({"message" : "NOT_FOUND_POSTING"}, status=400)
                
                postings = Posting.objects.filter(Q(author__name=keyword)|Q(title__icontains=keyword)|Q(text__icontains=keyword))

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

            except postings.DoesNotExist:
                return JsonResponse({"model error" : "MODEL_ERROR"}, status=400)

            except KeyError:
                return JsonResponse({"key error" : "KEY_ERROR"}, status=400)
            
            
# test_param = openapi.Parameter('test', openapi.IN_QUERY, description="test manual param", type=openapi.TYPE_BOOLEAN)
# user_response = openapi.Response('response description', UserSerializer)

# @swagger_auto_schema(method='get', manual_parameters=[test_param], responses={200: user_response})
# @swagger_auto_schema(methods=['put', 'post'], request_body=UserSerializer)
# @api_view(['GET', 'PUT', 'POST'])
# def user_detail(request, pk):
#     ...
