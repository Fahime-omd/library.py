# Generated by Django 4.0.4 on 2022-05-26 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0003_alter_bookinstance_borrower_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinstance',
            name='statuse',
            field=models.CharField(blank=True, choices=[('m', 'Maintenance'), ('o', 'On loan'), ('a', 'Available'), ('r', 'Reserved')], default='m', help_text='Book Availablity', max_length=1),
        ),
    ]