# Generated by Django 4.1.7 on 2023-06-19 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("PetopiaApp", "0009_payment_shoppingcart_payment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="product_category",
            field=models.CharField(
                choices=[
                    ("FD", "FOOD"),
                    ("HG", "HYGIENE"),
                    ("TS", "TOYS"),
                    ("TR", "TRANSPORT"),
                    ("OT", "OTHER"),
                ],
                max_length=2,
            ),
        ),
        migrations.DeleteModel(name="PetCategoryProductCategory",),
        migrations.DeleteModel(name="ProductCategory",),
    ]
