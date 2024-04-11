from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import User, Message


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
