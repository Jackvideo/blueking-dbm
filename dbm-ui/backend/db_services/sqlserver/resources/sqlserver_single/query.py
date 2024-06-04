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
from typing import Any, Dict, List

from django.utils.translation import ugettext_lazy as _

from backend.db_meta.api.cluster.sqlserversingle.detail import scan_cluster
from backend.db_meta.enums import InstanceInnerRole
from backend.db_meta.enums.cluster_type import ClusterType
from backend.db_meta.models.cluster import Cluster
from backend.db_services.dbbase.resources import query
from backend.db_services.dbbase.resources.register import register_resource_decorator


@register_resource_decorator()
class ListRetrieveResource(query.ListRetrieveResource):
    """查看 sqlserver ha 架构的资源"""

    cluster_types = [ClusterType.SqlserverSingle]

    fields = [
        {"name": _("集群名"), "key": "cluster_name"},
        {"name": _("主域名"), "key": "master_domain"},
        {"name": _("所属db模块"), "key": "db_module_name"},
        {"name": _("创建人"), "key": "creator"},
        {"name": _("创建时间"), "key": "create_at"},
    ]

    @classmethod
    def get_topo_graph(cls, bk_biz_id: int, cluster_id: int) -> dict:
        cluster = Cluster.objects.get(bk_biz_id=bk_biz_id, id=cluster_id)
        graph = scan_cluster(cluster).to_dict()
        return graph

    @classmethod
    def _to_cluster_representation(
        cls,
        cluster: Cluster,
        db_module_names_map: Dict[int, str],
        cluster_entry_map: Dict[int, Dict[str, str]],
        cluster_operate_records_map: Dict[int, List],
        **kwargs,
    ) -> Dict[str, Any]:
        """将集群对象转为可序列化的 dict 结构"""
        storages = [m.simple_desc for m in cluster.storages if m.instance_inner_role == InstanceInnerRole.ORPHAN]
        cluster_role_info = {"storages": storages}
        cluster_info = super()._to_cluster_representation(
            cluster, db_module_names_map, cluster_entry_map, cluster_operate_records_map, **kwargs
        )
        cluster_info.update(cluster_role_info)
        return cluster_info
