from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from .manager import UserManager
from django.contrib.auth.models import PermissionsMixin


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    firstName = models.CharField(max_length=15, null=True)
    lastName = models.CharField(max_length=15, null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    user_type_choice = (
        ('customer', 'customer'),
        ('staff', 'staff')
    )
    user_type = models.CharField(choices=user_type_choice, default='customer', max_length=8)

    # TODO: Added later
    session_token = models.CharField(max_length=10, default='0')

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class RoomCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False, null=False)
    description = models.TextField(max_length=500, blank=False, null=False)
    cost_of_room_type = models.IntegerField(blank=False, null=False)
    image = models.ImageField(upload_to='pictures', default=None, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def room_price(self):
        return str(self.cost_of_room_type)


class Room(models.Model):
    room_type = models.ForeignKey(RoomCategory, on_delete=models.CASCADE, related_name="rooms")

    availability = models.BooleanField(default=True, null=False, blank=False)
    description = models.TextField(max_length=300, null=True, blank=True)
    image = models.ImageField(upload_to='pictures')
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['id']


class Booking(models.Model):
    # booking_id = models.AutoField(primary_key=True, verbose_name='booking_id')
    guest = models.ForeignKey(User, on_delete=models.CASCADE, related_name="booking_details")
    room_no = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room_number_details')
    no_of_adults = models.IntegerField(default=1)
    no_of_children = models.IntegerField(default=0)
    check_in = models.DateField('check in')
    check_out = models.DateField('check out')

    id_proof_choices = (
        ('Aadhar', 'Aadhar'),
        ('PAN', 'PAN'),
        ('License', 'License')
    )
    id_proof = models.CharField(choices=id_proof_choices, max_length=10, default='Aadhar')
    id_proof_number = models.CharField(max_length=12, blank=True, null=True)
    phone_no = models.BigIntegerField(blank=True, null=True)
    is_cancelled = models.BooleanField(default=False)

    payment_detail = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Booking ID: " + str(self.id)

    @property
    def check_room_no(self):
        return self.room_no

    @property
    def total_no_of_booking_days(self):
        # print(self.check_in)
        check_in_date = (str(self.check_in))[-2:]
        check_out_date = (str(self.check_out))[-2:]
        total_days = abs(int(check_out_date) - int(check_in_date))
        # print("Total number of days:", total_days)
        if total_days == 0:
            return 1
        return total_days


class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="booking_details")
    status = models.BooleanField(default=False)
    amount = models.FloatField(default=0)

    def __str__(self):
        return "Payment ID: " + str(self.id)

    class Meta:
        ordering = ['status']