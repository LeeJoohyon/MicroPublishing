from django.conf.urls import url, include
from django.contrib import admin

from config.views import index
from config.views.index import write
from member.apis.verify import VerifyEmail, PasswordResetEmail

urlpatterns = [
    url(r'^$', index, name='index'),url(r'^write/$', write, name='write'),

    # url(r'^post/', include('column.urls.views', namespace='post')),
    url(r'^member/', include('member.urls.views', namespace='member')),
    #

]