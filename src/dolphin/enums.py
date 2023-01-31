from enum import Enum


class DolphinEnum(str, Enum):
    def __str__(self) -> str:
        return str.__str__(self)


class UserRoles(DolphinEnum):
    admin = "Admin"
    manager = "Manager"
    member = "Member"


class Visibility(DolphinEnum):
    open = "Open"
    restricted = "Restricted"
