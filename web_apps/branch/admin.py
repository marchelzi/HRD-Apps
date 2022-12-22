from django.contrib import admin

from branch.models import Branch, HeadQuarter

# Register your models here.
admin.site.site_header = "Admin Panel"
admin.site.register(Branch)
admin.site.register(HeadQuarter)
