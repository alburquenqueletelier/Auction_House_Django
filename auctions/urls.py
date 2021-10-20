from django.urls import path

from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_ac", views.new_auction, name="new_ac"),
    path("see_auction/<int:pk>", views.see_auction, name="see_auction"),
    path("see_auction/<int:pk>/addcomment", views.addcomment, name="addcomment"),
    path("see_auction/<int:pk>/addbid", views.addbid, name="addbid"),
    path("see_auction/<int:pk>/closebid", views.closebid, name="closebid"),
    path("closed", views.closed, name="closed")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
