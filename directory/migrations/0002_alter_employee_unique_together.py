# Generated by Django 3.2 on 2022-04-10 16:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='employee',
            unique_together={('person', 'department')},
        ),
    ]
