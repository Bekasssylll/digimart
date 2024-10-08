from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from mart.models import App, Author, AppRating, AppComment, CartProduct, Cart, UserProfile, DiscountUser, Discount


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class AppSerializer(ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())
    avg_rating = serializers.FloatField()
    count_comment = serializers.IntegerField()

    class Meta:
        model = App
        fields = ['title', 'author', 'description', 'price', 'genre', 'language', "time_of", 'created_at', 'updated_at',
                  'avg_rating', 'count_comment']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = instance.author.name
        return representation


class AppRatingSerializer(serializers.ModelSerializer):
    app = serializers.PrimaryKeyRelatedField(queryset=App.objects.all())

    class Meta:
        model = AppRating
        fields = ['id', 'app', 'user', 'rating', 'opinion']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['app'] = instance.app.title
        representation['user'] = instance.user.username
        return representation


class AppCommentSerializer(ModelSerializer):
    app = PrimaryKeyRelatedField(queryset=App.objects.all())
    user = serializers.SerializerMethodField()

    class Meta:
        model = AppComment
        fields = ['id', 'app', 'user', 'comment']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['app'] = instance.app.title
        return representation

    def get_user(self, obj):
        return str(obj.user.username)


class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = ['app', 'quantity', 'cart']


class CartSerializer(serializers.ModelSerializer):
    total_price_with_discount = serializers.SerializerMethodField()
    total_price_without_discount = serializers.SerializerMethodField()
    products = CartProductSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['user', 'products', 'total_price_with_discount', 'total_price_without_discount']

    def get_total_price_without_discount(self, obj):
        total = 0
        for cart_products in obj.products.all():
            product_price = cart_products.app.price
            product_quantity = cart_products.quantity
            total = total + (product_price * product_quantity)
        return total

    def get_total_price_with_discount(self, obj):
        user = obj.user
        total = 0
        for cart_products in obj.products.all():
            product_price = cart_products.app.price
            product_quantity = cart_products.quantity
            try:
                discount_user = DiscountUser.objects.get(user=user, app=cart_products.app)
                discount_percent = discount_user.discount.percent
            except DiscountUser.DoesNotExist:
                discount_percent = 0
            discount_price = product_price * (1 - discount_percent / 100)
            total = total + (discount_price * product_quantity)
        return total


class UserProfileSerializer(ModelSerializer):
    user = serializers.SerializerMethodField

    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ('user',)

    def get_user(self, obj):
        return str(obj.user.username)


class DiscountUserSerializer(ModelSerializer):
    class Meta:
        model = DiscountUser
        fields = ['app', 'user', 'discount']


class DiscountSerializer(ModelSerializer):
    class Meta:
        model = Discount
        fields = ['name', 'percent']
