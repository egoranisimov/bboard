# Generated by Django 3.2.4 on 2021-07-07 19:56

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boardapp', '0006_advertreply_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advert',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Содержание'),
        ),
    ]