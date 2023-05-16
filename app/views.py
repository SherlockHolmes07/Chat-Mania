import json
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import User, Room, UserRooms, Message, JoinRequests
import pusher
# Create your views here.


# Create Room Form
class CreateRoomForm(forms.Form):
    name = forms.CharField(label="Room Name", max_length=64, required=True, min_length=3,
    widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Room Name'}))

    description = forms.CharField(label="Description", max_length=256,min_length=5, required=True, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description', 'rows': '5'}))

# Index
@login_required(login_url="login")
def index(request):
    # get the list of rooms
    rooms = Room.objects.all()
    print(rooms)
    # Get the list of rooms that users has requested to join
    join_requests = JoinRequests.objects.filter(user=request.user)
    x = [room.room for room in join_requests]
    print(x)
    # Get the list of rooms that the user has joined
    user_rooms = UserRooms.objects.filter(user=request.user)
    y = [room.room for room in user_rooms]
    print(y)
    return render(request, 'app/index.html', {
        'rooms': rooms,
        'join_requests': join_requests,
        'x': x,
        'y': y,
    })

# Register a new user
def register_view(request):
    if request.method == 'POST':
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "app/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            print("User created")
        except IntegrityError:
            return render(
                request,
                "app/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        # Load registration form
        return render(request, 'app/register.html')

def login_view(request):
    if request.method == 'POST':
        # Attempt to sign user in
        print("Login attempt")
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password) 
        print(user)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            print("User is logged in")
            return HttpResponseRedirect(reverse("index"))
        else:
            print("User is not logged in")
            return render(
                request,
                "app/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        # Load login form
        return render(request, "app/login.html")
    
# Logout
def logout_view(request):
    logout(request)
    return render(request, "app/login.html", {"message": "Logged out."})


# Create Rooms
@login_required(login_url="login")
def create(request):
    # Check of the request is POST
    if request.method == "POST":
        # Get the form data
        form = CreateRoomForm(request.POST)
        # Check if the form is valid
        if form.is_valid():
            #Get from Data
            name = form.cleaned_data["name"]
            description = form.cleaned_data["description"]
            # Strip the name of whitespaces and replace spaces with underscores
            name = name.strip().replace(" ","_")
            # Create a new room
            room = Room(name=name, description=description, admin=request.user)
            room.save()
            # Add the User-Rooms Mapping
            user_room = UserRooms(user=request.user, room=room)
            user_room.save()
            # Redirect to the index page
            return HttpResponseRedirect(reverse("index"))
        else:
            # If the form is invalid
            return render(request, 'app/createroom.html', { # Render the same page with the form data
                'CreateRoomForm': CreateRoomForm(),
                'message': 'Invalid form data'
            })
    else:
        # If the request is GET
        return render(request, 'app/createroom.html', {
            # Render the same page with the form data
            'CreateRoomForm': CreateRoomForm()
        })
    

# Your Rooms
@login_required(login_url="login")
def your_rooms(request):
   # Get the rooms that the user is admin of
    rooms = Room.objects.filter(admin=request.user)
    return render(request, 'app/yourrooms.html', {
        'rooms': rooms
    })


# Join Room
@login_required(login_url="login")
def join_room(request):
    if request.method == "POST":
        data = json.loads(request.body)
        room_id = data['room']
        room = Room.objects.get(id=room_id)
        join =  JoinRequests.objects.create(user=request.user, room=room, admin=room.admin) 
        join.save()
        return HttpResponse("Added request to Join Requests", status=200)


# Join Requests
@login_required(login_url="login")
def join_requests(request):
    # Get the join requests
    requests = JoinRequests.objects.filter(admin=request.user)
    print(requests)
    return render(request, 'app/joinrequests.html', {
        'requests': requests
    })


# Accept Request
@login_required(login_url="login")
def accept_request(request):
    if request.method == "POST":
        # Get the request id
        data = json.loads(request.body)
        request_id = data["requestId"]  
        # Get the joinRequest Mapping   
        Request = JoinRequests.objects.get(id=request_id)
        # Check if the user is the admin of the room
        if Request.admin.id != request.user.id:
            return HttpResponse("You are not the admin of this room", status=403)
        else:
            # Add the user to the User-Rooms Mapping
            user_room = UserRooms(user=Request.user, room=Request.room)
            user_room.save()
            # Increment the number of users in the room
            room = Room.objects.get(id=Request.room.id)
            room.numberUsers += 1
            room.save()
            # Delete the user from the Join Requests Mapping
            Request.delete()
            return HttpResponse("Accepted request", status=200)


# Reject Request
@login_required(login_url="login")
def reject_request(request):
    if request.method == "POST":
        # Get the request id
        data = json.loads(request.body)
        request_id = data["requestId"]
        # Get the joinRequest Mapping
        Request = JoinRequests.objects.get(id=request_id)
        # Check if the user is the admin of the room
        if Request.admin.id != request.user.id:
            return HttpResponse("You are not the admin of this room", status=403)
        else:
            # Simply delete the user from the Join Requests Mapping
            Request.delete()
            return HttpResponse("Rejected request", status=200)
        

# get joined rooms
@login_required(login_url="login")
def joined_rooms(request):
    # Get the list of rooms that the user has joined
    user_rooms = UserRooms.objects.filter(user=request.user)
    rooms = [room.room for room in user_rooms]
    return render(request, 'app/joined.html', {
        'rooms': rooms
    })


# Room
@login_required(login_url="login")
def room(request, room_name):
    if request.method == "POST":
        pass
    else:
        # Get the room
        room = Room.objects.get(name=room_name)

        # Check if the user is in the room or not
        # Apply filter to the User-Rooms Mapping
        user_rooms = UserRooms.objects.filter(user=request.user)
        rooms = [x.room for x in user_rooms]
        print(rooms)
        if room not in rooms and room.admin != request.user:
            return HttpResponse("<h1>You are not in this room</h1>", status=403)
        messages = Message.objects.filter(room=room)
        return render(request, 'app/room.html', {
            'room': room,
            'messages': messages
        })


# Send Message
@login_required(login_url="login")
def send_message(request):
    if request.method == "POST":
        # Get the message and the room id
        data = json.loads(request.body)
        message = data["message"]
        room_id = data["roomId"]
        # Get the room
        room = Room.objects.get(id=room_id)
        # Create a new message
        msg = Message.objects.create(user=request.user, room=room, message=message)
        msg.save()
        # Use pusher to send the message to the room
        pusher_client = pusher.Pusher(
            app_id='1565223',
            key='bc1914d6eafb6813d9e9',
            secret='3b281663a1ed82794093',
            cluster='ap2',
            ssl=True
        )
        # Trigger the event
        pusher_client.trigger(room.name, 'my-event', {'message': message, 'user': request.user.username})
        return HttpResponse("Message sent", status=200)