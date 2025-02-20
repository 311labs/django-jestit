# Generated by Django 4.2.19 on 2025-02-20 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jestit', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jestitlog',
            name='method',
            field=models.CharField(default=None, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='jestitlog',
            name='kind',
            field=models.CharField(db_index=True, default=None, max_length=200, null=True),
        ),
    ]
