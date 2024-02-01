from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = "main"


urlpatterns = [
    # path("", views.homepage, name="homepage"),
    path("", views.login_request, name="login"),
    path("register", views.register_request, name="register"),
    path("firstuser/<str:user_id>", views.firstuser_request, name="firstuser"),
    path("<str:user_id>", views.homepage, name="homepage"),
    path("like_image/", views.like_image, name="like_image"),
    path("run_recommendations/", views.run_recommendations, name= "run_recommendations"),
    path("init_feed/<str:user_id>", views.init_feed, name="init_feed")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
