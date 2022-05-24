from rest_framework import serializers
from .models import User, Room, RoomCategory, Booking, Payment


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class UserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'firstName', 'lastName']


class GetBookingSerializer(serializers.ModelSerializer):
    guest = UserDetailsSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = "__all__"


class UpdateBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'id_proof', 'id_proof_number', 'phone_no']

    def update(self, instance, validated_data):
        instance.id_proof = validated_data.get('id_proof', instance.id_proof)
        instance.id_proof_number = validated_data.get('id_proof_number', instance.id_proof_number)
        instance.phone_no = validated_data.get('phone_no', instance.phone_no)
        instance.save()
        return instance


class BookingSerializer(serializers.ModelSerializer):
    guest = UserDetailsSerializer(read_only=True)
    roomCategory = serializers.CharField(write_only=True)

    class Meta:
        model = Booking
        exclude = ['room_no']

    def create(self, validated_data):
        roomCategory = validated_data.pop('roomCategory')
        roomc = RoomCategory.objects.get(name=roomCategory)
        try:
            room = Room.objects.filter(availability=True, room_type=roomc).first()
        except Room.DoesNotExist:
            return serializers.ValidationError()

        room.availability = False
        room.save()
        user = self.context['request'].user
        instance = self.Meta.model(guest=user, room_no=room, **validated_data)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    booking_details = BookingSerializer(many=True, read_only=True)

    class Meta:
        model = User
        exclude = ['is_superuser', 'password', 'is_active', 'last_login', 'groups', 'user_permissions']


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "firstName", "lastName"]

    def update(self, instance, validated_data):
        instance.firstName = validated_data.get('firstName', instance.firstName)
        instance.lastName = validated_data.get('lastName', instance.lastName)
        instance.save()
        return instance


class RoomCateRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["id", "availability"]


class RoomSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, allow_empty_file=False, allow_null=True, required=False)

    room_cost = serializers.FloatField(source='room_type.cost_of_room_type', read_only=True)
    room_type_name = serializers.CharField(source='room_type.name', read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'availability', 'description', 'image', 'room_type', 'room_cost', 'room_type_name']

    def create(self, validated_data):
        room_type = validated_data.pop('room_type')
        room_type_obj = RoomCategory.objects.get(name=room_type)
        instance = self.Meta.model(room_type=room_type_obj, **validated_data)
        instance.save()
        return instance


class RoomCategorySerializer(serializers.ModelSerializer):
    rooms = RoomSerializer(many=True, read_only=True)
    image = serializers.ImageField(max_length=None, allow_empty_file=False, allow_null=True, required=False)

    class Meta:
        model = RoomCategory
        exclude = ['created_at', 'updated_at']


class PaymentSerializer(serializers.ModelSerializer):
    booking_details = BookingSerializer(read_only=True)

    class Meta:
        model = Payment
        exclude = ["booking"]

    def create(self, validated_data):
        # print("INSIDE CREATE")
        bookingId = validated_data.pop('booking')
        booking = Booking.objects.get(pk=bookingId)
        booking.payment_detail = True
        booking.save()
        instance = self.Meta.model(booking=booking, **validated_data)
        instance.save()
        return instance


class SearchUserSearilizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class SearchBookingSearilizer(serializers.ModelSerializer):
    guest = UserDetailsSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = "__all__"