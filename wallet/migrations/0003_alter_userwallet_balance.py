# Generated by Django 4.2.5 on 2024-03-14 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0002_alter_userwallet_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userwallet',
            name='balance',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
