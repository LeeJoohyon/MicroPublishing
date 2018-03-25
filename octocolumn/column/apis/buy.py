from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, exceptions
from rest_framework.response import Response
from rest_framework.views import APIView

from column.models import Post
from member.models import User, PointHistory,BuyList


__all__ = (
    'PostBuy',
)


class PostBuy(APIView):

    # 구매리스트에 존재하는지 판명
    def buylist_duplicate(self, post):
        try:
            BuyList.objects.filter(user=self.request.user, post=post).get()
            raise False
        except ObjectDoesNotExist:
            return True

    def post(self,request):
        data = self.request.data
        user = self.request.user
        if not self.request.user.is_authenticated:
            raise exceptions.NotAuthenticated()

        post_queryset = Post.objects.filter(id=data['post_id']).get()

        # 포인트가 적을시에 오류 발생
        if post_queryset.price > user.point:
            raise exceptions.APIException({"detail": "There is not enough points."}, code=400)

        # 구매한 기록이 있는지를 확인
        if self.buylist_duplicate(post_queryset):
            # 구매내역에 추가
            PointHistory.objects.buy(user=self.request.user, point=post_queryset.price,
                                     history=post_queryset.title,
                                     post=post_queryset
                                     )

            buylist = BuyList.objects.create(user=self.request.user, post=post_queryset)

            if buylist:
                post_queryset.buy_count += 1
                post_queryset.save()
            else:
                raise exceptions.APIException({"detail": "There is not enough points."}, code=400)

            # 구매횟수 증가 업데이트

            return Response({"detail": "Success buy."}, status=status.HTTP_200_OK)

        raise exceptions.APIException({"detail": "Failed buy."}, 400)


