from django.conf.urls import include, url
import views
urlpatterns = [
    url(r'^$', views.recommend_news, name='recommend_news'),
    url(r'^get_like_ratio/$', views.get_like_ratio, name='get_like_ratio'),
    url(r'^like/$', views.users_mypage, name='users_mypage'),
    url(r'^like_news_in_liked_page/(?P<id>\d+)/$', views.like_news_in_liked_page, name='like_news_in_liked_page'),
    url(r'^dislike_news_in_liked_page/(?P<id>\d+)/$', views.dislike_news_in_liked_page, name='dislike_news_in_liked_page'),
    url(r'^like_in_recommend_page/(?P<id>\d+)/$', views.like_in_recommend_page, name='like_in_recommend_page'),
    url(r'^dislike_in_recommend_page/(?P<id>\d+)/$', views.dislike_in_recommend_page, name='dislike_in_recommend_page'),

]