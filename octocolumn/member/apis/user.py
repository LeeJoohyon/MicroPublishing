from django.core.exceptions import ObjectDoesNotExist
import requests
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from ipware.ip import get_ip
from redis_cache import cache

from rest_framework import status, generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import APIException
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from typing import NamedTuple

from rest_framework_jwt.settings import api_settings

from config import settings
from member.backends import FacebookBackend
from member.models import User, ProfileImage, ConnectedLog, InviteUser
from member.serializers import UserSerializer, SignUpSerializer, ProfileImageSerializer
from member.serializers.user import ChangePasswordSerializer
from utils.customsendmail import invite_email_send, password_reset_email_send
from utils.jwt import jwt_token_generator

__all__ = (
    'Login',
    'SignUp',
    'Logout',
    'FacebookLogin',
    'PasswordReset',
    'SendInviteEmail',
    'PasswordResetSendEmail',
    'UserInfo'
)


# 1
# 로그인 API
# URL /api/member/login/
# 전달 키값 : username, password
class Login(APIView):
    permission_classes = (AllowAny,)

    def saved_login_log(self, user):
        log = ConnectedLog()
        log.user = user
        log.type = 'login'
        log.ip_address = get_ip(self.request)
        log.user_agent = self.request.META['HTTP_USER_AGENT']
        return log.save()

    def post(self, request, *args, **kwargs):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(
            username=username,
            password=password,
        )
        if user:

            data = {
                'token': jwt_token_generator(user),
                'user': UserSerializer(user).data,
            }

            if data['user']['is_active']:
                # response = Response(data, status=status.HTTP_200_OK)
                # response = render_to_response("view/main.html", {"login": True})
                response = HttpResponseRedirect(redirect_to='/')
                if api_settings.JWT_AUTH_COOKIE:
                    response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                        data['token'],
                                        max_age=21600,
                                        httponly=True)
                    self.saved_login_log(user)
                    return response
                # return response
                return response
            data = {
                "detail": "This Account is not Activate"
            }
            # return Response(data, status=status.HTTP_401_UNAUTHORIZED)
            return HttpResponseRedirect(redirect_to='/signin/')
        data = {
            'detail': 'Invalid credentials'
        }

        # return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        return HttpResponseRedirect(redirect_to='/signin/')


# 1
# 로그아웃 API
# URL /api/member/logout/
# 전달 키값 : username, password1, password2, nickname
class Logout(APIView):
    permission_classes = (IsAuthenticated,)

    def saved_logout_log(self, user):
        log = ConnectedLog()
        log.user = user
        log.type = 'logout'
        log.ip_address = get_ip(self.request)
        log.user_agent = self.request.META['HTTP_USER_AGENT']
        return log.save()

    def post(self, request):
        response = Response({"detail": "Successfully logged out."},
                        status= status.HTTP_200_OK)

        self.saved_logout_log(self.request.user)
        response.delete_cookie('token')
        return response


# 1
# 회원가입 API
# URL /api/member/signup/
# 전달 키값 : username, password1, password2, nickname
class SignUp(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = SignUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponseRedirect(redirect_to='/okay/')
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return HttpResponseRedirect(redirect_to='/signup/')


# 1
# 페이스북 로그인 API
# URL /api/member/facebookLogin/
# 전달 키값 : token
class FacebookLogin(APIView):
    permission_classes = (AllowAny,)
    # /api/member/facebook-login/

    def post(self, request):
        # request.data에
        #   access_token
        #   facebook_user_id
        #       데이터가 전달됨

        # Debug결과의 NamedTuple
        class DebugTokenInfo(NamedTuple):
            app_id: str
            application: str
            expires_at: int
            is_valid: bool
            scopes: list
            type: str
            user_id: str

        # token(access_token)을 받아 해당 토큰을 Debug
        def get_debug_token_info(token):
            app_id = settings.FACEBOOK_APP_ID
            app_secret_code = settings.FACEBOOK_APP_SECRET_CODE
            app_access_token = f'{app_id}|{app_secret_code}'

            url_debug_token = 'https://graph.facebook.com/debug_token'
            params_debug_token = {
                'input_token': token,
                'access_token': app_access_token,
            }
            response = requests.get(url_debug_token, params_debug_token)
            return DebugTokenInfo(**response.json()['data'])

        # request.data로 전달된 access_token값을 페이스북API쪽에 debug요청, 결과를 받아옴
        debug_token_info = get_debug_token_info(request.data['access_token'])

        if debug_token_info.user_id != request.data['facebook_user_id']:
            raise APIException('페이스북 토큰의 사용자와 전달받은 facebook_user_id가 일치하지 않음')

        if not debug_token_info.is_valid:
            raise APIException('페이스북 토큰이 유효하지 않음')

        userid = debug_token_info.user_id

        userinfo = User.objects.filter(username=request.data['email']).count()

        if not userinfo == 0:
            raise APIException('Already exists this email')

        # FacebookBackend를 사용해서 유저 인증
        user = FacebookBackend.authenticate(facebook_user_id=userid)
        # 인증에 실패한 경우 페이스북유저 타입으로 유저를 만들어줌
        if not user:
            user = User.objects.create_facebook_user(
                username=request.data['email'],
                first_name=request.data['first_name'],
                last_name=request.data['last_name'],
                social_id=f'fb_{request.data["facebook_user_id"]}',
                )

        else:
            pass

        # 유저 시리얼라이즈 결과를 Response
        # token도 추가
        data = {
            'user': UserSerializer(user).data,
            'token': jwt_token_generator(user),
        }

        response = Response(data, status=status.HTTP_200_OK)
        if api_settings.JWT_AUTH_COOKIE:
            response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                response.data['token'],
                                max_age=21600,
                                httponly=True)
        return response


# 1
# 이메일 전달체킹 완료시 비밀번호변경 API
# URL /api/member/passwordReset/
class PasswordReset(APIView):
    permission_classes = (AllowAny, )

    def social_check(self):
        if self.request.user.user_type is not 'd':
            raise APIException('소셜계정은 비밀번호를 변경할수 없습니다.')
        return self.request.user

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=self.request.data)

        if serializer.is_valid():
            # Check old password

            # set_password also hashes the password that the user will get
            self.request.user.set_password(serializer.data['password1'])
            self.request.user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 1
# 유저정보 관련 API
# URL /api/member/userInfo/
class UserInfo(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = UserSerializer(self.request.user)
        try:
            profile_image = ProfileImage.objects.filter(user=self.request.user).get()
            profile_serializer = ProfileImageSerializer(profile_image)

            if serializer:
                return Response({"user": serializer.data,
                                 "profileImg": profile_serializer.data},
                                status=status.HTTP_200_OK)
            return Response({"detail": "NO User"})

        except ObjectDoesNotExist:
            return Response({"user": serializer.data,
                             "profileImg": {
                                 "profile_image": '/example/2_x20_.jpeg',
                                 "cover_image": '/example/1.jpeg'
                             }}, status=status.HTTP_200_OK)


# 1
# 초대메일 API
# URL /api/member/invite/
# 데이터 전송 키 값 : email
class SendInviteEmail(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        data = self.request.data

        user = InviteUser.objects.create(email=data['email'])
        email = invite_email_send(user, self.request.user)
        if email:
            return Response({"detail": "Email Send Success"}, status=status.HTTP_200_OK)
        raise APIException({"Email send failed"})


# 1
# 패스워드 분실시 비밀번호 초기화 API
# URL /api/member/passwordResetEmail/
# 데이터 전송 키 값 : username
class PasswordResetSendEmail(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        data = self.request.data

        try:
            user = User.objects.filter(username=data['username']).get()

            email = password_reset_email_send(user)

            if email:
                return Response({"detail": "Email Send Success"}, status=status.HTTP_200_OK)
            raise APIException({"Email send failed"})
        except ObjectDoesNotExist:
            raise APIException({"this username is not valid"})
