# Generated by Django 4.0.6 on 2024-09-02 11:54

from django.db import migrations, models
import myauth.models


class Migration(migrations.Migration):

    dependencies = [
        ('myauth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(null=True, upload_to=myauth.models.profile_avatar_directory_path),
        ),
    ]
