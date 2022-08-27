import logging
import os
from time import sleep

import click
import uvicorn
from dolphin import __version__
from dolphin import config


log = logging.getLogger(__name__)


@click.group()
@click.version_option(version=__version__)
def dolphin_cli():
    pass


@dolphin_cli.command("monitor")
def monitor_start():
    from dolphin.services.monitor import run

    while True:
        run()
        sleep(config.MONITOR_WAIT_TIME)


@dolphin_cli.group("server")
def dolphin_server():
    pass


@dolphin_server.command("routes")
def show_routes():
    from tabulate import tabulate
    from dolphin.main import api_router

    table = []
    for r in api_router.routes:
        table.append([r.path, ",".join(r.methods)])

    click.secho(tabulate(table, headers=["Path", "Authenticated", "Methods"]), fg="blue")


@dolphin_server.command("config")
def show_config():
    import sys
    import inspect
    from tabulate import tabulate
    from dolphin import config

    func_members = inspect.getmembers(sys.modules[config.__name__])

    table = []
    for key, value in func_members:
        if key.isupper():
            table.append([key, value])

    click.secho(tabulate(table, headers=["Key", "Value"]), fg="blue")


@dolphin_server.command("develop")
@click.option(
    "--log-level",
    type=click.Choice(["debug", "info", "error", "warning", "critical"]),
    default="debug",
    help="Log level to use",
)
def run_server(log_level):
    os.environ["LOG_LEVEL"] = log_level.upper()
    uvicorn.run("dolphin.main:app", debug=True, log_level=log_level)


@dolphin_server.command("start")
def server_start():
    uvicorn.run("dolphin.main:app", host="0.0.0.0")


def entrypoint():
    dolphin_cli()


if __name__ == "__main__":
    entrypoint()
