from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from utils.tokengenerator import account_activation_token


# 회원가입 인증 메일
def signup_email_send(user):
    # 이메일 발송
    mail_subject = 'Octocolumn 이메일 인증.'
    message = render_to_string('singup_activation.html', {
        'user': user,
        'domain': 'loaclhost:8000',
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    to_email = user.username
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    if not email.send():
        return False
    return True


def password_reset_email_send(user):
    # 이메일 발송
    mail_subject = 'Octocolumn 비밀번호 변경.'
    message = render_to_string('pw_change.html', {
        'user': user,
        'domain': 'loaclhost:8000',
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    to_email = user.username
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    if not email.send():
        return False
    return True

