"""
TencentBlueKing is pleased to support the open source community by making 蓝鲸智云-DB管理系统(BlueKing-BK-DBM) available.
Copyright (C) 2017-2023 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at https://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""

import logging

from pipeline.component_framework.component import Component

from backend.flow.plugins.components.collections.common.base_service import BaseService

logger = logging.getLogger("flow")


class SqlserverAddJobUserService(BaseService):
    """
    为Sqlserver单据添加job的临时本地账号，操作目标实例
    单据是以集群维度来添加，如果单据涉及到集群，应该统一添加账号密码，以便后续操作方便
    todo
    """

    def _execute(self, data, parent_data, callback=None) -> bool:

        return True


class SqlserverAddJobUserComponent(Component):
    name = __name__
    code = "sqlserver_add_job_user"
    bound_service = SqlserverAddJobUserService