from django.shortcuts import render, redirect
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Randonnee, Point, Photo
from .serializers import RandonneeSerializer, PointSerializer, PhotoSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

class RandonneeViewSet(viewsets.ModelViewSet):
    queryset = Randonnee.objects.all()
    serializer_class = RandonneeSerializer

    def list(self, request):
        randonnees = self.get_queryset()
        serializer = self.get_serializer(randonnees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            randonnee = self.get_object()
            serializer = self.get_serializer(randonnee)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Randonnee.DoesNotExist:
            return Response({"error": "Randonnée non trouvée"}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            randonnee = self.get_object()
            serializer = self.get_serializer(randonnee, data=request.data)
            if serializer.is_valid():
                self.perform_update(serializer)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Randonnee.DoesNotExist:
            return Response({"error": "Randonnée non trouvée"}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            randonnee = self.get_object()
            self.perform_destroy(randonnee)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Randonnee.DoesNotExist:
            return Response({"error": "Randonnée non trouvée"}, status=status.HTTP_404_NOT_FOUND)

class PointViewSet(viewsets.ModelViewSet):
    queryset = Point.objects.all()
    serializer_class = PointSerializer

class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        User.objects.create_user(username=username, password=password)
        return redirect('login')
    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')
