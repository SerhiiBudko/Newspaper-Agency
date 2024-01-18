from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from newspaper.models import Topic, Redactor, Newspaper


@admin.register(Redactor)
class RedactorAdmin(UserAdmin):
    list_display = UserAdmin.list_display + (
        "username",
        "first_name",
        "last_name",
        "email"
    )
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("years_of_experience",)}),)
    )


@admin.register(Newspaper)
class NewspaperAdmin(admin.ModelAdmin):
    list_display = ("title", )
    search_fields = ("published_date", )


admin.site.register(Topic)
