from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    list_display = ('name', 'email', )
    search_fields = ('name', 'email', )
    filter_horizontal = ()

    fieldsets = ()
    readonly_fields = ()
    list_filter = ('is_active',)
    ordering = ('name',)

    add_fieldsets = (
        (None, {
            'classes':'wide',
            'fields': ('name', 'email',  'password1', 'password2'),
        }),
    )


admin.site.register(User, UserAdmin)
