from zigporter.commands.export import (
    _build_area_map,
    _build_entity_map,
    _build_state_map,
    _extract_entity_ids_from_automation,
    _match_automations_to_devices,
    build_export,
)


def test_build_area_map(area_registry_payload):
    result = _build_area_map(area_registry_payload)
    assert result == {"living_room": "Living Room", "kitchen": "Kitchen"}


def test_build_entity_map_filters_zha_only(entity_registry_payload):
    result = _build_entity_map(entity_registry_payload)
    # hue entity should be excluded
    assert "device-other" not in result
    assert "device-abc" in result
    assert "device-def" in result
    assert result["device-abc"][0]["entity_id"] == "climate.living_room_thermostat"


def test_build_state_map(states_payload):
    result = _build_state_map(states_payload)
    assert "climate.living_room_thermostat" in result
    assert result["climate.living_room_thermostat"]["state"] == "heat"


def test_extract_entity_ids_flat():
    config = {
        "action": [
            {
                "service": "climate.set_temperature",
                "target": {"entity_id": "climate.thermostat"},
            }
        ]
    }
    result = _extract_entity_ids_from_automation(config)
    assert "climate.thermostat" in result


def test_extract_entity_ids_list():
    config = {
        "action": [
            {
                "service": "homeassistant.turn_on",
                "entity_id": ["light.a", "light.b"],
            }
        ]
    }
    result = _extract_entity_ids_from_automation(config)
    assert "light.a" in result
    assert "light.b" in result


def test_extract_entity_ids_no_references():
    config = {"trigger": [{"platform": "time", "at": "07:00"}]}
    result = _extract_entity_ids_from_automation(config)
    assert result == []


def test_match_automations_to_devices(automation_configs_payload):
    entity_to_device = {"climate.living_room_thermostat": "device-abc"}
    result = _match_automations_to_devices(automation_configs_payload, entity_to_device)

    assert "device-abc" in result
    assert len(result["device-abc"]) == 1
    assert result["device-abc"][0].alias == "Morning Heat"
    assert "climate.living_room_thermostat" in result["device-abc"][0].entity_references


def test_match_automations_no_zha_entities(automation_configs_payload):
    # No ZHA entity references in device map
    result = _match_automations_to_devices(automation_configs_payload, {})
    assert result == {}


def test_build_export_device_count(
    zha_devices_payload,
    device_registry_payload,
    entity_registry_payload,
    area_registry_payload,
    states_payload,
    automation_configs_payload,
):
    export = build_export(
        zha_devices=zha_devices_payload,
        device_registry=device_registry_payload,
        entity_registry=entity_registry_payload,
        area_registry=area_registry_payload,
        states=states_payload,
        automation_configs=automation_configs_payload,
        ha_url="https://ha.test",
    )

    assert len(export.devices) == 2
    assert export.ha_url == "https://ha.test"


def test_build_export_device_names(
    zha_devices_payload,
    device_registry_payload,
    entity_registry_payload,
    area_registry_payload,
    states_payload,
    automation_configs_payload,
):
    export = build_export(
        zha_devices=zha_devices_payload,
        device_registry=device_registry_payload,
        entity_registry=entity_registry_payload,
        area_registry=area_registry_payload,
        states=states_payload,
        automation_configs=automation_configs_payload,
        ha_url="https://ha.test",
    )

    thermostat = next(d for d in export.devices if d.ieee == "00:11:22:33:44:55:66:77")
    assert thermostat.name == "Living Room Thermostat"
    assert thermostat.area_name == "Living Room"
    assert thermostat.manufacturer == "Danfoss"
    assert thermostat.quirk_applied is True


def test_build_export_entity_assigned_to_device(
    zha_devices_payload,
    device_registry_payload,
    entity_registry_payload,
    area_registry_payload,
    states_payload,
    automation_configs_payload,
):
    export = build_export(
        zha_devices=zha_devices_payload,
        device_registry=device_registry_payload,
        entity_registry=entity_registry_payload,
        area_registry=area_registry_payload,
        states=states_payload,
        automation_configs=automation_configs_payload,
        ha_url="https://ha.test",
    )

    thermostat = next(d for d in export.devices if d.ieee == "00:11:22:33:44:55:66:77")
    assert len(thermostat.entities) == 1
    assert thermostat.entities[0].entity_id == "climate.living_room_thermostat"
    assert thermostat.entities[0].state == "heat"


def test_build_export_automation_linked(
    zha_devices_payload,
    device_registry_payload,
    entity_registry_payload,
    area_registry_payload,
    states_payload,
    automation_configs_payload,
):
    export = build_export(
        zha_devices=zha_devices_payload,
        device_registry=device_registry_payload,
        entity_registry=entity_registry_payload,
        area_registry=area_registry_payload,
        states=states_payload,
        automation_configs=automation_configs_payload,
        ha_url="https://ha.test",
    )

    thermostat = next(d for d in export.devices if d.ieee == "00:11:22:33:44:55:66:77")
    assert len(thermostat.automations) == 1
    assert thermostat.automations[0].alias == "Morning Heat"


def test_build_export_empty_automations(
    zha_devices_payload,
    device_registry_payload,
    entity_registry_payload,
    area_registry_payload,
    states_payload,
):
    export = build_export(
        zha_devices=zha_devices_payload,
        device_registry=device_registry_payload,
        entity_registry=entity_registry_payload,
        area_registry=area_registry_payload,
        states=states_payload,
        automation_configs=[],
        ha_url="https://ha.test",
    )

    for device in export.devices:
        assert device.automations == []
