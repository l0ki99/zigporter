<!-- markdownlint-disable MD013 -->
# zigporter

CLI tool to migrate Zigbee devices from ZHA to Zigbee2MQTT in Home Assistant.
Runs an interactive per-device wizard with persistent state so migrations can
be paused and resumed across sessions.

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)
- Home Assistant with ZHA and Zigbee2MQTT add-on

## Setup

```bash
uv sync
cp .env.example .env   # fill in your values
```

### .env

```dotenv
HA_URL=https://your-ha-instance.local
HA_TOKEN=your_long_lived_access_token
HA_VERIFY_SSL=true                   # false for self-signed certs
Z2M_URL=https://your-ha-instance.local/45df7312_zigbee2mqtt
Z2M_MQTT_TOPIC=zigbee2mqtt           # only if non-default
```

`HA_TOKEN` is a [Long-Lived Access Token](https://www.home-assistant.io/docs/authentication/#your-account-profile) from your HA profile page.

## Usage

```bash
# 1. Export your ZHA device inventory
uv run zigporter export

# 2. (Optional) inspect what's already in Z2M
uv run zigporter list-z2m

# 3. Run the migration wizard
#    ZHA_EXPORT defaults to the most recent zha-export-*.json in the current dir
uv run zigporter migrate [ZHA_EXPORT]

# Check progress without entering the wizard
uv run zigporter migrate --status
```

## Migration wizard

Run once per device. The wizard walks you through five steps:

```mermaid
flowchart TD
    A([Start]) --> B[Load export + state file]
    B --> C{State file\nexists?}
    C -- yes --> D[Resume — skip MIGRATED devices]
    C -- no --> E[Initialise all devices as PENDING]
    D & E --> F[/Pick a device from the list/]
    F --> G[1 · Remove from ZHA\nConfirm deletion in HA UI\nPoll registry until gone]
    G --> H[2 · Reset physical device\nFactory-reset to clear old pairing]
    H --> I[3 · Pair with Z2M\nEnable permit_join 120 s\nPoll Z2M every 3 s by IEEE]
    I --> J{Device\nfound?}
    J -- no --> K{Retry?}
    K -- yes --> I
    K -- no --> L[Mark FAILED · Save state]
    J -- yes --> M[4 · Rename\nApply ZHA name + area in Z2M + HA]
    M --> N[5 · Validate\nPoll HA entity states until online]
    N --> O{All entities\nonline?}
    O -- yes --> P[Mark MIGRATED · Save state]
    O -- no --> Q[Mark MIGRATED with warning\nCheck HA manually]
    P & Q --> R([Done — run again for next device])
    L --> R
```

State is written to `zha-migration-state.json` after every transition.
`Ctrl-C` at any point marks the device `FAILED` and saves — rerun to retry.

## Z2M authentication

The `Z2MClient` tries three strategies in order:

```mermaid
flowchart LR
    A([Request]) --> B[Bearer token\ndirectly on Z2M_URL]
    B -- JSON response --> Z([OK])
    B -- not JSON --> C[Exchange for ingress\nsession cookie via\n/api/hassio/ingress/session]
    C -- cookie set --> Z
    C -- no Supervisor --> D[HA-native fallback\nDevice list · permit_join · rename\nvia WebSocket + mqtt.publish]
    D --> Z
```

## Architecture

```text
CLI Layer       main.py  (Typer, -h / -v)
    ↓
Command Layer   commands/{export, migrate, list_z2m, compare*, rename*}.py
    ↓
Client Layer    ha_client.py  (WebSocket + REST)
                z2m_client.py (HTTP ingress, three-tier auth)
    ↓
Data Layer      models.py (Pydantic v2)
                migration_state.py (JSON on disk, keyed by IEEE)
```

\* `compare` and `rename` are not yet implemented.

## Device state machine

```mermaid
stateDiagram-v2
    [*] --> PENDING
    PENDING --> IN_PROGRESS : wizard started
    IN_PROGRESS --> MIGRATED : all steps passed
    IN_PROGRESS --> FAILED : pairing failed / Ctrl-C
    FAILED --> IN_PROGRESS : retry
```

## Development

```bash
uv run pytest          # all tests
uv run ruff check .    # lint
uv run ruff format .   # format
```
