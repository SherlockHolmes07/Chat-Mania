from django.contrib import admin
from .models import User, Room, UserRooms, Message

# Register your models here.

admin.site.register(User)
admin.site.register(Room)
admin.site.register(UserRooms)
admin.site.register(Message)
