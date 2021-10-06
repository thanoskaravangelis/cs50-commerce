from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE, DO_NOTHING, SET_NULL


class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', related_name = "users_saved")

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"Category: {self.name}"

class Listing(models.Model):
    title = models.CharField(max_length = 128)
    description = models.CharField(max_length = 1024)
    starting_bid = models.DecimalField(max_digits=8,decimal_places=2)
    closed = models.BooleanField(default=False)
    image = models.ImageField(upload_to="images/",blank=True,null=True)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL, related_name="listings", blank=True,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="my_listings")

    def __str__(self):
        return f"{self.pk}: {self.title}"

class Bid(models.Model):
    value = models.DecimalField(max_digits=8,decimal_places=2)
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE,related_name="listing_bids")
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="my_bids")

    def __str__(self):
        return f"{self.value} , made by {self.user.get_username()} in listing with id: {self.listing.id}"

class Comment(models.Model):
    text = models.CharField(max_length=128)
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="my_comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE,related_name="listing_comments")

    def __str__(self):
        return f"\"{self.text}\" made by {self.user.get_username()} in listing with id: {self.listing.id}"



