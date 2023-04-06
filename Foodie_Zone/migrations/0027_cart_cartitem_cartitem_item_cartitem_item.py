# Generated by Django 4.1.7 on 2023-03-30 15:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Foodie_Zone', '0026_delete_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id1', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('session_key', models.CharField(max_length=32, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Cust', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Foodie_Zone.customer')),
                ('cart1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Foodie_Zone.cart')),
            ],
        ),
        migrations.CreateModel(
            name='CartItem_Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('cart_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Foodie_Zone.cartitem')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Foodie_Zone.items')),
            ],
        ),
        migrations.AddField(
            model_name='cartitem',
            name='item',
            field=models.ManyToManyField(through='Foodie_Zone.CartItem_Item', to='Foodie_Zone.items'),
        ),
    ]