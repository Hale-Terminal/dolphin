import logging
from threading import local
from typing import Any, List, Optional

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class PluginConfiguration(BaseModel):
    pass


class PluginMount(type):
    def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)
        if IPlugin in bases:
            return new_cls
        if new_cls.title is None:
            new_cls.title = new_cls.__name__
        if not new_cls.slug:
            new_cls.slug = new_cls.title.replace(" ", "-").lower()

        return new_cls


class IPlugin(local):
    title: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    version: Optional[str] = None
    author: Optional[str] = None
    author_url: Optional[str] = None
    configuration: Optional[dict] = None
    resource_links = ()

    schema: PluginConfiguration
    commands: List[Any] = []

    events: Any = None

    enabled: bool = False
    can_disable: bool = True
    multiple: bool = False

    def is_enabled(self) -> bool:
        if not self.enabled:
            return False
        if not self.can_disable:
            return True
        return True

    def get_title(self) -> Optional[str]:
        return self.title

    def get_description(self) -> Optional[str]:
        return self.description

    def get_resource_links(self) -> List[Any]:
        return self.resource_links


class Plugin(IPlugin):
    __version__ = 1
    __metaclass__ = PluginMount
