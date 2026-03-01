# Rename commands

zigporter provides two rename commands that cascade changes across your entire Home Assistant
configuration — automations, scripts, scenes, and Lovelace dashboards.

Both commands default to a **dry run** that shows a full preview. Pass `--apply` or confirm
the interactive prompt to write changes.

---

## Rename an entity

Rename a Home Assistant entity ID and update every reference to it:

```bash
zigporter rename-entity <old_entity_id> <new_entity_id>
```

### Example

```bash
# Preview changes
zigporter rename-entity light.living_room_1 light.living_room_ceiling

# Apply the rename
zigporter rename-entity light.living_room_1 light.living_room_ceiling --apply
```

### What gets updated

- **Entity registry** — the entity ID itself
- **Automations** — `entity_id` fields and service call targets
- **Scripts** — `entity_id` fields and service call targets
- **Scenes** — entity entries
- **Lovelace dashboards** — all storage-mode dashboards (UI-managed)

### Limitations

Jinja2 template expressions are **not** patched automatically:

```yaml
# This will NOT be updated — review manually
condition: "{{ states('light.living_room_1') == 'on' }}"
```

YAML-mode dashboards stored outside the HA config API are also not reachable from the
command line — the output will list them by name so you can edit them manually.

---

## Rename a device

Rename any Home Assistant device by name and cascade the change to all its entities and
every reference to those entities across HA. Works with any integration — Zigbee, Z-Wave,
Matter, Wi-Fi, and more.

```bash
zigporter rename-device <old_name> <new_name>
```

Partial name matching is supported — the command finds devices whose name contains `old_name`.

### Example

```bash
# Preview changes
zigporter rename-device "Living Room 1" "Living Room Ceiling"

# Apply the rename
zigporter rename-device "Living Room 1" "Living Room Ceiling" --apply
```

### What gets updated

1. Z2M device friendly name (via the Z2M rename API)
2. All entity IDs that follow the device name slug pattern
3. All references to those entities (same scope as `rename-entity`)

For entities whose IDs don't follow the device name pattern, the command prompts you to
provide the new entity ID manually rather than guessing.

### Limitations

Same template and YAML-mode dashboard limitations as `rename-entity` apply.

---

## Dry run output

Running without `--apply` prints a summary table:

```
Rename plan: light.living_room_1 → light.living_room_ceiling
┌──────────────┬──────────────────────┬─────────────┐
│ Context      │ Name                 │ Occurrences │
├──────────────┼──────────────────────┼─────────────┤
│ registry     │ Entity registry      │ 1           │
│ automation   │ Turn on living room  │ 3           │
│ lovelace     │ Default dashboard    │ 2           │
└──────────────┴──────────────────────┴─────────────┘
Total: 6 occurrences across 3 locations
```

You are then prompted to apply or cancel before any changes are written.
