# Generated by Django 4.1.3 on 2023-02-23 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pakhsh', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(null=True, upload_to='product'),
        ),
        migrations.AlterField(
            model_name='product',
            name='moq',
            field=models.PositiveIntegerField(blank=True, default=1, null=True),
        ),
    ]