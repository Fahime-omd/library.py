# Generated by Django 4.0.4 on 2022-05-29 15:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0005_alter_bookinstance_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back'], 'permissions': (('can_read_private_section', 'VIP_User'), ('user_watcher', 'UserWatcher'), ('librarian', 'Librarian'))},
        ),
    ]
