# Generated by Django 2.1.7 on 2019-03-18 13:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('firstprojectapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='login',
            name='emailid',
            field=models.CharField(default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
    ]