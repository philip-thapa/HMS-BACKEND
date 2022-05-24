from django.urls import path, include
from .views import UserListAV, UserDetailAV, RoomCategoryListAV, RoomCatergoryDetailAV, RoomListAV, RoomDetailAV, \
    CreateRoomCategoryAV, BookingListAV, BookingDetailAV, CustomUserCreateAV, \
    UserBookingListAV, signout, signin, CreateRoomAV, CreateBookingAV, CancelBooking, GetAvailableRoom,PerformPayment, Payment,SearchUserView, SearchBooking, GetRoomCateAvailabeRoom

urlpatterns = [
    # USERS
    path('users/', UserListAV.as_view(), name="user_name"),
    path('user/<int:pk>/', UserDetailAV.as_view(), name="user_detail_name"),
    path("users/search/", SearchUserView.as_view(), name="search_user"),

    # AUTHENTICATION
    path('register/', CustomUserCreateAV.as_view(), name="register_user_name"),
    path('login/', signin, name='signin'),
    path('logout/<int:id>/', signout, name='signup'),

    # ROOM CATE
    path('roomcate/', RoomCategoryListAV.as_view(), name="room_category_list_name"),
    path('roomcate/create/', CreateRoomCategoryAV.as_view(), name="create_room_cate_name"),
    path('roomcate/<int:pk>/', RoomCatergoryDetailAV.as_view(), name="room_category_detail_name"),
    path('roomcate/<int:roomCateId>/rooms/', GetRoomCateAvailabeRoom.as_view(), name="room_inside_cate"),

    # ROOM
    path("rooms/", RoomListAV.as_view(), name="room_list_name"),
    path("rooms/create/", CreateRoomAV.as_view(), name="create_room_name"),
    path("room/<int:pk>/", RoomDetailAV.as_view(), name="room_detail_name"),

    # Bookings
    path("bookings/", BookingListAV.as_view(), name="booking_list_name"),
    path("bookings/roomCate/<int:roomCateId>/", GetAvailableRoom.as_view(), name="get_available roomId"),
    path("booking/create/", CreateBookingAV.as_view(), name="create_booking_name"),
    path("booking/mybooking/<int:bookingId>/", BookingDetailAV.as_view(), name="booking_detail_name"),
    path("bookings/mybooking/<int:userid>/", UserBookingListAV.as_view(), name="my_booking_name"),
    path("booking/cancel/<int:bookingId>/", CancelBooking.as_view(), name="cancel_booking"),
    path("bookings/search/", SearchBooking.as_view(), name="search_user"),

    # Payments
    path("payment/create/<int:bookingid>/", PerformPayment.as_view(), name="perform_payment"),
    path("payment/perform/<int:bookingid>/", Payment.as_view(), name="pay"),

]
