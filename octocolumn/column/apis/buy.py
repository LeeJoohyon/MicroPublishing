from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, exceptions
from rest_framework.response import Response
from rest_framework.views import APIView

from column.models import Post
from member.models import User, PointHistory, BuyList, SellList
from utils.error_code import kr_error_code

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
            return Response(
                {
                    "code": 401,
                    "message": kr_error_code(401)
                }
            , status=status.HTTP_401_UNAUTHORIZED)

        post_queryset = Post.objects.select_related('author').filter(id=data['post_id']).get()

        # 포인트가 적을시에 오류 발생
        if post_queryset.price > user.point:
            return Response(
                {
                    "code": 414,
                    "message": kr_error_code(414)
                }
                , status=status.HTTP_414_REQUEST_URI_TOO_LONG)

        # 구매한 기록이 있는지를 확인
        if self.buylist_duplicate(post_queryset):
            # 구매내역에 추가
            PointHistory.objects.buy(user=user, point=post_queryset.price,
                                     history=post_queryset.title,
                                     post=post_queryset
                                     )

            buy_list = BuyList.objects.create(user=user, post=post_queryset)

            sell_list = SellList.objects.create(user=user, post=post_queryset)

            if buy_list and sell_list:
                post_queryset.buy_count += 1
                user = post_queryset.author
                user.point += post_queryset.price
                post_queryset.save()
                user.save()
            else:
                return Response(
                    {
                        "code": 414,
                        "message": kr_error_code(414)
                    }
                    , status=status.HTTP_414_REQUEST_URI_TOO_LONG)

            # 구매횟수 증가 업데이트

            return Response({"detail": "Success buy."}, status=status.HTTP_200_OK)

        return Response(
            {
                "code": 416,
                "message": kr_error_code(416)
            }
            , status=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE)


