from django.contrib import admin
from . models import Category, Customer, Product, Order, Profile
from django.contrib.auth.models import User
# Register your models here.

# username = admin
# email = admin1@gmail.com
# password = praveen@1122


admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Profile)


# Mix Profile info and user info
class ProfileInline(admin.StackedInline):
    model = Profile


# Extend user model
class UserAdmin(admin.ModelAdmin):
    model = User
    field = ["username", "first_name", "last_name", "email"]
    inlines = [ProfileInline]

# Unregister the old way
admin.site.unregister(User)


# Re-register the old way
admin.site.register(User, UserAdmin)

