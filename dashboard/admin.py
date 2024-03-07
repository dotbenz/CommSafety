from django.contrib import admin
from .models import AnonymousReport, CitizenReport, Profile

# Register your models here.
admin.site.register(AnonymousReport)
admin.site.register(CitizenReport)
admin.site.register(Profile)
