# Generated by Django 2.1.2 on 2018-10-07 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matchups', '0006_participant_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
