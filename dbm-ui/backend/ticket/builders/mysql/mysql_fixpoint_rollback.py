# -*- coding: utf-8 -*-
"""
TencentBlueKing is pleased to support the open source community by making 蓝鲸智云-DB管理系统(BlueKing-BK-DBM) available.
Copyright (C) 2017-2023 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at https://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
import datetime

from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from backend.flow.engine.controller.mysql import MySQLController
from backend.ticket import builders
from backend.ticket.builders.common.base import HostInfoSerializer
from backend.ticket.builders.common.constants import MySQLBackupSource
from backend.ticket.builders.common.field import DBTimezoneField
from backend.ticket.builders.mysql.base import (
    BaseMySQLTicketFlowBuilder,
    DBTableField,
    MySQLBaseOperateDetailSerializer,
)
from backend.ticket.constants import FlowRetryType, TicketType
from backend.utils.time import str2datetime


class MySQLFixPointRollbackDetailSerializer(MySQLBaseOperateDetailSerializer):
    class FixPointRollbackSerializer(serializers.Serializer):
        cluster_id = serializers.IntegerField(help_text=_("集群ID"))
        rollback_host = HostInfoSerializer(help_text=_("备份新机器"))
        backup_source = serializers.ChoiceField(help_text=_("备份源"), choices=MySQLBackupSource.get_choices())
        rollback_time = DBTimezoneField(
            help_text=_("回档时间"), required=False, allow_blank=True, allow_null=True, default=""
        )
        backupinfo = serializers.DictField(
            help_text=_("备份文件信息"), required=False, allow_null=True, allow_empty=True, default={}
        )
        databases = serializers.ListField(help_text=_("目标库列表"), child=DBTableField(db_field=True))
        databases_ignore = serializers.ListField(help_text=_("忽略库列表"), child=DBTableField(db_field=True))
        tables = serializers.ListField(help_text=_("目标table列表"), child=DBTableField())
        tables_ignore = serializers.ListField(help_text=_("忽略table列表"), child=DBTableField())

    infos = serializers.ListSerializer(help_text=_("定点构造信息"), child=FixPointRollbackSerializer())

    @classmethod
    def validate_rollback_info(cls, info, now):
        # 校验rollback_time和backupinfo参数至少存在一个
        if not info["rollback_time"] and not info["backupinfo"]:
            raise serializers.ValidationError(_("请保证rollback_time或backupinfo参数至少存在一个"))

        if not info["rollback_time"]:
            return

        # 校验定点回档时间不能大于当前时间
        rollback_time = str2datetime(info["rollback_time"])
        if rollback_time > now:
            raise serializers.ValidationError(_("定点时间{}不能晚于当前时间{}").format(rollback_time, now))

    def validate(self, attrs):
        # 校验集群是否可用
        super().validate_cluster_can_access(attrs)

        now = datetime.datetime.now(timezone.utc)
        for info in attrs["infos"]:
            self.validate_rollback_info(info, now)

        # TODO: 库表校验

        return attrs


class MySQLFixPointRollbackFlowParamBuilder(builders.FlowParamBuilder):
    controller = MySQLController.mysql_rollback_data_cluster_scene

    def format_ticket_data(self):
        # 获取定点回档的类型
        for info in self.ticket_data["infos"]:
            op_type = "BACKUPID" if info.get("backupinfo") else "TIME"
            info["rollback_type"] = f"{info['backup_source'].upper()}_AND_{op_type}"
            info["rollback_ip"] = info["rollback_host"]["ip"]
            info["bk_rollback"] = info.pop("rollback_host")


@builders.BuilderFactory.register(TicketType.MYSQL_ROLLBACK_CLUSTER)
class MysqlFixPointRollbackFlowBuilder(BaseMySQLTicketFlowBuilder):
    serializer = MySQLFixPointRollbackDetailSerializer
    inner_flow_builder = MySQLFixPointRollbackFlowParamBuilder
    inner_flow_name = _("定点构造执行")
    retry_type = FlowRetryType.MANUAL_RETRY
