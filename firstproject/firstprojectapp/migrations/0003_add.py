# Generated by Django 2.1.7 on 2019-03-18 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstprojectapp', '0002_login_emailid'),
    ]

    operations = [
        migrations.CreateModel(
            name='add',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emailid', models.CharField(max_length=50)),
                ('work', models.CharField(max_length=50)),
                ('starttime', models.CharField(max_length=100)),
                ('endtime', models.CharField(max_length=100)),
            ],
        ),
    ]