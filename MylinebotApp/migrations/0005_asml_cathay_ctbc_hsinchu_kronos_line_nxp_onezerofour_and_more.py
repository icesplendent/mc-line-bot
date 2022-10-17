# Generated by Django 4.1.1 on 2022-10-17 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MylinebotApp', '0004_rename_chunghwa_user_info_hsinchu'),
    ]

    operations = [
        migrations.CreateModel(
            name='ASML',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(default='', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Cathay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(default='', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='CTBC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(default='', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Hsinchu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(default='', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Kronos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(default='', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='LINE',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(default='', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='NXP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(default='', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='onezerofour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(default='', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='PixArt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(default='', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='STM',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(default='', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='TSMC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(default='', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Yahoo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(default='', max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name='user_info',
            name='lottery',
            field=models.IntegerField(default=0),
        ),
    ]