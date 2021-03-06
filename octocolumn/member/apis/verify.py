from django.http import HttpResponseRedirect
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from member.models import User, Profile, ProfileImage, InviteUser
from member.serializers import UserSerializer
from utils.tokengenerator import account_activation_token

__all__ = (
    'VerifyEmail',
    'InviteVerifyEmail',

)


class VerifyEmail(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, uidb64, token):

        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            Profile.objects.create(user=user)
            ProfileImage.objects.create(user=user)
            user.is_active = True
            user.save()
            return HttpResponseRedirect(redirect_to='/')
        else:
            return Response('Activation link is invalid!', status=404)


class InviteVerifyEmail(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, uidb64, token):

        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = InviteUser.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            return HttpResponseRedirect(redirect_to='/signup/')
        else:
            return Response('Activation link is invalid!', status=404)


