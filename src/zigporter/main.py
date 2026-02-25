from datetime import date
from importlib.metadata import version as pkg_version
from pathlib import Path

import typer
from rich.console import Console

from zigporter.commands.compare import compare_command
from zigporter.commands.export import export_command
from zigporter.commands.inspect import inspect_command
from zigporter.commands.list_z2m import list_z2m_command
from zigporter.commands.migrate import migrate_command
from zigporter.commands.rename import rename_command
from zigporter.config import load_config, load_z2m_config

app = typer.Typer(
    name="zigporter",
    help="Migrate Zigbee devices from ZHA to Zigbee2MQTT in a controlled manner.",
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help"]},
)
console = Console()


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(pkg_version("zigporter"))
        raise typer.Exit()


@app.callback()
def _app_options(
    _version: bool = typer.Option(
        None,
        "--version",
        "-v",
        callback=_version_callback,
        is_eager=True,
        help="Show version and exit.",
    ),
) -> None:
    pass


def _get_config() -> tuple[str, str, bool]:
    try:
        return load_config()
    except ValueError as exc:
        console.print(f"[red]Configuration error:[/red] {exc}")
        raise typer.Exit(code=1) from exc


def _get_z2m_config() -> tuple[str, str]:
    try:
        return load_z2m_config()
    except ValueError as exc:
        console.print(f"[red]Configuration error:[/red] {exc}")
        raise typer.Exit(code=1) from exc


@app.command()
def export(
    output: Path = typer.Option(
        None,
        "--output",
        "-o",
        help="Output file path. Defaults to zha-export-YYYY-MM-DD.json in the current directory.",
    ),
    pretty: bool = typer.Option(False, "--pretty", help="Pretty-print JSON output."),
) -> None:
    """Export current ZHA devices, entities, areas, and automation references to JSON."""
    ha_url, token, verify_ssl = _get_config()

    if output is None:
        output = Path(f"zha-export-{date.today()}.json")

    export_command(output=output, pretty=pretty, ha_url=ha_url, token=token, verify_ssl=verify_ssl)


@app.command(name="list-z2m")
def list_z2m() -> None:
    """List all devices currently paired with Zigbee2MQTT."""
    ha_url, token, verify_ssl = _get_config()
    z2m_url, mqtt_topic = _get_z2m_config()
    list_z2m_command(
        ha_url=ha_url, token=token, z2m_url=z2m_url, verify_ssl=verify_ssl, mqtt_topic=mqtt_topic
    )


@app.command()
def compare(
    zha_export: Path = typer.Argument(
        ...,
        help="Path to a ZHA export JSON file produced by the export command.",
        exists=True,
    ),
) -> None:
    """Compare a ZHA export against current Zigbee2MQTT devices."""
    compare_command(zha_export=str(zha_export))


@app.command()
def rename(
    zha_export: Path = typer.Argument(
        ...,
        help="Path to a ZHA export JSON file produced by the export command.",
        exists=True,
    ),
    apply: bool = typer.Option(
        False,
        "--apply",
        help="Apply rename changes. Without this flag the command runs in dry-run mode.",
    ),
) -> None:
    """Rename Zigbee2MQTT devices/entities to match names from a ZHA export.

    Runs in dry-run mode by default. Use --apply to execute changes.
    """
    rename_command(zha_export=str(zha_export), apply=apply)


def _resolve_export(path: Path | None) -> Path:
    if path is not None:
        return path
    candidates = sorted(Path(".").glob("zha-export-*.json"), reverse=True)
    if not candidates:
        console.print(
            "[red]Error:[/red] No ZHA_EXPORT argument given and no zha-export-*.json found in the current directory."
        )
        raise typer.Exit(code=1)
    resolved = candidates[0]
    console.print(f"[dim]Using export file:[/dim] {resolved}")
    return resolved


@app.command()
def migrate(
    zha_export: Path = typer.Argument(
        None,
        help="Path to a ZHA export JSON file. Defaults to the most recent zha-export-*.json in the current directory.",
    ),
    state: Path = typer.Option(
        Path("zha-migration-state.json"),
        "--state",
        help="Path to the migration state file. Created automatically if it does not exist.",
    ),
    status: bool = typer.Option(
        False,
        "--status",
        help="Show migration progress summary and exit without entering the wizard.",
    ),
) -> None:
    """Interactive wizard to migrate ZHA devices to Zigbee2MQTT one at a time.

    Tracks progress in a state file so you can safely stop and resume across sessions.
    """
    ha_url, token, verify_ssl = _get_config()
    z2m_url, mqtt_topic = _get_z2m_config()

    migrate_command(
        zha_export_path=_resolve_export(zha_export),
        state_path=state,
        status_only=status,
        ha_url=ha_url,
        token=token,
        verify_ssl=verify_ssl,
        z2m_url=z2m_url,
        mqtt_topic=mqtt_topic,
    )


@app.command()
def inspect(
    debug: bool = typer.Option(
        False, "--debug", help="Print Lovelace fetch diagnostics before the report."
    ),
) -> None:
    """Show all automations, scripts, scenes, and dashboard cards that depend on a ZHA device.

    Connects live to Home Assistant, lets you pick a device, and prints a full
    dependency report.
    """
    ha_url, token, verify_ssl = _get_config()
    inspect_command(ha_url=ha_url, token=token, verify_ssl=verify_ssl, debug=debug)


if __name__ == "__main__":
    app()
