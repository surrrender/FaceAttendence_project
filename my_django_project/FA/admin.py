from django.contrib import admin

# Register your models here.
from .models import FaceEncoding
from .models import AbsentPerson
from .models import ClassInstance

admin.site.register(FaceEncoding)
admin.site.register(AbsentPerson)
admin.site.register(ClassInstance)
