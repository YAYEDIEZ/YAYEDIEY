from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['email', 'is_active', 'is_staff', 'is_superuser', 'date_joined']  # Retiré 'first_name' et 'last_name'
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('email',)  # Retiré 'first_name' et 'last_name'
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),  # Champ email et mot de passe
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),  # Champs permissions
        ('Important dates', {'fields': ('date_joined',)}),  # Champ date_joined
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser')  # Retiré 'first_name' et 'last_name'
        }),
    )
    
    # Retirer les champs non définis dans votre modèle User
    filter_horizontal = ()  # Ne pas utiliser 'groups' ou 'user_permissions'

# Enregistrez le modèle et l'admin personnalisé
admin.site.register(User, CustomUserAdmin)
