from django.contrib import admin
from . import models


admin.site.register(models.Item)
admin.site.register(models.Discount)
admin.site.register(models.Promocode)
admin.site.register(models.Tax)
