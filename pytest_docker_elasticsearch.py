"""Docker Elasticsearch fixtures.

"""
import os
import pytest
import elasticsearch
from lovely.pytest.docker.compose import Services


@pytest.fixture(scope='session')
def elasticsearch_docker_compose_files(pytestconfig):
    """Get the docker-compose.yml absolute path.
    """
    dirname = os.path.dirname(__file__)
    return [
        os.path.join(dirname,
                     'pytest_docker_elasticsearch',
                     'docker',
                     'docker-compose.yml'),
    ]


@pytest.fixture(scope='session')
def elasticsearch_docker_services(request,
                             pytestconfig,
                             elasticsearch_docker_compose_files,
                             docker_ip):
    """Provide the docker services as a pytest fixture.

    The services will be stopped after all tests are run.
    """
    keep_alive = request.config.getoption("--keepalive", False)
    project_name = "pytest{}".format(str(pytestconfig.rootdir))
    services = Services(elasticsearch_docker_compose_files,
                        docker_ip,
                        project_name)
    yield services
    if not keep_alive:
        services.shutdown()


@pytest.fixture(scope='session')
def elasticsearch_client(elasticsearch_docker_services):
    elasticsearch_docker_services.start('elasticsearch')
    elasticsearch_docker_services.wait_for_service('elasticsearch', 9200)

    client = elasticsearch.Elasticsearch()

    return client
