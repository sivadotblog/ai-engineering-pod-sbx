import json
import urllib.error
import urllib.request


def current_temperature(latitude: float, longitude: float) -> float:
    """Fetch current temperature in degrees Celsius for given location.

    Raises:
        ValueError: If latitude is not in [-90, 90] or longitude not in [-180, 180].
        RuntimeError: If API call fails, times out, or returns invalid response.
    """
    if not (-90.0 <= latitude <= 90.0):
        raise ValueError(f"Latitude must be between -90 and 90, got {latitude}")
    if not (-180.0 <= longitude <= 180.0):
        raise ValueError(f"Longitude must be between -180 and 180, got {longitude}")

    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}&longitude={longitude}&current=temperature_2m"
    )

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            payload = response.read().decode("utf-8")
            data = json.loads(payload)
    except (urllib.error.URLError, TimeoutError, OSError, ValueError) as err:
        raise RuntimeError(f"Failed to fetch weather data: {err}") from err

    if not isinstance(data, dict):
        raise RuntimeError("Invalid JSON payload: expected JSON object")

    current = data.get("current")
    if not isinstance(current, dict):
        raise RuntimeError("Response missing 'current' object")

    if "temperature_2m" not in current or current["temperature_2m"] is None:
        raise RuntimeError("Response missing 'temperature_2m' field in 'current'")

    try:
        return float(current["temperature_2m"])
    except (TypeError, ValueError) as err:
        raise RuntimeError(f"Invalid temperature format: {err}") from err
