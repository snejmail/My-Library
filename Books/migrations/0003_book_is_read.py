# Generated by Django 4.2.2 on 2024-08-29 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Books', '0002_alter_book_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
    ]
