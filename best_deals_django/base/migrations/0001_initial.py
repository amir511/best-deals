# Generated by Django 2.1.3 on 2018-11-23 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('brand', models.CharField(max_length=255)),
                ('link', models.URLField()),
                ('old_price', models.CharField(max_length=255)),
                ('new_price', models.CharField(max_length=255)),
                ('image', models.URLField()),
                ('platform', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='product',
            unique_together={('product_id', 'platform')},
        ),
    ]
