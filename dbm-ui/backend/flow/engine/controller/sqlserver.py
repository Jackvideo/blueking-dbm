"""
TencentBlueKing is pleased to support the open source community by making 蓝鲸智云-DB管理系统(BlueKing-BK-DBM) available.
Copyright (C) 2017-2023 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at https://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
from backend.flow.engine.bamboo.scene.sqlserver.sqlserver_backup_dbs import SqlserverBackupDBSFlow
from backend.flow.engine.bamboo.scene.sqlserver.sqlserver_clean_dbs import SqlserverCleanDBSFlow
from backend.flow.engine.bamboo.scene.sqlserver.sqlserver_ha_deploy import SqlserverHAApplyFlow
from backend.flow.engine.bamboo.scene.sqlserver.sqlserver_rename_dbs import SqlserverRenameDBSFlow
from backend.flow.engine.bamboo.scene.sqlserver.sqlserver_single_deploy import SqlserverSingleApplyFlow
from backend.flow.engine.bamboo.scene.sqlserver.sqlserver_sql_execute import SqlserverSQLExecuteFlow
from backend.flow.engine.controller.base import BaseController


class SqlserverController(BaseController):
    """
    sqlserver 相关调用
    """

    def single_cluster_apply_scene(self):
        flow = SqlserverSingleApplyFlow(root_id=self.root_id, data=self.ticket_data)
        flow.run_flow()

    def ha_cluster_apply_scene(self):
        flow = SqlserverHAApplyFlow(root_id=self.root_id, data=self.ticket_data)
        flow.run_flow()

    def sql_file_execute_scene(self):
        flow = SqlserverSQLExecuteFlow(root_id=self.root_id, data=self.ticket_data)
        flow.run_flow()

    def backup_dbs_scene(self):
        flow = SqlserverBackupDBSFlow(root_id=self.root_id, data=self.ticket_data)
        flow.run_flow()

    def rename_dbs_scene(self):
        flow = SqlserverRenameDBSFlow(root_id=self.root_id, data=self.ticket_data)
        flow.run_flow()

    def clean_dbs_scene(self):
        flow = SqlserverCleanDBSFlow(root_id=self.root_id, data=self.ticket_data)
        flow.run_flow()