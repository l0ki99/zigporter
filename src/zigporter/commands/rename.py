from rich.console import Console

console = Console()


def rename_command(zha_export: str, apply: bool) -> None:
    """Rename Zigbee2MQTT devices/entities to match a ZHA export.

    Runs in dry-run mode by default. Pass --apply to execute changes.
    """
    mode = "[green]APPLY[/green]" if apply else "[blue]DRY RUN[/blue]"
    console.print(f"[yellow]rename[/yellow] command is not yet implemented. Mode: {mode}")
    console.print(f"ZHA export: {zha_export}")
