from django.contrib import admin
from .models import Pessoa, Diario, Tags
# Register your models here.
admin.site.register(Pessoa)
admin.site.register(Diario)
admin.site.register(Tags)