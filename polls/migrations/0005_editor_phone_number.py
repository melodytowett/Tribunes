# Generated by Django 4.0.3 on 2022-03-22 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_article'),
    ]

    operations = [
        migrations.AddField(
            model_name='editor',
            name='phone_number',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]