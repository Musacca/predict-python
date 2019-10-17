from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^prediction/', views.post_prediction),
    url(r'^replay/', views.post_replay),
    url(r'^replay_prediction/', views.post_replay_prediction),
]
