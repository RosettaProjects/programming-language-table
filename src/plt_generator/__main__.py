from sys import argv

from . import cli


def main() -> None:
    subcommand = argv[1] if len(argv) > 1 else "generate"
    action = {
        "generate": cli.generate,
        "dryrun": cli.dryrun,
        "sync": cli.sync,
    }.get(subcommand)

    if not action:
        raise ValueError(
            f"Unknown subcommand: {subcommand}. Available commands: generate, dryrun, sync."
        )
    action()
