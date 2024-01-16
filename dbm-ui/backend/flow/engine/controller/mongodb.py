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
from backend.flow.engine.bamboo.scene.mongodb.mongodb_backup import MongoBackupFlow
from backend.flow.engine.bamboo.scene.mongodb.mongodb_fake_install import MongoFakeInstallFlow
from backend.flow.engine.bamboo.scene.mongodb.mongodb_install import MongoDBInstallFlow
from backend.flow.engine.controller.base import BaseController


class MongoDBController(BaseController):
    """
    名字服务相关控制器
    """

    def multi_replicaset_create(self):
        """
        安装复制集
        """

        flow = MongoDBInstallFlow(root_id=self.root_id, data=self.ticket_data)
        flow.multi_replicaset_install_flow()

    def cluster_create(self):
        """
        cluster安装
        """

        flow = MongoDBInstallFlow(root_id=self.root_id, data=self.ticket_data)
        flow.cluster_install_flow()

    def mongo_backup(self):
        """
        发起备份任务
        """
        flow = MongoBackupFlow(root_id=self.root_id, data=self.ticket_data)
        flow.start()

    def fake_install(self):
        """
        在Meta中生成一个ReplicaSet，用于测试
        """
        flow = MongoFakeInstallFlow(root_id=self.root_id, data=self.ticket_data)
        flow.start()