from django.contrib.auth.models import User
from django.db.models.functions import Coalesce
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from mart.models import App, Author, AppRating, AppComment, Cart, CartProduct, UserProfile, DiscountUser, Discount
from rest_framework.viewsets import ModelViewSet
from mart.serializers import AppSerializer, AppRatingSerializer, AppCommentSerializer, CartSerializer, \
    CartProductSerializer, UserProfileSerializer, DiscountUserSerializer, DiscountSerializer, UserRegistrationSerializer
from django.db.models import Avg, Value, Count


class AppViewSet(ModelViewSet):
    queryset = App.objects.all().annotate(avg_rating=Avg('appratings__rating')).annotate(
        count_comment=Count('comments__comment'))
    serializer_class = AppSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['author', 'genre', 'language']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'release_date']


class AppRatingViewSet(ModelViewSet):
    queryset = AppRating.objects.all()
    serializer_class = AppRatingSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AppCommentViewSet(ModelViewSet):
    queryset = AppComment.objects.all()
    serializer_class = AppCommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def perform_create(self, serializer):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        if self.request.user == cart.user:
            serializer.save(cart=cart)
        else:
            raise PermissionDenied("Вы не владелец этой корзины.")

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


class CartProductViewSet(ModelViewSet):
    queryset = CartProduct.objects.all()
    serializer_class = CartProductSerializer


class UserProfileViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user

        if UserProfile.objects.filter(user=user).exists():
            raise PermissionDenied("Вы не имеете права создавать несколько профилей.")

        serializer.save(user=user)

    def perform_update(self, serializer):
        user = self.request.user
        profile = self.get_object()

        if profile.user != user:
            raise PermissionDenied("Вы не имеете права редактировать этот профиль.")
        serializer.save()


class DiscountUserViewSet(ModelViewSet):
    queryset = DiscountUser.objects.all()
    serializer_class = DiscountUserSerializer


class DiscountViewSet(ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Пользователь успешно зарегистрирован!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET'])
# def export_users_to_file(request):
#     file_path = 'users_list.txt'
#
#     # Открываем файл для записи
#     with open(file_path, 'w') as file:
#         users = User.objects.all()
#         for user in users:
#             file.write(f'Username: {user.username}, Email: {user.email}\n')
#
#     return Response({"message": f"Данные пользователей записаны в файл: {file_path}"})
#

class export_users_to_file(APIView):
    permission_classes = [IsAdminUser,]
    def get(self,request):
        file_path = 'userlist.txt'
        with open(file_path,'w') as file:
            users = User.objects.all()
            for user in users:
                file.write(f'Username: {user.username}, Email: {user.email}\n')
        return Response({"message": f"Данные пользователей записаны в файл: {file_path}"})