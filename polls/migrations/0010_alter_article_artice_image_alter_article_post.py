# Generated by Django 4.0.3 on 2022-03-30 19:12

import cloudinary.models
from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0009_alter_article_editor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='artice_image',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, verbose_name='articles/'),
        ),
        migrations.AlterField(
            model_name='article',
            name='post',
            field=tinymce.models.HTMLField(),
        ),
    ]
