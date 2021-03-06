from rest_framework import serializers, status
from rest_framework.fields import SerializerMethodField
from rest_framework.response import Response

from member.models import User
from member.task import SignupEmailTask
from utils.crypto import encode

__all__ = (
    'UserSerializer',
    'SignUpSerializer',
    'ChangePasswordSerializer'
)


class UserSerializer(serializers.ModelSerializer):

    def get_pk(self, obj):

        return encode(clear=str(obj.pk))

    def get_notify(self, obj):
        from member.serializers import NotificationSerializer
        serializers = NotificationSerializer(obj.notify, many=True)
        return serializers.data

    pk = SerializerMethodField()
    notify = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'pk',
            'last_name',
            'first_name',
            'username',
            'nickname',
            'point',
            'notify',
            'is_active',
        )


class SignUpSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    nickname = serializers.CharField(write_only=True)
    username = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'password1',
            'password2',
            'nickname',
        )

    def validate(self, data):
        if data['password1'] != data['password2']:
            return serializers.ValidationError('비밀번호가 일치하지 않습니다.')

        if len(data['password1']) < 8:
            return serializers.ValidationError('비밀번호는 최소 8자리 입니다.')

        return data

    def create(self, validated_data):
        user = User.objects.create_user(
           username=validated_data['username'],
           password=validated_data['password1'],
           nickname=validated_data['nickname'],
        )
        if user:
            task = SignupEmailTask
            if task.delay(user.pk):
                return user
            else:
                return Response(
                    {
                        "code": 409,
                        "message": {
                            "title": "Email sended fail",
                            "content": "이메일 발송에 실패했습니다."
                        }

                    }
                    , status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(
                {
                    "code": 409,
                    "message": {
                        "title": "Email sended fail",
                        "content": "이메일 발송에 실패했습니다."
                    }

                }
                , status=status.HTTP_400_BAD_REQUEST)
        # if user:
        #     mail_subject = 'byCAL 이메일 인증.'
        #     user = user
        #     message = render_to_string('welcome.html', {
        #         'user': user.nickname,
        #         'domain': 'bycal.co',
        #         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        #         'token': account_activation_token.make_token(user),
        #     })
        #     to_email = user.username
        #     email = EmailMultiAlternatives(
        #         mail_subject, to=[to_email]
        #     )
        #     email.attach_alternative(message, "text/html")
        #     email.send()
        #     return True
        # return False

    def to_representation(self, instance):
        # serializer된 형태를 결정
        # super().to_representation()은 serialize된 기본 형태(dict)
        ret = super().to_representation(instance)
        data = {
            'user': ret,
        }
        # 마지막엔 serializer.data를 출력했을 때 반환될 값을 반환해줘야 함
        return data


class ChangePasswordSerializer(serializers.Serializer):

    password1 = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('비밀번호가 일치하지 않습니다')
        return data


