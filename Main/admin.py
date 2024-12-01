from django.contrib import admin
from .models import (Hashtags, UserAddress, CustomUser, Organization,
                     ProductStatus, Product, ProductImages, SalesHistory,
                     Cart)

admin.site.register(Hashtags)
admin.site.register(UserAddress)
admin.site.register(CustomUser)
admin.site.register(Organization)
admin.site.register(ProductStatus)
admin.site.register(Product)
admin.site.register(ProductImages)
admin.site.register(SalesHistory)
admin.site.register(Cart)