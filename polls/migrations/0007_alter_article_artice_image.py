# Generated by Django 4.0.3 on 2022-03-23 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_article_artice_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='artice_image',
            field=models.ImageField(blank=True, upload_to='articles/'),
        ),
    ]
