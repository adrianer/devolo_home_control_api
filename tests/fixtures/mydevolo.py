import pytest

from devolo_home_control_api.mydevolo import Mydevolo, GatewayOfflineError, WrongCredentialsError, WrongUrlError

from ..mocks.mock_mydevolo import MockMydevolo


@pytest.fixture()
def mydevolo(request):
    """ Create real mydevolo object with static test data. """
    mydevolo = Mydevolo()
    mydevolo._uuid = request.cls.user.get("uuid")
    yield mydevolo
    Mydevolo.del_instance()


@pytest.fixture()
def mock_mydevolo_full_url(mocker):
    """ Mock getting a gateway's full URL. """
    mocker.patch("devolo_home_control_api.mydevolo.Mydevolo.get_full_url", side_effect=MockMydevolo.get_full_url)


@pytest.fixture()
def mock_mydevolo__call(mocker, request):
    """ Mock calls to the mydevolo API. """
    mock_mydevolo = MockMydevolo(request)
    mocker.patch("devolo_home_control_api.mydevolo.Mydevolo._call", side_effect=mock_mydevolo._call)
    del mock_mydevolo


@pytest.fixture()
def mock_mydevolo__call_raise_GatewayOfflineError(mocker):
    """ Respond with GatewayOfflineError on calls to the mydevolo API. """
    mocker.patch("devolo_home_control_api.mydevolo.Mydevolo._call", side_effect=GatewayOfflineError)


@pytest.fixture()
def mock_mydevolo__call_raise_WrongCredentialsError(mocker):
    """ Respond with WrongCredentialsError on calls to the mydevolo API. """
    mocker.patch("devolo_home_control_api.mydevolo.Mydevolo.uuid", side_effect=WrongCredentialsError)


@pytest.fixture()
def mock_mydevolo__call_raise_WrongUrlError(mocker):
    """ Respond with WrongUrlError on calls to the mydevolo API. """
    mocker.patch("devolo_home_control_api.mydevolo.Mydevolo._call", side_effect=WrongUrlError)


@pytest.fixture()
def mock_get_zwave_products(mocker):
    """ Mock Z-Wave product information call to speed up tests. """
    mocker.patch("devolo_home_control_api.mydevolo.Mydevolo.get_zwave_products", return_value={})
