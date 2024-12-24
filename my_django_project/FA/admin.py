from django.contrib import admin

# Register your models here.
from .models import FaceEncoding


class FaceEncodingAdmin(admin.ModelAdmin):
    list_display = ('name', 'encoding')


# admin.site.register(FaceEncoding)
admin.site.register(FaceEncoding, FaceEncodingAdmin)
