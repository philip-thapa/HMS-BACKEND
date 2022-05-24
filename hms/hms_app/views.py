from rest_framework.views import APIView
from .models import User, RoomCategory, Room, Booking, Payment
from .serializers import UserSerializer, RoomCategorySerializer, RoomSerializer, BookingSerializer, PaymentSerializer, \
    RegistrationSerializer, GetBookingSerializer, UpdateBookingSerializer, SearchUserSearilizer, UpdateUserSerializer, \
    SearchBookingSearilizer, RoomCateRoomSerializer
from rest_framework.response import Response
from rest_framework import status

from rest_framework.parsers import FileUploadParser

from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout, authenticate
import random
import re
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.decorators import permission_classes

from .permissions import IsAdminOrLoggedInUser, LoggedInUserOrAdminOnly


def generate_session_token(length=10):
    return ''.join(random.SystemRandom().choice([chr(i) for i in range(97, 123)] + [str(i) for i in range(10)]) for _ in
                   range(length))


@csrf_exempt
@permission_classes((AllowAny,))
def signin(request):
    if not request.method == 'POST':
        return JsonResponse({'error': 'Send a post request with valid paramenter only'})

    email = request.POST.get('email', "")
    password = request.POST.get('password', "")

    if not re.match("^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email):
        return JsonResponse({'error': 'Enter a valid email'})

    if len(password) < 3:
        return JsonResponse({'error': 'Password needs to be at least of 3 char'})

    UserModel = get_user_model()

    try:
        user = UserModel.objects.get(email=email)

        if user.check_password(password):
            usr_dict = UserModel.objects.filter(
                email=email).values().first()
            usr_dict.pop('password')
            token = generate_session_token()
            user.session_token = token
            user.save()
            token, _ = Token.objects.get_or_create(user=user)
            login(request, user)
            return JsonResponse({'token': token.key, 'user': usr_dict, 'status': 200})
        else:
            return JsonResponse({'error': 'Invalid password', 'status': 404})

    except UserModel.DoesNotExist:
        return JsonResponse({'error': 'Invalid Email'})


def signout(request, id):
    logout(request)

    UserModel = get_user_model()

    try:
        user = UserModel.objects.get(pk=id)
        user.session_token = '0'
        user.save()
        return JsonResponse({'success': 'UserLoggedOut successfully'})
    except UserModel.DoesNotExist:
        return JsonResponse({'error': 'Invalid User ID'})


class CustomUserCreateAV(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        reg_serializer = RegistrationSerializer(data=request.data)
        if reg_serializer.is_valid():
            newUser = reg_serializer.save()
            if newUser:
                return Response(status=status.HTTP_201_CREATED)
        return Response(reg_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListAV(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse({'users': serializer.data, 'status': 200})


class UserDetailAV(APIView):
    permission_classes = [IsAdminOrLoggedInUser]

    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user)
            return JsonResponse({'user': serializer.data, 'status': 200})
        except User.DoesNotExist:
            return JsonResponse({'error': 'User doesnot exist', 'status': 400})

    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            serializer = UpdateUserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'User doesnot exist'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            return Response({'success': 'Deleted'})
        except User.DoesNotExist:
            return Response({'error': 'User doesnot exist'}, status=status.HTTP_404_NOT_FOUND)


class RoomCategoryListAV(APIView):
    def get(self, request):
        try:
            categories = RoomCategory.objects.all()
            serializer = RoomCategorySerializer(categories, many=True)
            return JsonResponse({'roomCate': serializer.data})
        except RoomCategory.DoesNotExist:
            return Response({"error": "Room Category doesnot exist"})


class CreateRoomCategoryAV(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = RoomCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"roomCate": serializer.data, 'status': 200})
        return JsonResponse({'error': serializer.errors, 'status': 400})


class RoomCatergoryDetailAV(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        try:
            roomCategory = RoomCategory.objects.get(pk=pk)
            serializer = RoomCategorySerializer(roomCategory)
            return Response(serializer.data)
        except RoomCategory.DoesNotExist:
            return Response({'error': 'Room category doesnot exist'})

    def put(self, request, pk):
        try:
            roomCategory = RoomCategory.objects.get(pk=pk)
            serializer = RoomCategorySerializer(roomCategory, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except RoomCategory.DoesNotExist:
            return Response({'error': 'Room category doesnot exist'})

    def delete(self, request, pk):
        try:
            roomCategory = RoomCategory.objects.get(pk=pk)
            roomCategory.delete()
            return Response({'success': 'Room Category Deleted'})
        except RoomCategory.DoesNotExist:
            return Response({'error': 'Room category doesnot exist'})


class RoomListAV(APIView):
    parser_class = (FileUploadParser,)

    def get(self, request):
        try:
            rooms = Room.objects.all()
            serializer = RoomSerializer(rooms, many=True)
            return JsonResponse({'rooms': serializer.data, 'status': 200})
        except Room.DoesNotExist:
            return JsonResponse({'error': 'Room doesnot exist', 'status': 400})


class CreateRoomAV(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        try:
            serializer = RoomSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'room': serializer.data, 'status': 200})
            return JsonResponse({'error': serializer.errors})
        except:
            return JsonResponse({'error': 'Something went wrong'})


class RoomDetailAV(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        try:
            room = Room.objects.get(pk=pk)
            serializer = RoomSerializer(room)
            return Response(serializer.data)
        except Room.DoesNotExist:
            return Response({'error': 'Room doesnot exist'})

    def put(self, request, pk):
        try:
            room = Room.objects.get(pk=pk)
            serializer = RoomSerializer(room, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except Room.DoesNotExist:
            return Response({'error': 'Room doesnot exist'})

    def delete(self, request, pk):
        try:
            room = Room.objects.get(pk=pk)
            room.delete()
            return Response({'success': 'Room Deleted'})
        except Room.DoesNotExist:
            return Response({'error': 'Room doesnot exist'})


class BookingListAV(APIView):
    # permission_classes = [IsAdminUser]

    def get(self, request):
        try:
            bookings = Booking.objects.all().order_by('is_cancelled')
            serializer = GetBookingSerializer(bookings, many=True)
            return JsonResponse({'bookings': serializer.data, 'status': 200})
        except Booking.DoesNotExist:
            return JsonResponse({'error': 'Bookings doesnot exist'})


class GetAvailableRoom(APIView):
    def get(self, request, roomCateId):
        try:
            roomCate = RoomCategory.objects.get(pk=roomCateId)
            room = Room.objects.filter(availability=True, room_type=roomCate).first()
            if room != None:
                return JsonResponse({"roomId": room.id})
            return JsonResponse({"error": "Room Not available currently"})
        except RoomCategory.DoesNotExist:
            return JsonResponse({'error': "Room Cate doesnot exist"})


class CreateBookingAV(APIView):

    def post(self, request):
        serializer = BookingSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'booking': serializer.data, 'status': 200})
        return JsonResponse({'error': serializer.errors})


class CancelBooking(APIView):
    permission_classes = [LoggedInUserOrAdminOnly]

    def get(self, request, bookingId):
        try:
            booking = Booking.objects.get(pk=bookingId)
            if booking.guest == request.user or request.user.is_staff == True:
                booking.is_cancelled = True
                room = booking.room_no.id
                room = Room.objects.get(pk=room)
                room.availability = True
                room.save()
                booking.save()
                return JsonResponse({"msg": "OOPS cancelled"})
        except Booking.DoesNotExist:
            return JsonResponse({'error': 'Invalid booking ID'})


class UserBookingListAV(APIView):
    # permission_classes = [IsAdminOrLoggedInUser]

    def get(self, request, userid):
        print("USERID", userid)
        try:
            user = request.user
            print(request.user)
            # if user.id == userid: ---> Page need to be refreshed to get the data if i keep it
            bookings = Booking.objects.filter(guest=user).order_by('is_cancelled')
            serializer = GetBookingSerializer(bookings, many=True)
            return JsonResponse({'bookings': serializer.data})
            # return JsonResponse({'error': 'Not Authorized ***'})
        except Booking.DoesNotExist:
            return Response({'error': 'No booking history  found'})


class BookingDetailAV(APIView):

    def get(self, request, bookingId):
        try:
            user = request.user
            booking = Booking.objects.get(pk=bookingId, guest=user)
            serializer = GetBookingSerializer(booking)
            return Response(serializer.data)
        except Booking.DoesNotExist:
            return Response({'error': 'Booking doesnot exist'})

    def put(self, request, bookingId):
        try:
            booking = Booking.objects.get(pk=bookingId)
            serializer = UpdateBookingSerializer(booking, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except Booking.DoesNotExist:
            return Response({'error': 'Booking doesnot exist'})

    def delete(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk)
            booking.delete()
            return Response({'success': 'Room Deleted'})
        except Booking.DoesNotExist:
            return Response({'error': 'Room doesnot exist'})


class PaymentListAV(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        try:
            payments = Payment.objects.all()
            serializer = PaymentSerializer(payments, many=True)
            return Response(serializer.data)
        except Payment.DoesNotExist:
            return Response({'error': 'Payment doesnot exist'})


class CreatePaymentAv(APIView):

    def post(self, request):
        serializer = PaymentSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class PaymentDetailAV(APIView):
    def get(self, request, pk):
        try:
            payment = Payment.objects.get(pk=pk)
            serializer = PaymentSerializer(payment)
            return Response(serializer.data)
        except Payment.DoesNotExist:
            return Response({'error': 'Payment doesnot exist'})

    def put(self, request, pk):
        try:
            payment = Payment.objects.get(pk=pk)
            serializer = PaymentSerializer(payment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except Payment.DoesNotExist:
            return Response({'error': 'Payment doesnot exist'})
        except:
            return Response({'error': 'Something went wrong'}, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            payment = Payment.objects.get(pk=pk)
            payment.delete()
            return Response({'success': 'Payment Deleted'})
        except Payment.DoesNotExist:
            return Response({'error': 'Payment doesnot exist'})


class PerformPayment(APIView):
    def get(self, request, bookingid):
        try:
            booking = Booking.objects.get(pk=bookingid)
            room = booking.room_no
            room_cate = RoomCategory.objects.get(name__startswith=room.room_type)
            total_amount = room_cate.cost_of_room_type * booking.total_no_of_booking_days
            return JsonResponse({'payment_details': {'amount': total_amount, 'room_rate': room_cate.cost_of_room_type,
                                                     'total_days': booking.total_no_of_booking_days}})
        except:
            return JsonResponse({'error': 'Something went wrong'})


class Payment(APIView):

    def post(self, request, bookingid):
        payment = PaymentSerializer(data=request.data)
        if payment.is_valid():
            booking = Booking.objects.get(pk=bookingid)
            booking.payment_detail = True
            booking.save()
            return JsonResponse({'msg': 'Payment Success'})
        return JsonResponse({'error': 'Payment failed'})


class SearchUserView(APIView):
    def get(self, request):
        query = request.GET.get('searchInput')
        if query is None or query == '':
            users = User.objects.all()
            searchSerializer = SearchUserSearilizer(users, many=True)
            return JsonResponse({'users': searchSerializer.data})

        users = User.objects.filter(firstName__icontains=query)
        if users is not None:
            searchSerializer = SearchUserSearilizer(users, many=True)
            return JsonResponse({'users': searchSerializer.data})
        return JsonResponse({'error': 'No user found'})


class SearchBooking(APIView):
    def get(self, request):
        query = request.GET.get('searchInput')
        if query is None or query == '':
            bookings = Booking.objects.all()
            searchSerializer = SearchBookingSearilizer(bookings, many=True)
            return JsonResponse({'bookings': searchSerializer.data})
        bookings = Booking.objects.filter(guest__email__icontains=query)
        if bookings is not None:
            searchSerializer = SearchBookingSearilizer(bookings, many=True)
            return JsonResponse({'bookings': searchSerializer.data})
        return JsonResponse({'error': 'No booking found'})


class GetRoomCateAvailabeRoom(APIView):
    def get(self, request, roomCateId):
        roomCate = RoomCategory.objects.get(pk=roomCateId)
        rooms = Room.objects.filter(room_type=roomCate)
        roomSerializer = RoomCateRoomSerializer(rooms, many=True)
        return JsonResponse({'rooms': roomSerializer.data, 'roomCateName': roomCate.name})
