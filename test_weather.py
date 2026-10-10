import urllib.error
from unittest.mock import MagicMock, patch

import pytest

from weather import current_temperature


def mock_response(json_data: str):
    """Helper to create a mock urllib response object for context manager usage."""
    cm = MagicMock()
    response = MagicMock()
    response.read.return_value = json_data.encode("utf-8")
    cm.__enter__.return_value = response
    cm.__exit__.return_value = None
    return cm


@patch("urllib.request.urlopen")
def test_current_temperature_success(mock_urlopen):
    json_data = '{"current": {"temperature_2m": 21.5}}'
    mock_urlopen.return_value = mock_response(json_data)

    temp = current_temperature(52.52, 13.41)

    assert temp == 21.5
    expected_url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=52.52&longitude=13.41&current=temperature_2m"
    )
    mock_urlopen.assert_called_once_with(
        expected_url,
        timeout=10,
    )


@pytest.mark.parametrize(
    "lat,lon",
    [
        (90.1, 0.0),
        (-90.1, 0.0),
        (100.0, 50.0),
        (-100.0, -50.0),
    ],
)
@patch("urllib.request.urlopen")
def test_current_temperature_invalid_latitude(mock_urlopen, lat, lon):
    with pytest.raises(ValueError):
        current_temperature(lat, lon)
    mock_urlopen.assert_not_called()


@pytest.mark.parametrize(
    "lat,lon",
    [
        (0.0, 180.1),
        (0.0, -180.1),
        (50.0, 200.0),
        (-50.0, -200.0),
    ],
)
@patch("urllib.request.urlopen")
def test_current_temperature_invalid_longitude(mock_urlopen, lat, lon):
    with pytest.raises(ValueError):
        current_temperature(lat, lon)
    mock_urlopen.assert_not_called()


@pytest.mark.parametrize(
    "lat,lon",
    [
        (90.0, 180.0),
        (-90.0, -180.0),
        (0.0, 0.0),
    ],
)
@patch("urllib.request.urlopen")
def test_current_temperature_boundary_coordinates(mock_urlopen, lat, lon):
    json_data = '{"current": {"temperature_2m": 0.0}}'
    mock_urlopen.return_value = mock_response(json_data)

    temp = current_temperature(lat, lon)
    assert temp == 0.0


@patch("urllib.request.urlopen")
def test_current_temperature_network_error(mock_urlopen):
    mock_urlopen.side_effect = urllib.error.URLError("Network unreachable")

    with pytest.raises(RuntimeError, match="Failed to fetch weather data"):
        current_temperature(10.0, 10.0)


@patch("urllib.request.urlopen")
def test_current_temperature_timeout(mock_urlopen):
    mock_urlopen.side_effect = TimeoutError("Connection timed out")

    with pytest.raises(RuntimeError, match="Failed to fetch weather data"):
        current_temperature(10.0, 10.0)


@patch("urllib.request.urlopen")
def test_current_temperature_invalid_json(mock_urlopen):
    mock_urlopen.return_value = mock_response("not valid json")

    with pytest.raises(RuntimeError, match="Failed to fetch weather data"):
        current_temperature(10.0, 10.0)


@patch("urllib.request.urlopen")
def test_current_temperature_non_dict_json(mock_urlopen):
    mock_urlopen.return_value = mock_response("[1, 2, 3]")

    with pytest.raises(RuntimeError, match="Invalid JSON payload"):
        current_temperature(10.0, 10.0)


@patch("urllib.request.urlopen")
def test_current_temperature_missing_current(mock_urlopen):
    mock_urlopen.return_value = mock_response('{"latitude": 10.0}')

    with pytest.raises(RuntimeError, match="Response missing 'current' object"):
        current_temperature(10.0, 10.0)


@patch("urllib.request.urlopen")
def test_current_temperature_missing_temperature_field(mock_urlopen):
    payload = '{"current": {"time": "2023-01-01T00:00"}}'
    mock_urlopen.return_value = mock_response(payload)

    with pytest.raises(RuntimeError, match="Response missing 'temperature_2m' field"):
        current_temperature(10.0, 10.0)


@patch("urllib.request.urlopen")
def test_current_temperature_null_temperature_value(mock_urlopen):
    payload = '{"current": {"temperature_2m": null}}'
    mock_urlopen.return_value = mock_response(payload)

    with pytest.raises(RuntimeError, match="Response missing 'temperature_2m' field"):
        current_temperature(10.0, 10.0)


@patch("urllib.request.urlopen")
def test_current_temperature_invalid_temperature_type(mock_urlopen):
    payload = '{"current": {"temperature_2m": "invalid"}}'
    mock_urlopen.return_value = mock_response(payload)

    with pytest.raises(RuntimeError, match="Invalid temperature format"):
        current_temperature(10.0, 10.0)
