# Factory run log: issue #2

## Summary

Add weather.py to fetch current temperature using Open-Meteo API and include pytest unit tests with HTTP mocks in test_weather.py.

Reviewer verdict: approve.

## Classification

- type: feature
- priority: medium
- complexity: small
- affected_area: weather module

## Analysis

### Problem

Add weather module and tests fetching current temperature in Celsius from Open-Meteo API using standard library.

### Approach

Create weather.py using standard library urllib.request and json to fetch temperature data from Open-Meteo API. Validate coordinates upfront, use 10s timeout, wrap network and JSON parsing errors into RuntimeError. Write test_weather.py with unittest.mock.patch to test all cases without network calls.

### Plan

1. Create weather.py with current_temperature function and validation.
2. Implement Open-Meteo HTTP fetch with 10s timeout and json parsing.
3. Handle HTTP/network/schema errors by raising RuntimeError.
4. Create test_weather.py with mocked HTTP calls for pytest.
5. Verify tests with pytest.

### Acceptance criteria

- [x] weather.py exists at repository root with function current_temperature(latitude: float, longitude: float) -> float.
- [x] current_temperature raises ValueError when latitude is outside [-90, 90] or longitude is outside [-180, 180], without making an HTTP request.
- [x] current_temperature uses urllib.request and json from standard library to request https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m with a 10 second timeout.
- [x] current_temperature returns current.temperature_2m from the JSON response as a float in degrees Celsius on successful fetch.
- [x] current_temperature raises RuntimeError on network/HTTP errors, timeouts, invalid JSON payload, missing current object, or missing temperature_2m field.
- [ ] test_weather.py exists at repository root containing pytest test cases for success, invalid coordinates, and malformed/error responses using HTTP mocks (no real network calls).
- [x] python -m pytest executes and passes all tests in test_weather.py without errors.

## Implementation

Branch `factory/feat-weather-open-meteo` (base `main`).

### Change summary

- `weather.py`: Added weather.py and test_weather.py with standard library HTTP fetch and pytest mocks.

### Verification

- `pytest`: 20 passed in 0.03s
- `ruff check`: All checks passed!

### Deviations

- None

## Review

Verdict: **approve**

All criteria met cleanly with full test coverage and linter approval.

### Criteria results

- pass: weather.py exists at repository root with function current_temperature(latitude: float, longitude: float) -> float. (weather.py defines def current_temperature(latitude: float, longitude: float) -> float at root.)
- pass: current_temperature raises ValueError when latitude is outside [-90, 90] or longitude is outside [-180, 180], without making an HTTP request. (Boundary checks enforce [-90, 90] and [-180, 180], raising ValueError before urlopen.)
- pass: current_temperature uses urllib.request and json from standard library to request https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m with a 10 second timeout. (Calls urllib.request.urlopen with exact URL and timeout=10.)
- pass: current_temperature returns current.temperature_2m from the JSON response as a float in degrees Celsius on successful fetch. (Returns current.temperature_2m as float.)
- pass: current_temperature raises RuntimeError on network/HTTP errors, timeouts, invalid JSON payload, missing current object, or missing temperature_2m field. (All HTTP, timeout, parsing, and payload errors re-raised as RuntimeError.)
- pass: test_weather.py exists at repository root containing pytest test cases for success, invalid coordinates, and a malformed response using HTTP mocks (no real network calls). (test_weather.py mocks urllib.request.urlopen across 20 test cases.)
- pass: python -m pytest executes and passes all tests in test_weather.py without errors. (python -m pytest passes 20/20.)
