# Generated by Django 2.2.5 on 2020-08-01 11:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0004_auto_20200801_1028'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=50, verbose_name='昵称')),
                ('content', models.TextField(verbose_name='内容')),
                ('date', models.DateField(auto_now=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.Articel', verbose_name='文章')),
            ],
            options={
                'verbose_name': '评论表',
                'db_table': 'comment',
            },
        ),
    ]