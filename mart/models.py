from django.contrib.auth.models import User
from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name}"


class App(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    description = models.TextField()
    language = models.CharField(max_length=4)
    price = models.IntegerField()
    genre = models.CharField(max_length=15)
    time_of = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"


class AppRating(models.Model):
    RATE_CHOICES = [
        (1, 'very bad'),
        (2, 'bad'),
        (3, 'okay'),
        (4, 'good'),
        (5, 'excellent')
    ]

    app = models.ForeignKey(App, on_delete=models.CASCADE, related_name='appratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    rating = models.PositiveIntegerField(choices=RATE_CHOICES)
    opinion = models.TextField(default='no opinion')

    def __str__(self):
        return f" rating {self.rating} for {self.app}"


class AppComment(models.Model):
    app = models.ForeignKey(App, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return f"{self.user.username} comment {self.comment}for {self.app}"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}"


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='products')
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    quantity = models.IntegerField()


class UserProfile(models.Model):
    # HEALTH_STATUS_CHOICES = [
    #     ('healthy', 'No problem'),
    #     ('sick', 'Ill'),
    #     ('disabled', 'Invalid')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    surname = models.CharField(max_length=30)
    email = models.EmailField(max_length=50)
    # health_status = models.CharField(max_length=25,choices=HEALTH_STATUS_CHOICES,default='healthy')


class Discount(models.Model):
    percent_choices = [
        (0, "0"),
        (5, '5%'),
        (15, '15%'),
        (25, '25%'),
        (50, '50%')
    ]
    name = models.CharField(max_length=40)
    percent = models.IntegerField(choices=percent_choices, default=0)

    def __str__(self):
        return f"{self.name}"


class DiscountUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    app = models.ForeignKey(App, on_delete=models.CASCADE, related_name='discounts_app')
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, related_name='discounts')
