"""Shakeout the Elasticsearch docker instance.

"""
import json
import pytest
import elasticsearch


@pytest.mark.skipif(raises=Exception)
def test_docker_elasticsearch(elasticsearch_client):
    """Test a pristine Elasticsearch instance.
    """
    # List pristine Elasticsearch tables.
    received = elasticsearch_client.cluster.health()

    msg = 'Pristine Elasticsearch health check should return a response'
    assert received.get('cluster_name') == 'docker-cluster', msg
