# Generated by Django 3.2.5 on 2022-08-21 13:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='total_tax',
            new_name='tax',
        ),
        migrations.RemoveField(
            model_name='order',
            name='tax_data',
        ),
    ]
