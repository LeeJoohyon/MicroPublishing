from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from column.models import Post
from member.models import BuyList

__all__ = (
    'index',
)


def index(request):
    if request.COOKIES:
        if request.COOKIES['token']:
            response = render_to_response("view/main.html", {"login": True})
            return response
        return render_to_response('view/main.html',)
    return render_to_response('view/main.html',)


def write(request):
    return render_to_response('view/write.html')


def read(request, post_id):
    print(post_id)
    post = Post.objects.filter(pk=post_id)
    if BuyList.objects.filter(user=request.user, post=post).count() == 0:
        return HttpResponseRedirect('/')
    return render_to_response('view/read.html')