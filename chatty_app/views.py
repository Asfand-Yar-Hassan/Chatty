from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import ChatRoom, Message


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        email = data['email']
        try:
            User.objects.create_user(username, email, password)
            return JsonResponse({"message": f"user created successfully: {username}"}, status=201)
        except:
            return JsonResponse({"error": "Username already exists"}, status=409)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def login_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"message": f"Welcome, {username}"}, status=200)
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=404)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def logout_user(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            logout(request)
            return JsonResponse({'message': "Logout successful"}, status=200)
        else:
            return JsonResponse({"error": "User not logged in"}, status=400)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def create_chatroom(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            data = json.loads(request.body)
            chatroom_name = data["chatroom_name"]

            if not ChatRoom.objects.filter(name=chatroom_name).exists():
                ChatRoom.objects.create(name=chatroom_name)
                return JsonResponse({"message": "Chatroom created successfully"}, status=201)
            else:
                return JsonResponse({"error": "Chatroom alread exist"}, status=409)
        else:
            return JsonResponse({"error": "User must be logged"}, status=401)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def join_chatroom(request, chatroom_name):
    if request.method == "POST":
        if request.user.is_authenticated:
            try:
                chatroom = ChatRoom.objects.get(name=chatroom_name)
                if request.user.chatrooms.filter(name=chatroom_name).exists():
                    return JsonResponse({"error": "User has already joined this chatroom"}, status=400)
                else:
                    request.user.chatrooms.add(chatroom)
                    chatroom.update_user_count()
                    return JsonResponse({"message": f"Chatroom {chatroom_name} joined successfully"}, status=200)
            except ChatRoom.DoesNotExist:
                return JsonResponse({"error": "Chatroom does not exist"}, status=404)
        else:
            return JsonResponse({"error": "User must be logged in"}, status=401)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def leave_chatroom(request, chatroom_name):
    if request.method == "POST":
        if request.user.is_authenticated:
            try:
                chatroom = ChatRoom.objects.get(name=chatroom_name)
                if request.user.chatrooms.filter(name=chatroom_name).exists():
                    request.user.chatrooms.remove(chatroom)
                    chatroom.update_user_count()
                    return JsonResponse({"message": "Chatroom left successfully"}, status=200)
                else:
                    return JsonResponse({"error": "User is not a member of this chatroom"}, status=400)
            except ChatRoom.DoesNotExist:
                return JsonResponse({"error": "Chatroom does not exist"}, status=404)
        else:
            return JsonResponse({"error": "User must be logged in"}, status=401)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)
