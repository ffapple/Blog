# Generated by Django 2.2.5 on 2020-07-31 15:36

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articel',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(verbose_name='内容'),
        ),
    ]
