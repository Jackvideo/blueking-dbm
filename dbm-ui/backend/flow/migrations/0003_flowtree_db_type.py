# Generated by Django 3.2.25 on 2024-06-02 12:55
from collections import defaultdict

from django.db import migrations, models

from backend.configuration.constants import DBType
from backend.ticket.constants import TicketType


def init_flow_tree_db_type(apps, schema_editor):
    FlowTree = apps.get_model("flow", "FlowTree")
    flow_tree_list = []
    for flow in FlowTree.objects.all():
        try:
            flow.db_type = TicketType.get_db_type_by_ticket(flow.ticket_type)
            flow_tree_list.append(flow)
        except Exception:
            pass
    # 分批更新，设5000一次
    FlowTree.objects.bulk_update(flow_tree_list, fields=["db_type"], batch_size=5000)


class Migration(migrations.Migration):
    dependencies = [
        ("flow", "0002_auto_20240522_2046"),
    ]

    operations = [
        migrations.AddField(
            model_name="flowtree",
            name="db_type",
            field=models.CharField(choices=DBType.get_choices(), default="", max_length=64, verbose_name="组件类型"),
        ),
        migrations.RunPython(init_flow_tree_db_type),
    ]
