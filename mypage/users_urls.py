from django.conf.urls import include, url
import views
urlpatterns = [
    url(r'^$', views.users_mypage, name='users_mypage'),
    url(r'^recommended/$', views.recommended_news, name='recommended_news'),
    url(r'^get_liked_ratio_data/', views.get_liked_ratio_data, name="get_liked_ratio_data"),


]