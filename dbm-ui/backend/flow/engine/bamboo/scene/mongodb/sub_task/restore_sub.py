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
from typing import Dict, List, Optional, Tuple

from django.utils.translation import ugettext as _

from backend.flow.consts import MongoDBActuatorActionEnum
from backend.flow.engine.bamboo.scene.common.builder import SubBuilder
from backend.flow.engine.bamboo.scene.mongodb.sub_task.base_subtask import BaseSubTask
from backend.flow.plugins.components.collections.mongodb.exec_actuator_job2 import ExecJobComponent2
from backend.flow.utils.mongodb.mongodb_dataclass import CommonContext
from backend.flow.utils.mongodb.mongodb_repo import MongoDBCluster, MongoDBNsFilter, MongoNode
from backend.flow.utils.mongodb.mongodb_util import MongoUtil


# RestoreSubTask 处理某个Cluster的Restore
class RestoreSubTask(BaseSubTask):
    """
    payload: 整体的ticket_data
    sub_payload: 这个子任务的ticket_data
    rs:
    """

    @classmethod
    def make_kwargs(
        cls, sub_payload: Dict, file_path, dest_dir: str, exec_node: MongoNode, dest_node: MongoNode, dest_type: str
    ) -> dict:
        ns_filter = sub_payload.get("ns_filter")
        is_partial = MongoDBNsFilter.is_partial(ns_filter)
        dba_user, dba_pwd = MongoUtil.get_dba_user_password(dest_node.ip, dest_node.port, dest_node.bk_cloud_id)
        return {
            "set_trans_data_dataclass": CommonContext.__name__,
            "get_trans_data_ip_var": None,
            "bk_cloud_id": exec_node.bk_cloud_id,
            "exec_ip": exec_node.ip,
            "db_act_template": {
                "action": MongoDBActuatorActionEnum.Restore,
                "file_path": file_path,
                "exec_account": "root",
                "sudo_account": "mysql",
                "payload": {
                    "ip": dest_node.ip,
                    "port": int(dest_node.port),
                    "dest_type": dest_type,
                    "adminUsername": dba_user,
                    "adminPassword": dba_pwd,
                    "args": {
                        "srcFile": sub_payload["task_ids"],
                        "isPartial": is_partial,
                        "oplog": False,
                        "nsFilter": sub_payload["ns_filter"],
                        "recoverDir": dest_dir,
                    },
                },
            },
        }

    @classmethod
    def process_cluster(
        cls,
        root_id: str,
        ticket_data: Optional[Dict],
        sub_ticket_data: Optional[Dict],
        cluster: MongoDBCluster,
        file_path,
        dest_dir: str,
        exec_node: MongoNode,
    ) -> Tuple[SubBuilder, List]:
        """
        cluster can be  a ReplicaSet or  a ShardedCluster
        """

        # 创建子流程
        sub_pipeline = SubBuilder(root_id=root_id, data=ticket_data)
        acts_list = []

        # 导入数据时，集群只使用一个分片，待完善.
        rs = cluster.get_shards()[0]
        if cluster.is_sharded_cluster():
            dest_node = cluster.get_mongos()[0]
            dest_type = "mongos"
        else:
            dest_node = exec_node
            dest_type = "mongod"

        kwargs = cls.make_kwargs(sub_ticket_data, file_path, dest_dir, exec_node, dest_node, dest_type)
        acts_list.append(
            {
                "act_name": _("{} {}".format(rs.set_name, kwargs["exec_ip"])),
                "act_component_code": ExecJobComponent2.code,
                "kwargs": kwargs,
            }
        )

        sub_pipeline.add_parallel_acts(acts_list=acts_list)
        sub_bk_host_list = []
        for v in acts_list:
            sub_bk_host_list.append({"ip": v["kwargs"]["exec_ip"], "bk_cloud_id": v["kwargs"]["bk_cloud_id"]})

        return sub_pipeline, sub_bk_host_list
