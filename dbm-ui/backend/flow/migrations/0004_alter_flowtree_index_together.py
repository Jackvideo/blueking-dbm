# Generated by Django 3.2.25 on 2024-06-21 04:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("flow", "0003_flowtree_db_type"),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name="flowtree",
            index_together={("bk_biz_id", "db_type")},
        ),
    ]