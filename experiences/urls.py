from django.urls import path
from experiences import views

urlpatterns = [
    path("perks/", views.Perks.as_view()),
    path("perks/<int:pk>", views.PerkDetail.as_view()),

    path("", views.Experiences.as_view()),
    path("<int:pk>", views.ExperiencesDetail.as_view()),
    path("<int:pk>/reviews", views.ExperienceReviews.as_view()),
    path("<int:pk>/perks", views.ExperiencePerks.as_view()),
]