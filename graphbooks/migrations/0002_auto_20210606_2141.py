# Generated by Django 3.2.3 on 2021-06-06 16:41

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('graphbooks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='primary_genre',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='primary_genre_books', to='graphbooks.genre'),
        ),
        migrations.AlterField(
            model_name='book',
            name='rating',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(10)]),
        ),
    ]
