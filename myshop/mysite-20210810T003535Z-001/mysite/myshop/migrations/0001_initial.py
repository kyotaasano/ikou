# Generated by Django 3.2.5 on 2021-08-05 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Memo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='名前:')),
                ('dsc', models.CharField(max_length=200, verbose_name='説明:')),
                ('date', models.DateField(blank=True, null=True)),
                ('pic', models.CharField(max_length=200, verbose_name='画像:')),
            ],
        ),
    ]
