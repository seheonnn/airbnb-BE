from django.urls import path
from rooms import views

urlpatterns = [
    # path("", views.see_all_rooms), # 이미 rooms/로 들어온 것이기 때문에 "" 비어있음
    # # <넘길 파라미터 타임 : 넘길 파라미터 이름>
    # path("<int:room_pk>", views.see_one_room),

    path("", views.Rooms.as_view()),
    path("<int:pk>", views.RoomDetail.as_view()),
    path("<int:pk>/reviews", views.RoomReviews.as_view()),
    path("<int:pk>/amenities", views.RoomAmenities.as_view()),
    path("<int:pk>/photos", views.RoomPhotos.as_view()),
    path("<int:pk>/bookings", views.RoomBookings.as_view()),

    path("<int:pk>/bookings/<int:booking_pk>", views.RoomBookingDelete.as_view()),

    path("amenities/", views.Amenities.as_view()),
    path("amenities/<int:pk>", views.AmenityDetail.as_view()),
]