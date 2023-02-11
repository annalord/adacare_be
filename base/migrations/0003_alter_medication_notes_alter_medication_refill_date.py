# Generated by Django 4.1.5 on 2023-02-11 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_event_completed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medication',
            name='notes',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='medication',
            name='refill_date',
            field=models.CharField(max_length=25, null=True),
        ),
    ]
