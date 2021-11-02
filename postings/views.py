import json

from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.http import JsonResponse
from django.views import View

from .models import Category, Posting, Comment
from core.utils import login_decorator
from .serializer import PostingSerializer, CommentSerializer

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
            data    = json.loads(request.body)
            user    = request.user
            content = data.get('content', None)
            
            if not (content and posting_id):
                return JsonResponse({"message" : "CHECK_YOUR_INPUT"}, status=400)
            
            if not Posting.objects.filter(id=posting_id).exists():
                return JsonResponse({"message" : "NOT_POSTING_ID"}, status=400)
            
            posting = Posting.objects.get(id=posting_id)
            
            Comment.objects.create(
                content = content,
                user    = user,
                posting = posting 
            )
            
            return JsonResponse({"message" : "SUCCESS"}, status=200)
            
        except KeyError:
            return JsonResponse({"key error" : "KEY_ERROR"}, status=400)