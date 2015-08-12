from django.conf.urls import url, include  
from rest_framework.routers import DefaultRouter
from news import news_urls, views  
import settings

router = DefaultRouter()
router.register(r'news', views.NewsViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    url(r'^rest-api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^$', views.index, name='index'),
    url(r'^news/', include(news_urls, namespace='news')),
]


if settings.DEBUG:  
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]