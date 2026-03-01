# zigporter

Home Assistant device management from the command line — migrate from ZHA to Zigbee2MQTT,
rename entities and devices with full cascade across automations, scripts, and dashboards.

## Features

| Command | Description |
|---|---|
| [`migrate`](guide/migration-wizard.md) | Interactive wizard: remove from ZHA → factory reset → pair with Z2M → restore names, areas, and entity IDs |
| [`rename-entity`](guide/rename.md#rename-an-entity) | Rename a HA entity ID and cascade the change across automations, scripts, scenes, and all Lovelace dashboards |
| [`rename-device`](guide/rename.md#rename-a-device) | Rename any HA device by name and cascade the change to all its entities and references |
| `check` | Verify HA and Z2M connectivity before making changes |
| `inspect` | Show a device's current state across ZHA, Z2M, and the HA registry |
| `export` | Snapshot your ZHA device inventory to JSON |
| `list-z2m` | List all devices currently paired with Zigbee2MQTT |

## Installation

```bash
uv tool install zigporter
```

## Quick start

### Migrate ZHA → Zigbee2MQTT

```bash
zigporter setup   # configure credentials once
zigporter check   # verify connectivity
zigporter migrate # start the interactive wizard
```

### Rename an entity

```bash
# Preview what would change
zigporter rename-entity light.old_name light.new_name

# Apply the rename
zigporter rename-entity light.old_name light.new_name --apply
```

### Rename a device

```bash
zigporter rename-device "Old Device Name" "New Device Name" --apply
```

---

See [Installation](getting-started/installation.md) and [Configuration](getting-started/configuration.md) to get set up.
