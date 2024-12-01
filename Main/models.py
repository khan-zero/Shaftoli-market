from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid


# Base model with UUID
class ShortUUIDModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Hashtags(ShortUUIDModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class UserAddress(ShortUUIDModel):
    address = models.TextField()

    def __str__(self):
        return self.address


class CustomUser(AbstractUser, ShortUUIDModel):
    address = models.ForeignKey(UserAddress, on_delete=models.CASCADE, related_name='users', null=True, blank=True)
    browsing_history = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='browsing_history', null=True, blank=True)
    reviewed_products = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='reviewed_products', null=True, blank=True)
    balance = models.FloatField(default=0.0)

    def __str__(self):
        return self.username


class Organization(ShortUUIDModel):
    name = models.CharField(max_length=255)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='organization')

    def __str__(self):
        return self.name


class ProductStatus(ShortUUIDModel):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('out_of_stock', 'Out of Stock'),
        ('discontinued', 'Discontinued'),
    ]
    status = models.CharField(max_length=30, choices=STATUS_CHOICES)

    def __str__(self):
        return self.status


class Product(ShortUUIDModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    org_price = models.FloatField()
    selling_price = models.FloatField()
    discount = models.FloatField(default=0)
    description = models.TextField()
    rating = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        default=0
    )
    status = models.ForeignKey(ProductStatus, on_delete=models.CASCADE, related_name='products')
    hashtag = models.ManyToManyField(Hashtags, related_name='products')

    def __str__(self):
        return self.name


class ProductImages(ShortUUIDModel):
    product = models.ManyToManyField(Product, related_name='images')
    img = models.ImageField()
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {', '.join([product.name for product in self.product.all()])}"


@receiver(post_save, sender=ProductImages)
def set_main_image(sender, instance, created, **kwargs):
    if created and not ProductImages.objects.filter(product__in=instance.product.all(), is_main=True).exists():
        instance.is_main = True
        instance.save()


class SalesHistory(ShortUUIDModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sales')
    quantity = models.PositiveIntegerField(default=1)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sale of {self.product.name} (Quantity: {self.quantity})"


class Cart(ShortUUIDModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='carts')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_quantity = models.IntegerField()

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"Cart for {self.user.username} with {self.product.name}"
