# Generated by Django 2.1.7 on 2019-03-21 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstprojectapp', '0004_auto_20190321_1917'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedules',
            name='status',
            field=models.CharField(default='Imcomplete', max_length=15),
        ),
        migrations.AlterField(
            model_name='login',
            name='email',
            field=models.CharField(max_length=38),
        ),
        migrations.AlterField(
            model_name='login',
            name='password',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='schedules',
            name='email',
            field=models.CharField(max_length=38),
        ),
        migrations.AlterField(
            model_name='schedules',
            name='work',
            field=models.TextField(max_length=100),
        ),
    ]