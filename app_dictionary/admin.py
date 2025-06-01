from django.contrib import admin
from .models import ItemlistModel,BillModel,ItemModel,ProfileModel
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.admin import UserAdmin
# from .models import User


class itemsetup(admin.ModelAdmin):
    list_display = ["id","name","prize"]
    list_display_links = list_display
    ordering = ["name"]

# Register your models here.
admin.site.register(ItemlistModel)
admin.site.register(BillModel)
admin.site.register(ItemModel,itemsetup)
admin.site.register(User)
admin.site.register(ProfileModel)