from django.conf.urls import url, include

from config.urls import support
from config.views import index
from config.views.index import write, naver_request, preview, more, robot, sitemap
from config.views.index import bookmark, buylist, feed
from config.views.index import findPass, resetPass
from config.views.index import read
from config.views.index import profile
from config.views.index import shop
from member.apis import VerifyEmail, InviteVerifyEmail


urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^naverd45c8d580806584cb434be95a432581b.html', naver_request, name='naver'),


    url(r'^write/',
        include([
            url(r'^$', write, name="write"),
            url(r'^(?P<temp_id>\d+)$',
                write, name="temp_write")
    ]), name='write'),
    url(r'^@(?P<author>.+)/(?P<title>.+)$', read, name='read'),
    url(r'^preview/@(?P<author>.+)/(?P<title>.+)$', preview, name='preview'),
    url(r'^profile/', include([
            url(r'^$', profile, name="profile"),
            url(r'^(?P<member_id>.+)$',
                profile, name="profile")
    ]), name='profile'),
    url(r'^more/(?P<type>[-\w]+)/$', more, name='more'),
    # url(r'^recent/$', recent, name='recent'),
    url(r'^buylist/$', buylist, name='buylist'),
    url(r'^bookmark/$', bookmark, name='bookmark'),
    url(r'^feed/$', feed, name='feed'),
    # url(r'^signin/$', signin, name='signin'),
    # url(r'^signinForm/$', signinForm, name='signinForm'),
    # url(r'^okay/$', okay, name='okay'),
    url(r'^findPass/$', findPass, name='findPass'),
    url(r'^resetPass/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        resetPass, name='resetPass'),
    # url(r'^signup/$', signup, name='signup'),
    url(r'^shop/$', shop, name='shop'),

    # 이메일 체킹
    url(r'^verifyChecking/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        VerifyEmail.as_view(), name='verifyChecking'),

    url(r'^inviteChecking/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        InviteVerifyEmail.as_view(), name='InviteVerifyEmail'),

    url(r'^support/', include(support, namespace='support')),

    # url(r'^search/', include('search_indexs.urls')),

    url(r'^robots.txt', robot, name='robot'),
    url(r'^sitemap.xml', sitemap, name='sitemap'),

]
