from rich.console import Console

console = Console()


def compare_command(zha_export: str) -> None:
    """Compare a ZHA export against current Zigbee2MQTT devices."""
    console.print("[yellow]compare[/yellow] command is not yet implemented.")
    console.print(f"ZHA export: {zha_export}")
