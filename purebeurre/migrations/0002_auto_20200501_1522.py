# Generated by Django 3.0.5 on 2020-05-01 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purebeurre', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='code',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='code'),
        ),
    ]
