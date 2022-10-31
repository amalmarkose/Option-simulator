from django.contrib import admin
from .models import dashboard, displaydata, optionchain, positions, builder, inview

# Register your models here.

admin.site.register(displaydata)
admin.site.register(positions)
admin.site.register(optionchain)
admin.site.register(dashboard)
admin.site.register(builder)
admin.site.register(inview)

