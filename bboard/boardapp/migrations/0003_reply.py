# Generated by Django 3.2.4 on 2021-07-01 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boardapp', '0002_alter_advert_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
