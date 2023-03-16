from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    """username(str), email(str), password(str), joinedRooms(int,default=0), createdRooms(int,default=0)"""
    joinedRooms = models.IntegerField(default=0)
    createdRooms = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.username}"
    
class Room(models.Model):
    """name(str), description(str), admin(User), numberUsers(int,default=1)"""
    name = models.CharField(max_length=64,unique=True)
    description = models.CharField(max_length=256)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="get_admin")
    numberUsers = models.IntegerField(default=1)
    
    def __str__(self):
        return f"{self.name} created by {self.admin.username}"
    
class UserRooms(models.Model):
    """user(User), room(Room)"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="get_user")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="get_room")
    
    def __str__(self):
        return f"{self.user.username} joined {self.room.name}"
    
class Message(models.Model):
    """user(User), room(Room), message(Text), timestamp(datetime)"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="get_users_messages")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="get_rooms_messages")
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} said {self.message} in {self.room.name}"
    

class JoinRequests(models.Model):
    """user(User), room(Room), admin(User)"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="get_users_requests")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="get_rooms_requests")
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="get_admins_requests")

    def __str__(self):
        return f"{self.user.username} requested to join {self.room.name} by {self.admin.username}"
    
    # make sure that the user can only request to join a room once
    class Meta:
        unique_together = ['user', 'room', 'admin']

