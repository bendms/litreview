from django.contrib import admin
from authentication.models import CustomUser, UserFollows
from reviews_app.models import Ticket, Review

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Ticket)
admin.site.register(Review)
admin.site.register(UserFollows)
