from django.contrib import admin
from .models import User, Room, UserRooms, Message, JoinRequests

# Register your models here.

admin.site.register(User)
admin.site.register(Room)
admin.site.register(UserRooms)
admin.site.register(Message)
admin.site.register(JoinRequests)