# Generated by Django 5.1.5 on 2025-02-11 22:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('brands', '0001_initial'),
        ('categories', '0001_initial'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('idOrder', models.AutoField(primary_key=True, serialize=False)),
                ('order_type', models.CharField(choices=[('quote', 'Cotización'), ('purchase', 'Compra')], default='quote', max_length=10)),
                ('status', models.CharField(choices=[('pending', 'Pendiente'), ('confirmed', 'Confirmado'), ('cancelled', 'Cancelado')], default='pending', max_length=10)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'orders',
            },
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('idDetail', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.PositiveIntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'db_table': 'order_details',
            },
        ),
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('idBanner', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('image', models.ImageField(upload_to='banners/')),
                ('url', models.URLField(blank=True, null=True)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('is_active', models.BooleanField(default=True)),
                ('position', models.CharField(choices=[('carousel', 'Carrusel'), ('section', 'Sección fija'), ('both', 'Ambos')], default='carousel', max_length=10)),
                ('layout', models.CharField(choices=[('row', 'Fila'), ('grid', 'Cuadrícula')], default='row', max_length=5)),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='brands.brand')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='categories.category')),
            ],
            options={
                'db_table': 'banners',
            },
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('idOffer', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('discount_percentage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('status', models.CharField(choices=[('active', 'Activa'), ('inactive', 'Inactiva')], default='active', max_length=10)),
                ('is_global', models.BooleanField(default=False)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='categories.category')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.product')),
            ],
            options={
                'db_table': 'offers',
            },
        ),
        migrations.CreateModel(
            name='OfferDetail',
            fields=[
                ('idOfferDetail', models.AutoField(primary_key=True, serialize=False)),
                ('price_with_discount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogs.offer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
            options={
                'db_table': 'offer_details',
            },
        ),
    ]
