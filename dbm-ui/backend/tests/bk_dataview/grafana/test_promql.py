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
from backend.bk_dataview.grafana.promsql import extract_condition_from_promql


class TestGrafanaPromql:
    @staticmethod
    def test_grafana_promql():
        result = extract_condition_from_promql(
            "min(min_over_time(bkmonitor:exporter_dbm_redis_exporter:__default__:"
            'redis_config_maxmemory{cluster_domain="example.domain.db",instance_role="redis_master"}[1m]))'
        )
        assert result["cluster_domain"] == "example.domain.db"
        assert result["instance_role"] == "redis_master"

    @staticmethod
    def test_with_lhs():
        result = extract_condition_from_promql(
            "sum by(command) (rate(bkmonitor:exporter_dbm_mysqld_exporter:__default__:"
            'mysql_global_status_commands_total{cluster_domain="example.domain.db",'
            'command=~"select|insert|update|delete|replace|commit",instance_role="backend_master"}[2m])) >0'
        )
        assert result["cluster_domain"] == "example.domain.db"
        assert result["instance_role"] == "backend_master"

    @staticmethod
    def test_pulsar():
        result = extract_condition_from_promql(
            "sum by (topic) (sum_over_time(bkmonitor:pushgateway_dbm_pulsarbroker_bkpull:"
            'pulsar_throughput_in{app="test_app",cluster_domain="example.domain.db",'
            'namespace="test_namespace",topic="test_topic"}[1m]))'
        )
        assert result["cluster_domain"] == "example.domain.db"
        assert result["app"] == "test_app"
        assert result["topic"] == "test_topic"
        assert result["namespace"] == "test_namespace"