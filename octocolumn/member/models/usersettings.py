from django.db import models
from django.db.models import F

__all__ = (
    'UserSecondPassword',
    'UserSetting'
)


class UserSecondPassword(models.Model):
    user = models.OneToOneField('member.User',null=True)
    second_password = models.IntegerField(default=None)
    error_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return '{} : {}'.format(
            self.user,
            self.second_password,
        )

    # 오입력시 카운트 증가 시키는 메서드
    def increase(self):
        self.error_count = F('error_count') + 1
        self.save()

    # 비밀번호 오입력시 카운트를 초기화 시키는 메서드
    def decrease(self):
        self.error_count = 0
        self.save()


class UserSetting(models.Model):
    user = models.ForeignKey('member.User',null=True)

    def __str__(self):
        return '{} : {}'.format(
            self.user,
        )

