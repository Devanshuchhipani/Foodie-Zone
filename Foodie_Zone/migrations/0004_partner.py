# Generated by Django 4.1.7 on 2023-03-12 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Foodie_Zone', '0003_delete_partner'),
    ]

    operations = [
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Partners',
            },
        ),
    ]
