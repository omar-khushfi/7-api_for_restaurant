# Generated by Django 5.1.1 on 2024-09-17 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_rename_calories_meal_calories'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('cooking', 'Cooking'), ('in_queue', 'Inqueue'), ('eating', 'Eating')], default='in_queue', max_length=30),
        ),
        migrations.AddField(
            model_name='order',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
    ]
