# Generated by Django 5.0.6 on 2024-05-22 01:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Cliente",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nome", models.CharField(max_length=50)),
                ("sobrenome", models.CharField(max_length=50)),
                ("email", models.EmailField(max_length=50)),
                ("cpf", models.CharField(max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name="Pet",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nome_pet", models.CharField(max_length=50)),
                ("data_nascimento_pet", models.DateField()),
                ("porte", models.CharField(max_length=7)),
                ("banhos", models.IntegerField(default=0)),
                ("tosas", models.IntegerField(default=0)),
                (
                    "cliente",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="clientes.cliente",
                    ),
                ),
            ],
        ),
    ]
