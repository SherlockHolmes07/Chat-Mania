import json
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import User, Room, UserRooms, Message, JoinRequests
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
    return render(request, 'app/index.html', {
        'rooms': rooms,
        'join_requests': join_requests,
        'x': x,
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
            name = form.cleaned_data["name"]
            description = form.cleaned_data["description"]
            # Create a new room
            room = Room(name=name, description=description, admin=request.user)
            room.save()
            # Add the user to the room
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
        return render(request, 'app/createroom.html', { # Render the same page with the form data
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
        data = json.loads(request.body)
        request_id = data["requestId"]     
        Request = JoinRequests.objects.get(id=request_id)
        if Request.admin.id != request.user.id:
            return HttpResponse("You are not the admin of this room", status=403)
        else:
            user_room = UserRooms(user=Request.user, room=Request.room)
            user_room.save()
            Request.delete()
            return HttpResponse("Accepted request", status=200)


# Reject Request
@login_required(login_url="login")
def reject_request(request):
    if request.method == "POST":
        data = json.loads(request.body)
        request_id = data["requestId"]
        Request = JoinRequests.objects.get(id=request_id)
        if Request.admin.id != request.user.id:
            return HttpResponse("You are not the admin of this room", status=403)
        else:
            Request.delete()
            return HttpResponse("Rejected request", status=200)