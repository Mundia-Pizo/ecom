# Generated by Django 2.2.5 on 2019-10-09 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0002_billingaddress'),
    ]

    operations = [
        migrations.AddField(
            model_name='billingaddress',
            name='zip',
            field=models.CharField(default='1223', max_length=20),
            preserve_default=False,
        ),
    ]
