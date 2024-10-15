from django.db import migrations, IntegrityError


def create_groups(apps, schema_editor):
    User = apps.get_model('authentication', 'User')
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    # Vérifier si les permissions existent et les récupérer
    try:
        add_photo = Permission.objects.get(codename='add_photo')
        change_photo = Permission.objects.get(codename='change_photo')
        delete_photo = Permission.objects.get(codename='delete_photo')
        view_photo = Permission.objects.get(codename='view_photo')
    except Permission.DoesNotExist as e:
        print(f"Permission missing: {e}")
        return

    # Liste des permissions pour les créateurs
    creator_permissions = [
        add_photo,
        change_photo,
        delete_photo,
        view_photo,
    ]

    # Créer ou récupérer le groupe "creators"
    creators, created = Group.objects.get_or_create(name="creators")
    if created:
        print("Group 'creators' created.")
    else:
        print("Group 'creators' already exists.")

    # Associer les permissions au groupe
    creators.permissions.set(creator_permissions)

    # Créer ou récupérer le groupe "subscribers"
    subscribers, created = Group.objects.get_or_create(name="subscribers")
    if created:
        print("Group 'subscribers' created.")
    else:
        print("Group 'subscribers' already exists.")

    # Associer la permission de visualisation au groupe subscribers
    subscribers.permissions.add(view_photo)

    # Associer les utilisateurs aux groupes en fonction de leur rôle
    for user in User.objects.all():
        print(f"Processing user: {user.username} with role: {user.role}")  # Debug line
        if user.role == 'CREATOR':
            print(f"Adding {user.username} to creators")
            creators.user_set.add(user)
        elif user.role == 'SUBSCRIBER':
            print(f"Adding {user.username} to subscribers")
            subscribers.user_set.add(user)


class Migration(migrations.Migration):
    dependencies = [
        ('authentication', '0002_alter_user_profile_photo'),
    ]

    operations = [
        migrations.RunPython(create_groups)
    ]
