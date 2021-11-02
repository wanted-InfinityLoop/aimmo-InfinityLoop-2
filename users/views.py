import json
import re
import bcrypt
import jwt

from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.http import JsonResponse

from users.models import User
from my_settings import MY_SECRET_KEY
from .serializer import UserSignInSerializer, UserSignUpSerializer


class SignupView(APIView):
    @swagger_auto_schema(operation_description="회원가입", request_body = UserSignUpSerializer)
    def post(self, request):
        try:
            data = json.loads(request.body)

            if User.objects.filter(email=data["email"]).exists():
                return JsonResponse(
                    {"message": f"{data['email']}_ALREADY_EXIST"}, status=409
                )

            REGEX_EMAIL = re.compile("^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

            REGEX_PASSWORD = re.compile(
                "^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$"
            )

            is_email_valid = REGEX_EMAIL.match(data["email"])
            is_password_valid = REGEX_PASSWORD.match(data["password"])

            if not (is_email_valid and is_password_valid):
                return JsonResponse({"message": "INVALID_INPUT_FORMAT"}, status=400)

            user = User.objects.create(
                name=data["name"],
                email=data["email"],
                password=bcrypt.hashpw(
                    data["password"].encode("utf-8"), bcrypt.gensalt()
                ).decode("utf-8"),
            )

            return JsonResponse(
                {"message": "SUCCESS", "username": user.name}, status=201
            )
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)


class SigninView(APIView):
    @swagger_auto_schema(operation_description="로그인", request_body = UserSignInSerializer)
    def post(self, request):
        try:
            data = json.loads(request.body)

            if not User.objects.filter(email=data["email"]).exists():
                return JsonResponse({"message": "INVALID_USER"}, status=401)

            user = User.objects.get(email=data["email"])

            if not bcrypt.checkpw(
                data["password"].encode("utf-8"), user.password.encode("utf-8")
            ):
                return JsonResponse({"message": "INVALID_USER"}, status=401)

            token = jwt.encode({"id": user.id}, MY_SECRET_KEY, algorithm="HS256")
            return JsonResponse(
                {"message": "SUCCESS", "token": token, "username": user.name},
                status=200,
            )

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
