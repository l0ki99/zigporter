# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]


## [0.1.0] - 2026-02-26

### Added
- Add streamlined UX: preflight check, auto-export, config dir (#7)

### Changed
- Update uv-build requirement from <0.10.0,>=0.9.26 to >=0.9.26,<0.11.0 (#6)
- Streamlined UX: setup wizard, check command, improved migrate flow (#8)

### Dependencies
- Bump astral-sh/setup-uv from 6 to 7 (#1)
- Bump actions/upload-artifact from 4 to 6 (#5)
- Bump actions/download-artifact from 4 to 7 (#4)
- Bump codecov/codecov-action from 4 to 5 (#3)
- Bump actions/github-script from 7 to 8 (#2)

## [0.1.0] - 2025-02-26

### Added

- **Initial release of `zigporter`** — CLI tool for migrating Zigbee devices from ZHA to Zigbee2MQTT in Home Assistant
  - `export` command to export ZHA device data from Home Assistant
  - `list-z2m` command to list devices currently in Zigbee2MQTT
  - `migrate` command with interactive wizard for device-by-device migration
  - `setup` command to create and configure `~/.config/zigporter/.env`
- **Persistent migration state tracking** — JSON-based state with `PENDING → IN_PROGRESS → MIGRATED / FAILED` lifecycle; migrations can be paused and resumed
- **HA WebSocket integration** — ZHA device registry queries via WebSocket (compatible with HA 2025+ which dropped the REST ZHA endpoint)
- **Three-tier Z2M auth fallback** — Bearer token, ingress session cookie, and HA-native `mqtt.publish` via `call_service`
- SSL verification support via `HA_VERIFY_SSL` config option

[Unreleased]: https://github.com/nordstad/zigporter/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/nordstad/zigporter/compare/v0.1.0...v0.1.0
[0.1.0]: https://github.com/nordstad/zigporter/releases/tag/v0.1.0
