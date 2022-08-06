import traceback
import logging
import pkg_resources
from sqlalchemy.exc import SQLAlchemyError

from dolphin.plugins.base import plugins, register

log = logging.getLogger(__name__)


def install_plugins():
    for ep in pkg_resources.iter_entry_points("dolphin.plugins"):
        log.info(f"Attempting to load plugin: {ep.name}")
        try:
            plugin = ep.load()
            register(plugin)
            log.info(f"Successfully loaded plugin: {ep.name}")
        except SQLAlchemyError:
            log.error(
                "Something went wrong with creating plugin rows, is the database setup correctly?"
            )
            log.error(f"Failed to load plugin {ep.name}:{traceback.format_exc()}")
        except KeyError as e:
            log.info(f"Failed to load plugin {ep.name} due to missing configuration items. {e}")
        except Exception:
            log.error(f"Failed to load plugin {ep.name}:{traceback.format_exc()}")


def install_plugin_events(api):
    for plugin in plugins.all():
        if plugin.events:
            pass
