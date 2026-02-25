import json

import httpx
import pytest
import respx  # used by @respx.mock decorator

from zigporter.ha_client import HAClient


HA_URL = "https://ha.test"
TOKEN = "test-token"


@pytest.fixture
def client() -> HAClient:
    return HAClient(ha_url=HA_URL, token=TOKEN, verify_ssl=False)


async def test_get_zha_devices(client, zha_devices_payload, mocker):
    messages = [
        json.dumps({"type": "auth_required"}),
        json.dumps({"type": "auth_ok"}),
        json.dumps({"id": 1, "type": "result", "success": True, "result": zha_devices_payload}),
    ]
    mock_ws = mocker.AsyncMock()
    mock_ws.recv = mocker.AsyncMock(side_effect=messages)
    mock_ws.__aenter__ = mocker.AsyncMock(return_value=mock_ws)
    mock_ws.__aexit__ = mocker.AsyncMock(return_value=False)
    mocker.patch("websockets.connect", return_value=mock_ws)

    result = await client.get_zha_devices()
    assert len(result) == 2
    assert result[0]["ieee"] == "00:11:22:33:44:55:66:77"


@respx.mock
async def test_get_states(client, states_payload):
    respx.get(f"{HA_URL}/api/states").mock(
        return_value=httpx.Response(200, json=states_payload)
    )
    result = await client.get_states()
    assert any(s["entity_id"] == "climate.living_room_thermostat" for s in result)


async def test_get_zha_devices_ws_command_failure(client, mocker):
    messages = [
        json.dumps({"type": "auth_required"}),
        json.dumps({"type": "auth_ok"}),
        json.dumps({"id": 1, "type": "result", "success": False, "error": {"code": "unknown_command"}}),
    ]
    mock_ws = mocker.AsyncMock()
    mock_ws.recv = mocker.AsyncMock(side_effect=messages)
    mock_ws.__aenter__ = mocker.AsyncMock(return_value=mock_ws)
    mock_ws.__aexit__ = mocker.AsyncMock(return_value=False)
    mocker.patch("websockets.connect", return_value=mock_ws)

    with pytest.raises(RuntimeError, match="command failed"):
        await client.get_zha_devices()


@respx.mock
async def test_get_states_http_error(client):
    respx.get(f"{HA_URL}/api/states").mock(
        return_value=httpx.Response(403)
    )
    with pytest.raises(httpx.HTTPStatusError):
        await client.get_states()


async def test_ws_command_auth_failure(client, mocker):
    messages = [
        json.dumps({"type": "auth_required"}),
        json.dumps({"type": "auth_invalid", "message": "Invalid token"}),
    ]

    mock_ws = mocker.AsyncMock()
    mock_ws.recv = mocker.AsyncMock(side_effect=messages)
    mock_ws.__aenter__ = mocker.AsyncMock(return_value=mock_ws)
    mock_ws.__aexit__ = mocker.AsyncMock(return_value=False)

    mocker.patch("websockets.connect", return_value=mock_ws)

    with pytest.raises(RuntimeError, match="authentication failed"):
        await client.get_entity_registry()


async def test_ws_command_unexpected_first_message(client, mocker):
    messages = [json.dumps({"type": "unexpected"})]

    mock_ws = mocker.AsyncMock()
    mock_ws.recv = mocker.AsyncMock(side_effect=messages)
    mock_ws.__aenter__ = mocker.AsyncMock(return_value=mock_ws)
    mock_ws.__aexit__ = mocker.AsyncMock(return_value=False)

    mocker.patch("websockets.connect", return_value=mock_ws)

    with pytest.raises(RuntimeError, match="auth_required"):
        await client.get_entity_registry()
