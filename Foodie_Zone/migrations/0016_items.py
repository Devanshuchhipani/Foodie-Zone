# Generated by Django 4.1.7 on 2023-03-12 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Foodie_Zone', '0015_delete_items'),
    ]

    operations = [
        migrations.CreateModel(
            name='Items',
            fields=[
                ('item_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('image', models.ImageField(upload_to='item')),
                ('ingredients', models.TextField()),
                ('price', models.FloatField()),
                ('is_available', models.BooleanField(default=True)),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Item Table',
            },
        ),
    ]
