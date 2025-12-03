from django.contrib import admin
from .models import Developer, Game, UserProfile, Purchase, Review

admin.site.register(Developer)
admin.site.register(Game)
admin.site.register(UserProfile)
admin.site.register(Purchase)
admin.site.register(Review)
