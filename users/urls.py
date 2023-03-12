from django.urls import path
from . import views

urlpatterns = [
    path("", views.Users.as_view()),
    # *********** 순서 주의
    # path("<str:username>", views.PublicUser.as_view()), # 이 url 때문에 /me를 username으로 받아들여 오류 발생
    path("me", views.Me.as_view()),
    path("change-password", views.ChangePassword.as_view()),
    path("log-in", views.LogIn.as_view()),
    path("log-out", views.LogOut.as_view()),
    path("@<str:username>", views.PublicUser.as_view()), # me 아래로 내리면 제대로 작동, me라는 user가 있을 수 있기 때문에 @ 추가

    path("@<str:username>/rooms", views.ShowRooms.as_view()),
    path("@<str:username>/reviews", views.ShowReviews.as_view()),

]