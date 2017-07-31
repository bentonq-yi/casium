import pytest

from test_launcher.launcher import Launcher


@pytest.fixture(scope='module', autouse=True)
def auto_connect():
    l = Launcher()
    yield l
    l.device.disconnect()


def pytest_addoption(parser):
    parser.addoption('--repeat-count', action='store', default=3, help='Test case repeat count')


@pytest.fixture(scope='function')
def repeat_count(request):
    return int(request.config.getoption('--repeat-count'))
