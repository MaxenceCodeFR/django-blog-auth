from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User  # Importer votre modèle personnalisé


# Personnalisation de l'affichage du modèle User dans l'admin
class CustomUserAdmin(UserAdmin):
    # Ajouter les champs personnalisés à l'affichage dans la liste
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')

    # Ajouter les champs personnalisés dans les sections de modification
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('profile_photo', 'role')}),
    )

    # Si vous souhaitez que ces champs apparaissent aussi lors de la création d'un utilisateur
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('profile_photo', 'role')}),
    )


# Enregistrer le modèle personnalisé User dans l'administration
admin.site.register(User, CustomUserAdmin)
